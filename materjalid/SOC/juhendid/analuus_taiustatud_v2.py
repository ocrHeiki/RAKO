# analuus_taiustatud_v2.py
# Täiustatud SOC logianalüüs (Palo Alto Threat 24h)
# Autor: <sinu nimi>
# Eeldused: pip install pandas matplotlib openpyxl

import argparse
import re
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Värvikaardid (kokkulepitud HEX-id) ----------
SEVERITY_COLORS = {
    "critical": "#FF0000",
    "high":     "#FFA500",
    "medium":   "#FFFF00",
    "low":      "#0000FF",
}
ACTION_COLORS = {
    "allow":        "#33CC33",
    "deny":         "#CC3333",
    "drop":         "#3366CC",
    "alert":        "#FFCC00",
    "reset-both":   "#9933CC",
    "reset-server": "#800080",
}
TYPE_COLORS = {
    "malware":      "#CC0033",
    "vulnerability":"#FF3333",
    "spyware":      "#3399FF",
    "suspicious":   "#FFCC66",
    "benign":       "#66CC66",
}
CATEGORY_COLORS = {
    "command-and-control": "#CC0000",
    "code-execution":      "#FF6600",
    "sql-injection":       "#FF9933",
    "brute-force":         "#FFCC00",
    "dos":                 "#FFFF66",
    "hacktool":            "#9933CC",
    "info-leak":           "#66CCFF",
    "spyware":             "#3399FF",
    "code-obfuscation":    "#996633",
}

# ---------- Abid ----------
def first_existing(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

def norm_lower(series):
    return series.astype(str).str.strip().str.lower()

def parse_possible_datetimes(df):
    for col in ["Time Received","Timestamp","Start Time","End Time","High Res Timestamp"]:
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
            except Exception:
                pass

def fig_bar(series, title, path, color_map=None):
    plt.figure(figsize=(10,5))
    if color_map:
        colors = [color_map.get(str(idx).lower(), None) for idx in series.index]
    else:
        colors = None
    series.plot(kind="bar", color=colors)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def fig_pie(series, title, path):
    plt.figure(figsize=(6,6))
    series.plot(kind="pie", autopct="%1.1f%%", startangle=90, ylabel="")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def infer_base_from_csv(csv_path: Path) -> Path:
    """
    Kui CSV asub SOC/raw all, tagasta SOC juurkaust.
    Muidu kasuta kasutaja Documents\SOC.
    """
    p = csv_path.resolve()
    parts = [x.lower() for x in p.parts]
    if "soc" in parts:
        # leia 'soc' indeks ja tagasta see kaust
        idx = parts.index("soc")
        return Path(*p.parts[:idx+1])
    # fallback
    return Path.home() / "Documents" / "SOC"

def iso_from_filename(name: str, default_date=None) -> str:
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)  # dd.mm.yyyy
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)   # yyyy-mm-dd
    if m2:
        return m2.group(0)
    return (default_date or datetime.now().date().isoformat())

# ---------- Argumendid ----------
parser = argparse.ArgumentParser(description="SOC 24h täiustatud analüüs (Palo Alto Threat).")
parser.add_argument("csv", nargs="?", default=None, help="Sisend-CSV tee (kui jätad tühjaks, kasutatakse SOC/raw/ThreatLog_06.10.2025.csv)")
args = parser.parse_args()

# Vaikimisi CSV
default_csv = Path.home() / "Documents" / "SOC" / "raw" / "ThreatLog_06.10.2025.csv"
csv_path = Path(args.csv) if args.csv else default_csv
if not csv_path.exists():
    raise SystemExit(f"[ERR] CSV ei leitud: {csv_path}")

BASE = infer_base_from_csv(csv_path)
RAW_DIR = BASE / "raw"
PROC_DIR = BASE / "processed"
REP_DIR = BASE / "reports"
PROC_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR.mkdir(parents=True, exist_ok=True)

date_iso = iso_from_filename(csv_path.name)

