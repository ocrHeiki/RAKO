# soc_24h.py – 24h SOC analüüs ühest CSV failist (TXT + CSV + XLSX + graafikud)
# Autor: <sinu nimi> | Eeldused: pip install pandas matplotlib openpyxl
# Käivitus (Windows PowerShell):  py soc_24h.py

from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re, shutil

# -----------------------------------
# Kaustad: standard 'processed' + ühilduvus 'process'
# -----------------------------------
BASE = Path.home() / "Documents" / "SOC"
RAW   = BASE / "raw"
PROC  = BASE / "processed"
PROC2 = BASE / "process"   # kui kasutusel on see nimi, teeme peegelduse
REP   = BASE / "reports"

for d in (RAW, PROC, PROC2, REP):
    d.mkdir(parents=True, exist_ok=True)

# -----------------------------------
# Värvikaardid (standard)
# -----------------------------------
COLORS_SEV = {"low":"#0000FF","medium":"#FFFF00","high":"#FFA500","critical":"#FF0000"}
COLORS_ACTION = {
    "allow":"#33CC33","deny":"#CC3333","drop":"#3366CC","alert":"#FFCC00",
    "reset-both":"#9933CC","reset-server":"#800080"
}
COLORS_TYPE = {"malware":"#CC0033","vulnerability":"#FF3333","spyware":"#3399FF","suspicious":"#FFCC66","benign":"#66CC66"}
COLORS_CAT = {
    "command-and-control":"#CC0000","code-execution":"#FF6600","sql-injection":"#FF9933","brute-force":"#FFCC00",
    "dos":"#FFFF66","hacktool":"#9933CC","info-leak":"#66CCFF","spyware":"#3399FF","code-obfuscation":"#996633"
}

# -----------------------------------
# Valepositiivide näidiskirjed – kohanda oma keskkonnale!
# -----------------------------------
FALSE_POSITIVE_CATEGORIES = {
    "dns.query.anomaly","port.scan","ssl.decrypt.failure","internal.backup.sync","trusted.update.service"
}
FALSE_POSITIVE_NAMES = {
    "windows-update","office-cdn","zabbix-probe","okta-healthcheck","backup-job","scanner-internal"
}

# -----------------------------------
# Abifunktsioonid
# -----------------------------------
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)  # dd.mm.yyyy
    if m: return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)   # yyyy-mm-dd
    return m2.group(0) if m2 else datetime.now().date().isoformat()

def first_existing(df, names):
    for n in names:
        if n in df.columns: return n
    return None

