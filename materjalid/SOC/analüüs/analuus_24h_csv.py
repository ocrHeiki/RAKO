# analuus_paevane_csv_plus.py – Päevane SOC analüüs CSV failist
# Autor: <sinu nimi>
# Kasutus: py analuus_paevane_csv_plus.py
# Eeldused: pip install pandas matplotlib openpyxl

from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re

# -----------------------------
# Kaustad
# -----------------------------
BASE = Path.home() / "Documents" / "SOC"
RAW  = BASE / "raw"
PROC = BASE / "processed"
REP  = BASE / "reports"
PROC.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Fikseeritud värvikaardid
# -----------------------------
COLORS_SEV = {
    "low": "#0000FF",      # sinine
    "medium": "#FFFF00",   # kollane
    "high": "#FFA500",     # oranž
    "critical": "#FF0000", # punane
}
COLORS_ACTION = {
    "allow": "#33CC33",
    "deny": "#CC3333",
    "drop": "#3366CC",
    "alert": "#FFCC00",
}
COLORS_TYPE = {
    "malware": "#CC0033",
    "vulnerability": "#FF3333",
    "spyware": "#3399FF",
    "suspicious": "#FFCC66",
    "benign": "#66CC66",
}
COLORS_CAT = {
    "command-and-control": "#CC0000",
    "code-execution": "#FF6600",
    "sql-injection": "#FF9933",
    "brute-force": "#FFCC00",
    "dos": "#FFFF66",
    "hacktool": "#9933CC",
    "info-leak": "#66CCFF",
    "spyware": "#3399FF",
    "code-obfuscation": "#996633",
}

# -----------------------------
# Abi funktsioonid
# -----------------------------
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return m2.group(0) if m2 else datetime.now().date().isoformat()