print(f"[INFO] BASE:     {BASE}")
print(f"[INFO] CSV:      {csv_path}")
print(f"[INFO] Kuupäev:  {date_iso}")

# ---------- Loe CSV ----------
df = pd.read_csv(csv_path, encoding="utf-8", low_memory=False)
print(f"[INFO] Ridu kokku: {len(df):,}")
parse_possible_datetimes(df)

# ---------- Leia veerud (paindlik) ----------
severity_col = first_existing(df, ["Severity","severity"])
risk_col     = first_existing(df, ["Risk","risk","Risk Level","risk_level","Risk of app"])
action_col   = first_existing(df, ["Action","action"])
cat_col      = first_existing(df, ["thr_category","category","Threat Category"])
type_col     = first_existing(df, ["Threat/Content Type","threat/content type","Threat Type","threat_type"])
name_col     = first_existing(df, ["Threat/Content Name","Threat Name","content_name","threat_name"])
src_col      = first_existing(df, ["Source address","Src","Source","src_ip","Source IP","src"])
dst_col      = first_existing(df, ["Destination address","Dst","Destination","dst_ip","Destination IP","dst"])

# Normaliseeritud tööveerud
if severity_col: df["severity_norm"] = norm_lower(df[severity_col])
if risk_col:     df["risk_norm"]     = pd.to_numeric(df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0).astype(int)
if action_col:   df["action_norm"]   = norm_lower(df[action_col])
if cat_col:      df["category_norm"] = norm_lower(df[cat_col])
if type_col:     df["type_norm"]     = norm_lower(df[type_col])
if name_col:     df["tname_norm"]    = df[name_col].astype(str).str.strip()
if src_col:      df["src_ip_norm"]   = df[src_col].astype(str).str.strip()
if dst_col:      df["dst_ip_norm"]   = df[dst_col].astype(str).str.strip()

# ---------- 1) Alertide koguarv ----------
total_alerts = len(df)
print(f"[SUM] Alertide koguarv: {total_alerts:,}")

# ---------- 2) Severity jaotus ----------
if severity_col:
    sev_counts = df["severity_norm"].value_counts()
    print("\n[SUM] Severity jaotus:\n", sev_counts)
    fig_bar(sev_counts, "Severity jaotus (24h)", REP_DIR / f"severity_{date_iso}.png", SEVERITY_COLORS)
else:
    sev_counts = pd.Series(dtype=int)

# ---------- 3) Riskitasemed ----------
if risk_col:
    risk_counts = df["risk_norm"].value_counts().sort_index()
    print("\n[SUM] Riskitasemed:\n", risk_counts)
    fig_bar(risk_counts, "Riskitasemed (1–5)", REP_DIR / f"riskitasemed_{date_iso}.png")
else:
    risk_counts = pd.Series(dtype=int)

# ---------- 4) TOP 5 ohukategooriat ----------
if cat_col:
    top_cat = df["category_norm"].value_counts().head(5)
    print("\n[TOP] Kategooriad (TOP 5):\n", top_cat)
    fig_bar(top_cat, "TOP 5 ohukategooriat", REP_DIR / f"top_kategooriad_{date_iso}.png", CATEGORY_COLORS)
else:
    top_cat = pd.Series(dtype=int)

# ---------- 5) TOP 5 allika ja sihtmärgi IP ----------
if src_col:
    top_src = df["src_ip_norm"].value_counts().head(5)
    fig_bar(top_src, "TOP 5 allika IP", REP_DIR / f"top_src_{date_iso}.png")
else:
    top_src = pd.Series(dtype=int)

if dst_col:
    top_dst = df["dst_ip_norm"].value_counts().head(5)
    fig_bar(top_dst, "TOP 5 sihtmärk IP", REP_DIR / f"top_dst_{date_iso}.png")
else:
    top_dst = pd.Series(dtype=int)

# ---------- 6) Severity + Risk kombineeritud ----------
if severity_col and risk_col:
    combo = df.groupby(["severity_norm","risk_norm"]).size().unstack(fill_value=0).sort_index()
    combo_path = PROC_DIR / f"combo_severity_risk_{date_iso}.xlsx"
    with pd.ExcelWriter(combo_path) as xw:
        combo.to_excel(xw, sheet_name="Severity_Risk")
    print(f"\n[OUT] Severity×Risk tabel: {combo_path}")