def norm_lower(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()

def bar(series, title, outpath, colors=None, rot=0):
    if series is None or series.empty: return
    plt.figure(figsize=(10,5))
    c = [colors.get(str(i).lower(), None) for i in series.index] if colors else None
    series.plot(kind="bar", color=c)
    plt.title(title); plt.xticks(rotation=rot, ha="right" if rot else "center")
    plt.tight_layout(); plt.savefig(outpath); plt.close()

def pie(series, title, outpath):
    if series is None or series.empty: return
    plt.figure(figsize=(6,6))
    series.plot(kind="pie", autopct="%1.1f%%", startangle=90, ylabel="")
    plt.title(title); plt.tight_layout(); plt.savefig(outpath); plt.close()

def copy_to_process(path: Path):
    try:
        shutil.copy2(path, PROC2 / path.name)
    except Exception:
        pass

# -----------------------------------
# Peaosa
# -----------------------------------
def main():
    # Leia kõige värskem ThreatLog CSV
    csv_files = sorted(RAW.glob("ThreatLog_*.csv"), reverse=True)
    if not csv_files:
        print("[!] Ei leitud CSV-faile kaustas 'raw/'."); return

    path = csv_files[0]
    date_iso = iso_from_filename(path.name)
    print(f"[i] Analüüsitakse: {path.name} ({date_iso})")

    df = pd.read_csv(path, encoding="utf-8", low_memory=False)

    # Veerud / normaliseerimine
    sev_col   = first_existing(df, ["Severity","severity"])
    risk_col  = first_existing(df, ["Risk","risk","Risk Level","risk_level","Risk of app"])
    cat_col   = first_existing(df, ["thr_category","category","Threat Category"])
    type_col  = first_existing(df, ["Threat/Content Type","threat/content type","Threat Type","threat_type"])
    act_col   = first_existing(df, ["Action","action"])
    name_col  = first_existing(df, ["Threat/Content Name","Threat Name","content_name","threat_name"])
    src_col   = first_existing(df, ["Source address","Source","src","src_ip","Source IP"])
    dst_col   = first_existing(df, ["Destination address","Destination","dst","dst_ip","Destination IP"])

    if sev_col:  df["sev_norm"]   = norm_lower(df[sev_col])
    if risk_col:
        df["risk_norm"] = pd.to_numeric(df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0).astype(int)
    if cat_col:  df["cat_norm"]   = norm_lower(df[cat_col])
    if type_col: df["type_norm"]  = norm_lower(df[type_col])
    if act_col:  df["act_norm"]   = norm_lower(df[act_col])
    if name_col: df["tname_norm"] = df[name_col].astype(str).str.strip()
    if src_col:  df["src_norm"]   = df[src_col].astype(str).str.strip()
    if dst_col:  df["dst_norm"]   = df[dst_col].astype(str).str.strip()

    # Põhinäitajad
    total       = len(df)
    sev_counts  = df["sev_norm"].value_counts() if "sev_norm" in df.columns else pd.Series(dtype=int)
    act_counts  = df["act_norm"].value_counts() if "act_norm" in df.columns else pd.Series(dtype=int)
    type_counts = df["type_norm"].value_counts() if "type_norm" in df.columns else pd.Series(dtype=int)
    risk_avg    = float(df["risk_norm"].mean()) if "risk_norm" in df.columns and len(df)>0 else None
    hi_crit     = int(sev_counts.get("high",0) + sev_counts.get("critical",0))
    hi_crit_pct = round(100 * hi_crit / total, 2) if total else 0.0

    # TOP koondid
    top_cat  = df["cat_norm"].value_counts().head(10) if "cat_norm" in df.columns else pd.Series(dtype=int)
    top_name = df["tname_norm"].value_counts().head(10) if "tname_norm" in df.columns else pd.Series(dtype=int)
    top_src  = df["src_norm"].value_counts().head(10) if "src_norm" in df.columns else pd.Series(dtype=int)
    top_dst  = df["dst_norm"].value_counts().head(10) if "dst_norm" in df.columns else pd.Series(dtype=int)

    # TOP 5 ohud iga severity sees (Threat/Content Name + kategooria)
    top5_by_sev = {}
    if {"sev_norm","tname_norm"}.issubset(df.columns):
        g = df.groupby(["sev_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for sev in ["critical","high","medium","low"]:
            tmp = g[g["sev_norm"]==sev].sort_values("count", ascending=False).head(5)
            top5_by_sev[sev] = tmp[["tname_norm","cat_norm","count"]]

    # TOP 5 ohud iga riskitaseme sees
    top5_by_risk = {}
    if {"risk_norm","tname_norm"}.issubset(df.columns):
        gr = df.groupby(["risk_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for risk in sorted(gr["risk_norm"].dropna().unique()):
            tmp = gr[gr["risk_norm"]==risk].sort_values("count", ascending=False).head(5)
            top5_by_risk[int(risk)] = tmp[["tname_norm","cat_norm","count"]]

    # Sagedased valepositiivid
    fp_cat = pd.Series(dtype=int)
    if "cat_norm" in df.columns:
        fp_cat = df[df["cat_norm"].isin(FALSE_POSITIVE_CATEGORIES)]["cat_norm"].value_counts()
    fp_names = pd.Series(dtype=int)
    if "tname_norm" in df.columns:
        fp_names = df[df["tname_norm"].str.lower().isin(FALSE_POSITIVE_NAMES)]["tname_norm"].str.lower().value_counts()

    # Fookusfail: High või Critical
    focus = df[df.get("sev_norm","").isin(["high","critical"])].copy() if "sev_norm" in df.columns else pd.DataFrame()
    if not focus.empty:
        focus_path = PROC / f"threat_focus_{date_iso}.csv"
        focus.to_csv(focus_path, index=False, encoding="utf-8")
        copy_to_process(focus_path)

    # -----------------------------
    # TXT kokkuvõte
    # -----------------------------
    out_txt = PROC / f"24h_summary_{date_iso}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"SOC 24h ANALÜÜS — {path.name}\n")
        f.write("-"*44 + "\n")
        f.write(f"Kuupäev: {date_iso}\n")
        f.write(f"Kokku logikirjeid: {total}\n")
        f.write(f"High+Critical kokku: {hi_crit} ({hi_crit_pct}%)\n")
        if risk_avg is not None:
            f.write(f"Keskmine Riskitase: {risk_avg:.2f}\n")

        if not sev_counts.empty:
            f.write("\nSeverity jaotus:\n")
            for sev, cnt in sev_counts.items():
                f.write(f"  - {sev.title():<10}: {int(cnt)}\n")

        # TOP 5 iga severity
        f.write("\nTOP 5 ohud iga severity sees (Threat/Content Name – Category – Count):\n")
        for sev in ["critical","high","medium","low"]:
            f.write(f"  [{sev.title()}]\n")
            df_top = top5_by_sev.get(sev)
            if df_top is None or len(df_top)==0:
                f.write("    – (puuduvad)\n"); continue
            for _, row in df_top.iterrows():
                f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

        # TOP 5 iga riskitaseme sees
        f.write("\nTOP 5 ohud iga riskitaseme sees (Threat/Content Name – Category – Count):\n")
        if len(top5_by_risk)==0:
            f.write("  – (puuduvad)\n")
        else:
            for risk in sorted(top5_by_risk.keys()):
                f.write(f"  [Risk {risk}]\n")
                df_top = top5_by_risk[risk]
                for _, row in df_top.iterrows():
                    f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

        # Valepositiivid
        f.write("\nSAGEDASED VALEPOSITIIVID (24h):\n")
        f.write("  Kategooriad:\n")
        if not fp_cat.empty:
            for i, (k, v) in enumerate(fp_cat.items(), 1):
                f.write(f"    {i}. {k} – {int(v)}\n")
        else:
            f.write("    – (puuduvad)\n")
        f.write("  Threat/Content Name:\n")
        if not fp_names.empty:
            for i, (k, v) in enumerate(fp_names.items(), 1):
                f.write(f"    {i}. {k} – {int(v)}\n")
        else:
            f.write("    – (puuduvad)\n")

        # Graafikute viide + selgitused
        f.write("\nGraafikud salvestatud kausta: reports/\n")
        f.write("  - paev_severity_bar_{d}.png – Severity jaotus (tulbad)\n".format(d=date_iso))
        f.write("  - paev_severity_pie_{d}.png – Severity osakaal (pirukas)\n".format(d=date_iso))
        f.write("  - paev_action_bar_{d}.png – Action jaotus (tulbad)\n".format(d=date_iso))
        f.write("  - paev_action_pie_{d}.png – Action osakaal (pirukas)\n".format(d=date_iso))
        f.write("  - paev_threat_type_pie_{d}.png – Threat/Content Type pirukas\n".format(d=date_iso))
        f.write("  - paev_top_kategooriad_{d}.png – TOP kategooriad (tulbad)\n".format(d=date_iso))
        f.write("  - paev_top_src_{d}.png – TOP 10 allika IP (tulbad)\n".format(d=date_iso))
        f.write("  - paev_top_dst_{d}.png – TOP 10 sihtmärgi IP (tulbad)\n".format(d=date_iso))
    copy_to_process(out_txt)

    # -----------------------------
    # CSV + XLSX koondtabelid
    # -----------------------------
    out_csv = PROC / f"24h_summary_{date_iso}.csv"
    koond_rows = []
    for label, series in [
        ("Severity", sev_counts),
        ("Action", act_counts),
        ("ThreatType", type_counts),
        ("TopCategory", top_cat),
        ("TopName", top_name),
        ("TopSrc", top_src),
        ("TopDst", top_dst),
    ]:
        if series is not None and not series.empty:
            tmp = pd.DataFrame({"label": series.index.astype(str), "count": series.values})
            tmp.insert(0, "metric", label)
            koond_rows.append(tmp)
    if koond_rows:
        pd.concat(koond_rows, ignore_index=True).to_csv(out_csv, index=False, encoding="utf-8")
        copy_to_process(out_csv)

    out_xlsx = PROC / f"24h_threats_{date_iso}.xlsx"
    with pd.ExcelWriter(out_xlsx) as xw:
        df.to_excel(xw, sheet_name="Raw", index=False)
        if not sev_counts.empty:
            sev_counts.rename_axis("Severity").reset_index(name="Count").to_excel(xw, sheet_name="Severity", index=False)
        if not act_counts.empty:
            act_counts.rename_axis("Action").reset_index(name="Count").to_excel(xw, sheet_name="Action", index=False)
        if not type_counts.empty:
            type_counts.rename_axis("Type").reset_index(name="Count").to_excel(xw, sheet_name="ThreatType", index=False)
        if not top_cat.empty:
            top_cat.rename_axis("Category").reset_index(name="Count").to_excel(xw, sheet_name="TopCategories", index=False)
        if not top_name.empty:
            top_name.rename_axis("ThreatName").reset_index(name="Count").to_excel(xw, sheet_name="TopThreatNames", index=False)
        if not top_src.empty:
            top_src.rename_axis("SrcIP").reset_index(name="Count").to_excel(xw, sheet_name="TopSrc", index=False)
        if not top_dst.empty:
            top_dst.rename_axis("DstIP").reset_index(name="Count").to_excel(xw, sheet_name="TopDst", index=False)
        # Top 5 per severity / risk
        for sev, dft in top5_by_sev.items():
            if dft is not None and len(dft)>0:
                dft.to_excel(xw, sheet_name=f"Top5_{sev.title()}", index=False)
        for risk, dft in top5_by_risk.items():
            if dft is not None and len(dft)>0:
                dft.to_excel(xw, sheet_name=f"Top5_Risk{risk}", index=False)
        # False positives
        if not fp_cat.empty:
            fp_cat.rename_axis("category").reset_index(name="count").to_excel(xw, sheet_name="FalsePos_Categories", index=False)
        if not fp_names.empty:
            fp_names.rename_axis("threat_name").reset_index(name="count").to_excel(xw, sheet_name="FalsePos_Names", index=False)
        # Focus (High + Critical)
        if not focus.empty:
            focus.to_excel(xw, sheet_name="Focus_HiCrit", index=False)
    copy_to_process(out_xlsx)

    # -----------------------------
    # Graafikud (pirukad + tulbad)
    # -----------------------------
    bar(sev_counts, f"Severity jaotus (24h) – {date_iso}", REP / f"paev_severity_bar_{date_iso}.png", colors=COLORS_SEV)
    pie(sev_counts, f"Severity osakaal (24h) – {date_iso}", REP / f"paev_severity_pie_{date_iso}.png")

    bar(act_counts, f"Action jaotus (24h) – {date_iso}", REP / f"paev_action_bar_{date_iso}.png", colors=COLORS_ACTION, rot=45)
    pie(act_counts, f"Action osakaal (24h) – {date_iso}", REP / f"paev_action_pie_{date_iso}.png")

    pie(type_counts, f"Threat/Content Type (24h) – {date_iso}", REP / f"paev_threat_type_pie_{date_iso}.png")

    bar(top_cat, f"TOP kategooriad (24h) – {date_iso}", REP / f"paev_top_kategooriad_{date_iso}.png", colors=COLORS_CAT, rot=45)
    bar(top_src, f"TOP 10 allika IP (24h) – {date_iso}", REP / f"paev_top_src_{date_iso}.png", rot=45)
    bar(top_dst, f"TOP 10 sihtmärgi IP (24h) – {date_iso}", REP / f"paev_top_dst_{date_iso}.png", rot=45)

    print("[OK] 24h analüüs valmis. Väljundid:")
    print(f" - TXT : {out_txt}")
    print(f" - CSV : {out_csv}")
    print(f" - XLSX: {out_xlsx}")
    if not focus.empty: print(f" - Focus (Hi+Crit): {focus_path}")
    print(f" - Graafikud: {REP}")

if __name__ == "__main__":
    main()
