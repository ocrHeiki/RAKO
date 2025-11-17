# analyser.py – Palo Alto Threat Logianalüüs + Valepositiivsed + MITRE ATT&CK
# Autoriseeritud kasutus: jah
# Versioon: 4.0 – Lõplik versioon

import subprocess
import sys
import os
import importlib
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --------------------------
# PAKETID
# --------------------------
def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"📦 Paigaldan {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])

REQUIRED = ["pandas", "matplotlib", "python-docx", "openpyxl"]
for pkg in REQUIRED:
    pkg_name = pkg.replace("-", "_")
    install_and_import(pkg_name)

# --------------------------
# KAUSTAD
# --------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"
REPORTS_DIR = BASE_DIR / "reports"
RESULTS_DIR = BASE_DIR / "tulemused"
for d in [RAW_DIR, REPORTS_DIR, RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

today = datetime.now()
today_str = today.strftime('%Y-%m-%d')
current_time = today.strftime('%Y-%m-%d %H:%M')

# --------------------------
# AJAVAHMIKU TUVASTUS
# --------------------------
def detect_time_range(dates):
    if not dates:
        return "24h"
    min_date = min(dates)
    max_date = max(dates)
    diff_days = (max_date - min_date).days + 1
    if diff_days <= 1:
        return "24h"
    elif diff_days <= 7:
        return "7 päeva"
    elif diff_days <= 31:
        return "30 päeva"
    else:
        return f"{diff_days} päeva"

# --------------------------
# VÄRVID
# --------------------------
COLORS_SEV = {"low": "#0000FF", "medium": "#FFFF00", "high": "#FFA500", "critical": "#FF0000"}
COLORS_ACTION = {"allow": "#33CC33", "deny": "#CC3333", "drop": "#3366CC", "alert": "#FFCC00", "reset-both": "#9933CC"}
COLORS_CAT = {
    "hacktool": "#9933CC", "dos": "#FFFF66", "info-leak": "#66CCFF",
    "code-execution": "#FF6600", "brute-force": "#FFCC00", "spyware": "#3399FF"
}

# --------------------------
# MITRE ATT&CK
# --------------------------
attck_mapping = {
    "Nmap Aggressive Option Print Detection": {"tactic": "Discovery", "technique": "T1046"},
    "Microsoft Windows RPC Encrypted Data Detected": {"tactic": "Execution", "technique": "T1059"},
    "SSL Double Client Hello Cipher Suite Length Mismatch": {"tactic": "Defense Evasion", "technique": "T1071"},
    "HTTP2 Protocol Suspicious RST STREAM Frame detection": {"tactic": "Defense Evasion", "technique": "T1071"},
    "Windows Local Security Authority lsardelete access": {"tactic": "Credential Access", "technique": "T1003"}
}

# --------------------------
# VALEPOSITIIVSE RISKI HINNANGUD – 16 THREATI
# --------------------------
fp_guidance = {
    "Nmap Aggressive Option Print Detection": {
        "risk": "KÕRGE",
        "reason": "Sageli kasutavad seda legitiimsed süsteemihaldurid või turvameeskonnad skaneerimiseks.",
        "tip": "Kontrolli IP konteksti ja kas see kuulub ettevõttesse. Mitte alati oht – võib viidata pentestile."
    },
    "SIP Register Message Brute Force Attack": {
        "risk": "KESKMINE",
        "reason": "SIP-serverid saavad sageli vigaseid päringuid isegi ilma ründeta.",
        "tip": "Vaata, kas IP kuulub tuntud kliendivõrku või partnerile. Mõnikord valed konfiguratsioonid."
    },
    "OpenSSL Handshake Cipher Two More Times Changed Anomaly": {
        "risk": "MADAL–KESKMINE",
        "reason": "Võib olla tegu ainult ühilduvus veaga klientrakenduses (nt vana seade).",
        "tip": "Kontrolli seadetüüpe, mis loovad ühendust ja nende OpenSSL versioone."
    },
    "FTP REST": {
        "risk": "KÕRGE",
        "reason": "Täiesti legitiimne käsk, mida kasutavad backup- ja failisüsteemid.",
        "tip": "Kontrolli, kas FTP kasutatakse sisemiselt või väliselt. Tõeline oht vaid kui jagatakse tundlikku infot."
    },
    "Windows Local Security Authority lsardelete access": {
        "risk": "KESKMINE",
        "reason": "Sageli legitiimne haldustegevus või teenuste skaneerimine.",
        "tip": "Vaata, kas tegu oli süsteemihalduri tegevusega ja kas IP kuulub sisepiirkonda."
    },
    "SMB: User Password Brute Force Attempt": {
        "risk": "MADAL–KESKMINE",
        "reason": "Sageli tekib siis, kui lõppkasutaja sisestab valesti parooli korduvalt.",
        "tip": "Vaata kas IP kuulub sisepiirkonda – tõeline oht ainult väljast."
    },
    "SSL Double Client Hello Cipher Suite Length Mismatch": {
        "risk": "MADAL",
        "reason": "Võib olla seotud mõne ebatavalise või vananenud klientrakendusega.",
        "tip": "Vaata, millise brauseri või rakendusega loodi ühendus."
    },
    "Cisco Malformed SNMP Message Format String Vulnerability": {
        "risk": "KESKMINE",
        "reason": "Sageli esineb vigaste seadmete puhul (nt printerid, haldusliidesed).",
        "tip": "Kontrolli, kas IP kuulub Cisco seadmete haldusvõrku."
    },
    "Suspicious User-Agent Strings Detection": {
        "risk": "KÕRGE",
        "reason": "Paljud analüüsi- ja automatiseeritud tööriistad kasutavad samu stringe – nt curl, wget.",
        "tip": "Ava IP-logid ja leia täpne brauseri nimi – mitte alati spyware."
    },
    "HTTP2 Protocol Suspicious RST STREAM Frame detection": {
        "risk": "KESKMINE",
        "reason": "Sageli esineb halvasti programmeeritud rakendustes.",
        "tip": "Vaata, kas tegu oli rakenduse vigadega, mitte ainult pahavara vastu."
    },
    "Kahtlane PowerShell-i käivitus": {
        "risk": "KESKMINE",
        "reason": "Süsteemihaldurid kasutavad sageli PowerShelli skripte.",
        "tip": "Ava skripti sisu – kas see tuleb ettevõttesisest tühist või välisest allikast?"
    },
    "Kahtlane pikk URL koos paljude parameetritega": {
        "risk": "KÕRGE",
        "reason": "Sageli kasutatakse CMS-ides või veebivormides – pole alati ohtlik.",
        "tip": "Ava leht ja vaata URL-i sisu, kas tegu tegelikult mõõdukate parameetritega."
    },
    "Võimalik Cobalt Strike Beacon tegevus": {
        "risk": "MADAL",
        "reason": "Kui kasutatakse legitiimset red teami, siis võib olla lubatud tegevus.",
        "tip": "Vaata, kas IP kuulub soovitustele – muidu tõeline oht."
    },
    "Võimalik failide allalaadimine": {
        "risk": "KÕRGE",
        "reason": "Arendajad või süsteemid kasutavad sageli neid tööriistu.",
        "tip": "Vaata, mis fail laeti alla ja kas allikas on usaldusväärne."
    },
    "Võimalik HTTP pahatahtliku sisu tuvastamine": {
        "risk": "KESKMINE",
        "reason": "Sageli valed automaattuvastused veebiserverite puhul.",
        "tip": "Ava lehe sisu ja võrdle – kas tegu on legitiimse dünaamilise veebilehega."
    },
    "HTTP Response Content Length Too Long": {
        "risk": "KESKMINE",
        "reason": "Sageli on tegu suurte failide päringutega või API vastustega.",
        "tip": "Kontrolli, kas tegu on legitiimse API või failiteenusega."
    }
}

# --------------------------
# FUNKTSIOONID
# --------------------------
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m:
        return datetime.strptime(f"{m.group(3)}-{m.group(2)}-{m.group(1)}", "%Y-%m-%d").date()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    if m:
        return datetime.strptime(m.group(0), "%Y-%m-%d").date()
    return today.date()

def first_existing(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

def norm_lower(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()

def bar(series, title, outpath, colors=None, rot=0):
    if series.empty: return
    plt.figure(figsize=(10, 5))
    c = [colors.get(str(i).lower(), "#888888") for i in series.index] if colors else "#888888"
    series.plot(kind="bar", color=c)
    plt.title(title)
    plt.xticks(rotation=rot)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def pie(series, title, outpath):
    if series.empty: return
    plt.figure(figsize=(6, 6))
    plt.pie(series, labels=series.index, autopct="%1.1f%%", startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def add_image(doc: Document, img_path: Path, caption: str, width_in=6.0):
    if img_path.exists():
        p = doc.add_paragraph()
        run = p.add_run()
        run.add_picture(str(img_path), width=Inches(width_in))
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph(caption)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

# --------------------------
# PEAMINE FUNKTSIOON
# --------------------------
def main():
    csv_files = list(RAW_DIR.glob("*.csv"))
    if not csv_files:
        print("⚠️ Ühtegi CSV-faili ei leitud kaustas: raw/")
        return

    processed_files = []
    dates = []
    dfs = []

    for fpath in csv_files:
        try:
            df = pd.read_csv(fpath, low_memory=False)
            df['_source_file'] = fpath.name
            dfs.append(df)
            processed_files.append(fpath.name)
            dates.append(iso_from_filename(fpath.name))
        except Exception as e:
            print(f"⚠️ Viga faili lugemisel {fpath}: {e}")

    if not dfs:
        print("⚠️ Ühtegi loetavat CSV-faili ei leitud.")
        return

    df_all = pd.concat(dfs, ignore_index=True)
    time_range = detect_time_range(dates)

    # Veeruteisendus
    sev_col = first_existing(df_all, ["Severity", "severity", "sev"])
    act_col = first_existing(df_all, ["Action", "action", "act"])
    cat_col = first_existing(df_all, ["thr_category", "category", "Threat Category"])
    name_col = first_existing(df_all, ["Threat/Content Name", "threat_name"])
    src_col = first_existing(df_all, ["Source address", "src", "Source"])
    dst_col = first_existing(df_all, ["Destination address", "dst", "Destination"])

    if sev_col: df_all["sev_norm"] = norm_lower(df_all[sev_col])
    if act_col: df_all["act_norm"] = norm_lower(df_all[act_col])
    if cat_col: df_all["cat_norm"] = norm_lower(df_all[cat_col])
    if name_col: df_all["tname_norm"] = df_all[name_col].astype(str).str.strip()
    if src_col: df_all["src_norm"] = df_all[src_col].astype(str).str.strip()
    if dst_col: df_all["dst_norm"] = df_all[dst_col].astype(str).str.strip()

    # MITRE ATT&CK seostus
    def map_attack(threat):
        for key in attck_mapping:
            if key.lower() in str(threat).lower():
                return pd.Series([attck_mapping[key]['tactic'], attck_mapping[key]['technique']])
        return pd.Series(['-', '-'])

    df_all[['attack_tactic', 'attack_technique']] = df_all[name_col].apply(map_attack)

    # STATISTIKA
    total = len(df_all)
    sev_counts = df_all["sev_norm"].value_counts() if "sev_norm" in df_all.columns else pd.Series(dtype=int)
    act_counts = df_all["act_norm"].value_counts() if "act_norm" in df_all.columns else pd.Series(dtype=int)
    top_cat = df_all["cat_norm"].value_counts().head(10) if "cat_norm" in df_all.columns else pd.Series(dtype=int)
    top_threat = df_all["tname_norm"].value_counts().head(10) if "tname_norm" in df_all.columns else pd.Series(dtype=int)
    top_src = df_all["src_norm"].value_counts().head(10) if "src_norm" in df_all.columns else pd.Series(dtype=int)
    top_dst = df_all["dst_norm"].value_counts().head(10) if "dst_norm" in df_all.columns else pd.Series(dtype=int)
    attack_summary = df_all[df_all['attack_tactic'] != '-'].groupby(['attack_tactic', 'attack_technique', 'tname_norm']).size().reset_index(name='count')

    # TXT raport
    out_txt = RESULTS_DIR / f"soc_summary_{today_str}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"SOC {time_range} KOONDARUANNE – {today_str}\n")
        f.write("=" * 50 + "\n")
        f.write(f"Analüüsi aeg: {current_time}\n")
        f.write(f"Kasutatud logifailid ({len(processed_files)}):\n")
        for fname in sorted(processed_files):
            f.write(f"  - {fname}\n")
        f.write(f"Kirjeid kokku: {total}\n")
        if dates:
            f.write(f"Ajavahemik: {min(dates)} kuni {max(dates)}\n\n")
        else:
            f.write("\n")

        if not sev_counts.empty:
            f.write("■ Severity jaotus:\n")
            for s, c in sev_counts.items():
                f.write(f"  - {s.title():<10}: {c}\n")

        if not act_counts.empty:
            f.write("\n■ Action jaotus:\n")
            for a, c in act_counts.items():
                f.write(f"  - {a:<15}: {c}\n")

        if not top_cat.empty:
            f.write("\n■ TOP kategooriad:\n")
            for i, (k, v) in enumerate(top_cat.items(), 1):
                f.write(f"  {i}. {k} – {v}\n")

        if not top_threat.empty:
            f.write("\n■ TOP 10 Threat / Content Name:\n")
            for i, (k, v) in enumerate(top_threat.items(), 1):
                f.write(f"  {i}. {k} – {v}\n")

        if not top_src.empty:
            f.write("\n■ TOP 10 allika IP:\n")
            for i, (k, v) in enumerate(top_src.items(), 1):
                f.write(f"  {i}. {k} – {v}\n")

        if not top_dst.empty:
            f.write("\n■ TOP 10 sihtmärgi IP:\n")
            for i, (k, v) in enumerate(top_dst.items(), 1):
                f.write(f"  {i}. {k} – {v}\n")

        if not attack_summary.empty:
            f.write("\n■ MITRE ATT&CK tegevused:\n")
            for _, row in attack_summary.iterrows():
                f.write(f"  [{row['attack_tactic']}] → {row['attack_technique']} ({row['tname_norm']}): {row['count']} korda\n")
        else:
            f.write("\n■ MITRE ATT&CK tegevused:\n  Seostusi ei leitud.\n")

        # Valepositiivne risk - TOP 10
        f.write("\n■ Valepositiivne risk - TOP 10 Threat Name:\n")
        for i, (threat, count) in enumerate(top_threat.items()):
            if i >= 10: break
            f.write(f"\n{i+1}. {threat} – {count} korda\n")
            guide = fp_guidance.get(threat, {})
            if guide:
                f.write(f"  🔸 Valepositiivne risk: {guide.get('risk', '–')}\n")
                f.write(f"  🔸 Põhjus: {guide.get('reason', '–')}\n")
                f.write(f"  🔸 Soovitus: {guide.get('tip', '–')}\n")
            else:
                f.write("  🔸 Valepositiivse riski info puudub.\n")

    # Graafikud
    bar(sev_counts, f"Severity – {today_str}", REPORTS_DIR / f"sev_bar_{today_str}.png", COLORS_SEV)
    pie(sev_counts, f"Severity (%)", REPORTS_DIR / f"sev_pie_{today_str}.png")
    bar(act_counts, f"Action – {today_str}", REPORTS_DIR / f"act_bar_{today_str}.png", COLORS_ACTION, rot=45)
    bar(top_cat, f"TOP kategooriad – {today_str}", REPORTS_DIR / f"cat_bar_{today_str}.png", COLORS_CAT, rot=45)
    bar(top_threat, f"TOP Threat Name", REPORTS_DIR / f"threat_bar_{today_str}.png", rot=45)
    bar(top_src, f"TOP allikad", REPORTS_DIR / f"src_bar_{today_str}.png", rot=45)
    bar(top_dst, f"TOP sihtmärgid", REPORTS_DIR / f"dst_bar_{today_str}.png", rot=45)

    # DOCX raport
    doc = Document()
    doc.add_heading(f"SOC {time_range} aruanne – {today_str}", level=1)
    doc.add_paragraph(f"Analüüsi aeg: {current_time}")
    if dates:
        doc.add_paragraph(f"Ajavahemik: {min(dates)} kuni {max(dates)}")
    doc.add_paragraph(f"Logifailid ({len(processed_files)}): " + ", ".join(processed_files[:3]) + ("..." if len(processed_files) > 3 else ""))

    doc.add_heading("Tekstiline kokkuvõte", level=2)
    with open(out_txt, "r", encoding="utf-8") as f:
        parsing_fp_section = False
        for line in f:
            if line.startswith("■ Valepositiivne risk"):
                break
            if not parsing_fp_section:
                doc.add_paragraph(line.rstrip("\n"))
    doc.add_paragraph("")

    doc.add_heading("MITRE ATT&CK tegevused", level=2)
    if attack_summary.empty:
        doc.add_paragraph("Seostusi ei leitud.")
    else:
        for _, row in attack_summary.iterrows():
            doc.add_paragraph(f"[{row['attack_tactic']}] → {row['attack_technique']} ({row['tname_norm']}): {row['count']} korda")

    doc.add_heading("Valepositiivne risk – TOP 10 Threat Name", level=2)
    for i, (threat, count) in enumerate(top_threat.items()):
        if i >= 10: break
        doc.add_paragraph(f"{i+1}. {threat} – {count} korda")
        guide = fp_guidance.get(threat, {})
        if guide:
            doc.add_paragraph(f"🔸 Valepositiivne risk: {guide.get('risk', '–')}", style='Intense Quote')
            doc.add_paragraph(f"🔸 Põhjus: {guide.get('reason', '–')}")
            doc.add_paragraph(f"🔸 Soovitus: {guide.get('tip', '–')}")
        else:
            doc.add_paragraph("🔸 Valepositiivse riski info puudub.")
        doc.add_paragraph("")

    doc.add_heading("Graafikud", level=2)
    for img, cap in [
        (REPORTS_DIR / f"sev_bar_{today_str}.png", "Severity jaotus"),
        (REPORTS_DIR / f"sev_pie_{today_str}.png", "Severity osakaal"),
        (REPORTS_DIR / f"act_bar_{today_str}.png", "Action jaotus"),
        (REPORTS_DIR / f"cat_bar_{today_str}.png", "TOP kategooriad"),
        (REPORTS_DIR / f"threat_bar_{today_str}.png", "TOP Threat"),
        (REPORTS_DIR / f"src_bar_{today_str}.png", "TOP allikad"),
        (REPORTS_DIR / f"dst_bar_{today_str}.png", "TOP sihtmärgid"),
    ]:
        add_image(doc, img, cap)

    docx_path = RESULTS_DIR / f"soc_summary_{today_str}.docx"
    doc.save(str(docx_path))

    # Lõpp
    print(f"\n✅ {time_range} aruanne valmis.")
    print(f" - TXT : {out_txt}")
    print(f" - DOCX: {docx_path}")
    print(f" - Graafikud: {REPORTS_DIR}")

if __name__ == "__main__":
    main()