else:
    combo = pd.DataFrame()

# ---------- 7) TOP 5 ründetüüpi igas Severitys ----------
if type_col and severity_col:
    grouped = df.groupby(["severity_norm","type_norm"]).size().reset_index(name="count")
    top5_per_sev = (
        grouped.sort_values(["severity_norm","count"], ascending=[True,False])
        .groupby("severity_norm").head(5)
    )
    top5_path = PROC_DIR / f"top5_runded_per_severity_{date_iso}.xlsx"
    with pd.ExcelWriter(top5_path) as xw:
        for sev in sorted(top5_per_sev["severity_norm"].unique()):
            tmp = top5_per_sev[top5_per_sev["severity_norm"]==sev].drop(columns=["severity_norm"])
            tmp.to_excel(xw, sheet_name=sev.title(), index=False)
    print(f"[OUT] TOP5 ründetüübid per Severity: {top5_path}")

# ---------- 8) Threat/Content Name kordused vs Severity ----------
if name_col and severity_col:
    name_sev = df.groupby(["tname_norm","severity_norm"]).size().reset_index(name="count")
    threatname_summary = (
        name_sev.groupby("tname_norm")
        .agg(severity_tasemed=("severity_norm", lambda x: ", ".join(sorted(pd.Series(x).unique()))),
             esinemisi_kokku=("count", "sum"))
        .sort_values("esinemisi_kokku", ascending=False)
    )
    korduvad = threatname_summary[threatname_summary["severity_tasemed"].str.contains(",")]
    tname_all_path = PROC_DIR / f"threatname_severity_kordused_{date_iso}.xlsx"
    tname_dups_path = PROC_DIR / f"threatname_korduvad_{date_iso}.xlsx"
    with pd.ExcelWriter(tname_all_path) as xw:
        threatname_summary.to_excel(xw, sheet_name="Koond", index=True)
    with pd.ExcelWriter(tname_dups_path) as xw:
        korduvad.to_excel(xw, sheet_name="Korduvad", index=True)
    print(f"[OUT] Threat/Content Name koond:    {tname_all_path}")
    print(f"[OUT] Threat/Content Name korduvad: {tname_dups_path}")
else:
    threatname_summary = pd.DataFrame()
    korduvad = pd.DataFrame()

# ---------- 9) Threat/Content Type pirukas ----------
if type_col:
    type_counts = df["type_norm"].value_counts()
    fig_pie(type_counts, "Threat/Content Type osakaal (24h)", REP_DIR / f"threat_type_pirukas_{date_iso}.png")
else:
    type_counts = pd.Series(dtype=int)

# ---------- 10) Fookusfiltrid ja eksport ----------
sev_mask = df["severity_norm"].isin(["high","critical"]) if severity_col else False
act_mask = df["action_norm"].isin(["alert","reset-both","reset-server"]) if action_col else False
cat_mask = df["category_norm"].isin(["command-and-control","code-execution","sql-injection","brute-force","dos","malware","spyware"]) if cat_col else False
typ_mask = df["type_norm"].isin(["malware","vulnerability","spyware"]) if type_col else False

focus = df[ (sev_mask) | (act_mask) | (cat_mask) | (typ_mask) ].copy()
focus_path = PROC_DIR / f"threat_focus_{date_iso}.csv"
focus.to_csv(focus_path, index=False, encoding="utf-8")
print(f"\n[OUT] Fookusfail: {focus_path} (read: {len(focus):,})")

