# analuus_taiustatud.py
# SOC - Täiustatud Palo Alto Threat logi analüüs
# Autor: <sinu nimi>
# Eeldused: pip install pandas matplotlib openpyxl

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import re

# ----------------------------
# KONFIGURATSIOON
# ----------------------------
BASE = Path(r"C:\Users\<SINU_NIMI>\Documents\SOC")
RAW_DIR = BASE / "raw"
PROC_DIR = BASE / "processed"
REP_DIR = BASE / "reports"

RAW_FILE = "ThreatLog_06.10.2025.csv"
m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", RAW_FILE)
DATE_ISO = f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else "2025-10-06"

for d in [PROC_DIR, REP_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ----------------------------
# ABI
# ----------------------------
def color_by_severity(level):
    colors = {
        "critical": "#FF0000",
        "high": "#FFA500",
        "medium": "#FFFF00",
        "low": "#0000FF"
    }
    return colors.get(level.lower(), "#CCCCCC")

def bar_chart(series, title, path, color_func=None):
    plt.figure(figsize=(10,5))
    colors = [color_func(x) for x in series.index] if color_func else None
    series.plot(kind="bar", color=colors)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

def pie_chart(series, title, path):
    plt.figure(figsize=(6,6))
    series.plot(kind="pie", autopct="%1.1f%%", startangle=90, ylabel="")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()

# ----------------------------
# LAE FAIL
# ----------------------------
src = RAW_DIR / RAW_FILE
print(f"[INFO] Laen {src}")
df = pd.read_csv(src, encoding="utf-8", low_memory=False)

print(f"[INFO] Ridu: {len(df):,}")

# ----------------------------
# VEERUNIMED (paindlik leidmine)
# ----------------------------
def first_existing(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

severity_col = first_existing(df, ["Severity", "severity"])
risk_col = first_existing(df, ["Risk", "risk", "Risk Level", "risk_level"])
cat_col = first_existing(df, ["thr_category", "category", "Threat Category"])
src_col = first_existing(df, ["Source address", "Src", "Source", "src_ip"])
dst_col = first_existing(df, ["Destination address", "Dst", "Destination", "dst_ip"])
type_col = first_existing(df, ["Threat/Content Type", "Threat Type", "threat_type"])

# Normaliseeri väärtused
if severity_col: df["severity_norm"] = df[severity_col].astype(str).str.lower()
if risk_col: df["risk_norm"] = df[risk_col].astype(str).str.extract(r"(\d+)")[0].fillna(0).astype(int)
if cat_col: df["category_norm"] = df[cat_col].astype(str).str.lower()
if src_col: df["src_ip_norm"] = df[src_col].astype(str)
if dst_col: df["dst_ip_norm"] = df[dst_col].astype(str)
if type_col: df["type_norm"] = df[type_col].astype(str).str.lower()

# ----------------------------
# 1) ALERTIDE KOKKUARV
# ----------------------------
total_alerts = len(df)
print(f"[INFO] Alertide koguarv: {total_alerts:,}")

# ----------------------------
# 2) SEVERITY JAOTUS
# ----------------------------
sev_counts = df["severity_norm"].value_counts()
bar_chart(sev_counts, "Severity jaotus (24h)", REP_DIR / f"severity_{DATE_ISO}.png", color_by_severity)

# ----------------------------
# 3) RISKITASEMED
# ----------------------------
if risk_col:
    risk_counts = df["risk_norm"].value_counts().sort_index()
    bar_chart(risk_counts, "Riskitasemed (1–5)", REP_DIR / f"riskitasemed_{DATE_ISO}.png")
else:
    risk_counts = pd.Series(dtype=int)

# ----------------------------
# 4) TOP OHUKATEGOORIAD
# ----------------------------
if cat_col:
    top_cat = df["category_norm"].value_counts().head(5)
    bar_chart(top_cat, "TOP 5 ohukategooriat", REP_DIR / f"top_kategooriad_{DATE_ISO}.png")
else:
    top_cat = pd.Series(dtype=int)

# ----------------------------
# 5) TOP ALLIKAD JA SIHTMÄRGID
# ----------------------------
if src_col:
    top_src = df["src_ip_norm"].value_counts().head(5)
    bar_chart(top_src, "TOP 5 allika IP", REP_DIR / f"top_src_{DATE_ISO}.png")
else:
    top_src = pd.Series(dtype=int)

if dst_col:
    top_dst = df["dst_ip_norm"].value_counts().head(5)
    bar_chart(top_dst, "TOP 5 sihtmärk IP", REP_DIR / f"top_dst_{DATE_ISO}.png")
else:
    top_dst = pd.Series(dtype=int)

# ----------------------------
# 6) SEVERITY + RISK KOMBINATSIOON
# ----------------------------
if severity_col and risk_col:
    combo = df.groupby(["severity_norm", "risk_norm"]).size().unstack(fill_value=0)
    combo.to_excel(PROC_DIR / f"combo_severity_risk_{DATE_ISO}.xlsx")
    print("[INFO] Salv. severity-risk kombineeritud kokkuvõte")
else:
    combo = pd.DataFrame()

# ----------------------------
# 7) TOP 5 RÜNDE TÜÜPI IGAS SEVERITY-RISK GRUPIS
# ----------------------------
if type_col and severity_col:
    grouped = df.groupby(["severity_norm", "type_norm"]).size().reset_index(name="count")
    top5_per_sev = (
        grouped.sort_values(["severity_norm", "count"], ascending=[True, False])
        .groupby("severity_norm")
        .head(5)
    )
    top5_per_sev.to_excel(PROC_DIR / f"top5_runded_{DATE_ISO}.xlsx", index=False)
    print("[INFO] Salv. TOP 5 ründetüüpi iga severity taseme jaoks")

# ----------------------------
# 8) ÜLDINE RAPORT CSV
# ----------------------------
summary = pd.DataFrame({
    "Kokku Alerts": [total_alerts],
    "Severity tasemeid": [len(sev_counts)],
    "Riskitasemeid": [len(risk_counts)],
    "TOP kategooria": [top_cat.index[0] if not top_cat.empty else "—"],
    "TOP allikas IP": [top_src.index[0] if not top_src.empty else "—"],
    "TOP sihtmärk IP": [top_dst.index[0] if not top_dst.empty else "—"]
})
summary.to_csv(PROC_DIR / f"raport_koond_{DATE_ISO}.csv", index=False, encoding="utf-8")

print("\n✅ Analüüs valmis! Tulemused:")
print(f" - Processed: {PROC_DIR}")
print(f" - Reports: {REP_DIR}")