def first_existing(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

def norm_lower(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()

def bar(series, title, outpath, colors=None, rot=0):
    plt.figure(figsize=(10,5))
    c = [colors.get(str(i).lower(), None) for i in series.index] if colors else None
    series.plot(kind="bar", color=c)
    plt.title(title)
    plt.xticks(rotation=rot, ha="right" if rot else "center")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def pie(series, title, outpath):
    plt.figure(figsize=(6,6))
    series.plot(kind="pie", autopct="%1.1f%%", startangle=90, ylabel="")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

# -----------------------------
# Peaosa
# -----------------------------
def main():
    # Leia kõige uuem ThreatLog fail
    csv_files = sorted(RAW.glob("ThreatLog_*.csv"), reverse=True)
    if not csv_files:
        print("[!] Ei leitud ühtegi CSV faili kaustast 'raw/'.")
        return

    path = csv_files[0]  # võtab viimase (uuema) faili
    date_iso = iso_from_filename(path.name)
    print(f"[i] Analüüsitakse faili: {path.name} ({date_iso})")

    df = pd.read_csv(path, encoding="utf-8", low_memory=False)

    # Leia veerud
    sev_col = first_existing(df, ["Severity", "severity"])
    risk_col = first_existing(df, ["Risk", "risk", "Risk Level", "risk_level"])
    cat_col = first_existing(df, ["thr_category", "category", "Threat Category"])
    type_col = first_existing(df, ["Threat/Content Type", "threat/content type"])
    src_col = first_existing(df, ["Source address", "Source", "src"])
    dst_col = first_existing(df, ["Destination address", "Destination", "dst"])

    # Normaliseeri
    if sev_col:  df["sev_norm"]  = norm_lower(df[sev_col])
    if cat_col:  df["cat_norm"]  = norm_lower(df[cat_col])
    if type_col: df["type_norm"] = norm_lower(df[type_col])
    if src_col:  df["src_norm"]  = df[src_col].astype(str).str.strip()
    if dst_col:  df["dst_norm"]  = df[dst_col].astype(str).str.strip()
    if risk_col:
        df["risk_norm"] = pd.to_numeric(
            df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce"
        ).fillna(0).astype(int)

    # -----------------------------
    # Arvutused
    # -----------------------------
    total = len(df)
    sev_counts = df["sev_norm"].value_counts() if sev_col else pd.Series(dtype=int)
    risk_avg = df["risk_norm"].mean() if risk_col else None
    hi_crit = int(sev_counts.get("high", 0) + sev_counts.get("critical", 0))
    hi_crit_pct = round(100 * hi_crit / total, 2) if total else 0.0

    # TOP kategooriad, type, src/dst
    top_cat = df["cat_norm"].value_counts().head(10) if cat_col else pd.Series(dtype=int)
    type_counts = df["type_norm"].value_counts() if type_col else pd.Series(dtype=int)
    top_src = df["src_norm"].value_counts().head(10) if src_col else pd.Series(dtype=int)
    top_dst = df["dst_norm"].value_counts().head(10) if dst_col else pd.Series(dtype=int)

    # -----------------------------
    # TXT raport
    # -----------------------------
    today = datetime.now().date().isoformat()
    out_txt = PROC / f"paevakoond_{today}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("SOC 24h PÄEVA KOONDARUANNE\n")
        f.write("===========================\n\n")
        f.write(f"Fail: {path.name}\nKuupäev: {date_iso}\n\n")
        f.write(f"Alertide koguarv: {total}\n")
        f.write(f"High+Critical kokku: {hi_crit} ({hi_crit_pct}%)\n")
        if risk_avg is not None:
            f.write(f"Keskmine Riskitase: {risk_avg:.2f}\n")
        f.write("\nSeverity jaotus:\n")
        for sev, cnt in sev_counts.items():
            f.write(f"  - {sev.title():<10}: {cnt}\n")

        f.write("\nTOP kategooriad:\n")
        for i, (cat, val) in enumerate(top_cat.items(), 1):
            f.write(f"  {i}. {cat} – {val}\n")

        f.write("\nTOP allika IP:\n")
        for i, (ip, val) in enumerate(top_src.items(), 1):
            f.write(f"  {i}. {ip} – {val}\n")

        f.write("\nTOP sihtmärgi IP:\n")
        for i, (ip, val) in enumerate(top_dst.items(), 1):
            f.write(f"  {i}. {ip} – {val}\n")

        f.write("\nMärkused:\n- % High+Critical näitab ohutõusu trendi.\n- Kõrge riskitase viitab korduvatele ohtudele.\n")

    # -----------------------------
    # Graafikud
    # -----------------------------
    bar(sev_counts, "Severity jaotus (24h)", REP / f"paev_severity_{today}.png", colors=COLORS_SEV)
    if not type_counts.empty:
        pie(type_counts, "Threat/Content Type (24h)", REP / f"paev_threat_type_{today}.png")
    if not top_cat.empty:
        bar(top_cat, "TOP kategooriad (24h)", REP / f"paev_top_kategooriad_{today}.png", colors=COLORS_CAT, rot=45)
    if not top_src.empty:
        bar(top_src, "TOP 10 allika IP (24h)", REP / f"paev_top_src_{today}.png", rot=45)
    if not top_dst.empty:
        bar(top_dst, "TOP 10 sihtmärgi IP (24h)", REP / f"paev_top_dst_{today}.png", rot=45)

    # CSV + XLSX väljund
    out_csv = PROC / f"paevakoond_{today}.csv"
    out_xlsx = PROC / f"paevakoond_{today}.xlsx"
    df_out = pd.DataFrame({
        "Severity": sev_counts.index,
        "Count": sev_counts.values
    })
    df_out.to_csv(out_csv, index=False, encoding="utf-8")
    with pd.ExcelWriter(out_xlsx) as xw:
        df_out.to_excel(xw, sheet_name="Severity", index=False)
        top_cat.rename_axis("Category").reset_index(name="Count").to_excel(xw, sheet_name="TopCategories", index=False)
        type_counts.rename_axis("Type").reset_index(name="Count").to_excel(xw, sheet_name="ThreatType", index=False)

    print(f"[OK] Päeva analüüs valmis: TXT, CSV, XLSX ja graafikud loodud.")

if __name__ == "__main__":
    main()