# ---------- 11) Excel koond ----------
xlsx_path = PROC_DIR / f"threat_summary_{date_iso}.xlsx"
with pd.ExcelWriter(xlsx_path) as xw:
    df.to_excel(xw, sheet_name="Raw", index=False)
    focus.to_excel(xw, sheet_name="Focus", index=False)
    if not sev_counts.empty:
        sev_counts.rename_axis("severity").reset_index(name="count").to_excel(xw, sheet_name="Severity", index=False)
    if not risk_counts.empty:
        risk_counts.rename_axis("risk").reset_index(name="count").to_excel(xw, sheet_name="Risk", index=False)
    if not type_counts.empty:
        type_counts.rename_axis("type").reset_index(name="count").to_excel(xw, sheet_name="ThreatType", index=False)
    if not top_cat.empty:
        top_cat.rename_axis("category").reset_index(name="count").to_excel(xw, sheet_name="TopCategories", index=False)
    if not top_src.empty:
        top_src.rename_axis("src_ip").reset_index(name="count").to_excel(xw, sheet_name="TopSrc", index=False)
    if not top_dst.empty:
        top_dst.rename_axis("dst_ip").reset_index(name="count").to_excel(xw, sheet_name="TopDst", index=False)
    if not combo.empty:
        combo.to_excel(xw, sheet_name="Severity_Risk")
    if name_col and severity_col:
        name_sev.to_excel(xw, sheet_name="ThreatName_Sev", index=False)
print(f"[OUT] Excel kokkuvõte: {xlsx_path}")

# ---------- 12) TXT raport ----------
txt_path = PROC_DIR / f"raport_koond_{date_iso}.txt"
with open(txt_path, "w", encoding="utf-8") as fh:
    fh.write(f"SOC Päevaohutõrje Raport – {date_iso}\n")
    fh.write("-" * 38 + "\n")
    fh.write(f"Alertide koguarv: {total_alerts:,}\n\n")

    if not sev_counts.empty:
        fh.write("Severity jaotus:\n")
        for k in ["critical","high","medium","low"]:
            if k in sev_counts.index:
                fh.write(f" - {k.title()}: {int(sev_counts[k])}\n")
        fh.write("\n")

    if not risk_counts.empty:
        fh.write("Riskitasemed (1–5):\n")
        for r, c in risk_counts.sort_index().items():
            fh.write(f" - Risk {int(r)}: {int(c)}\n")
        fh.write("\n")

    if not top_cat.empty:
        fh.write("TOP 5 ohukategooriat:\n")
        for i, (k, v) in enumerate(top_cat.items(), 1):
            fh.write(f" {i}. {k} – {int(v)}\n")
        fh.write("\n")

    if not top_src.empty:
        fh.write("TOP 5 allika IP-d:\n")
        for i, (k, v) in enumerate(top_src.items(), 1):
            fh.write(f" {i}. {k} – {int(v)} korda\n")
        fh.write("\n")

    if not top_dst.empty:
        fh.write("TOP 5 sihtmärk IP-d:\n")
        for i, (k, v) in enumerate(top_dst.items(), 1):
            fh.write(f" {i}. {k} – {int(v)} korda\n")
        fh.write("\n")

    if name_col and severity_col:
        fh.write("Threat/Content Name kordused severity tasemete lõikes:\n")
        if not threatname_summary.empty:
            fh.write(f" - Kokku: {len(threatname_summary)} erinevat threat-nime\n")
        if not korduvad.empty:
            fh.write(f" - Korduva severity'ga ohte: {len(korduvad)}\n")
            top_name = threatname_summary.index[0]
            fh.write(f" - Kõige sagedasem: {top_name} ({threatname_summary.iloc[0]['severity_tasemed']})\n")
        fh.write("\n")

    fh.write(f"Severity×Risk tabel: {combo_path if severity_col and risk_col else '—'}\n")
    fh.write(f"TOP5 ründetüübid per Severity: {top5_path if (type_col and severity_col) else '—'}\n")
    fh.write(f"Graafikud salvestatud: {REP_DIR}\n")
    fh.write("-" * 38 + "\n")
    fh.write(f"Loodud: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
print(f"[OUT] TXT raport: {txt_path}")

print("\n[OK] Analüüs lõpetatud.")
print(f" - Processed: {PROC_DIR}")
print(f" - Reports:   {REP_DIR}")
