# analuus.py
# SOC – Palo Alto Threat 24h analüüs (Windows)
# Autor: <sinu nimi> | Praktika
# Eeldused: pip install pandas matplotlib openpyxl

from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------
# KONFIGURATSIOON
# ----------------------------
# Muuda oma kasutajanime või asukohta vastavalt:
BASE = Path(r"C:\Users\<SINU_NIMI>\Documents\SOC")
RAW_DIR = BASE / "raw"
PROC_DIR = BASE / "processed"
REP_DIR = BASE / "reports"

RAW_FILE = "ThreatLog_06.10.2025.csv"   # kasutame just seda faili
# Kui soovid automaatselt kuupäeva failinimest, proovi regexi:
m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", RAW_FILE)
DATE_ISO = f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else "2025-10-06"

# Värvilegend (ühtlustatud)
COLORS = {
    "severity": {
        "critical": "#FF0000", "high": "#FFA500",
        "medium": "#FFFF00", "low": "#0000FF"
    },
    "action": {
        "allow": "#33CC33", "deny": "#CC3333", "drop": "#3366CC",
        "alert": "#FFCC00", "reset-both": "#9933CC", "reset-server": "#800080"
    },
    "threat_type": {
        "malware": "#CC0033", "vulnerability": "#FF3333",
        "spyware": "#3399FF", "suspicious": "#FFCC66", "benign": "#66CC66"
    },
    "category": {
        "command-and-control": "#CC0000", "code-execution": "#FF6600",
        "sql-injection": "#FF9933", "brute-force": "#FFCC00",
        "dos": "#FFFF66", "hacktool": "#9933CC",
        "info-leak": "#66CCFF", "spyware": "#3399FF",
        "code-obfuscation": "#996633"
    }
}

# Tee sihtkaustad olemasolevaks
PROC_DIR.mkdir(parents=True, exist_ok=True)
REP_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------
# ABIFUNKTSIOONID
# ----------------------------
def first_existing_column(df, candidates):
    """Tagasta esimene olemasolev veerunimi loetelust (case-sensitive)."""
    for c in candidates:
        if c in df.columns:
            return c
    return None

def normalize_lower(series):
    return series.astype(str).str.lower()

def parse_possible_datetimes(df):
    for col in ["Time Received", "Timestamp", "Start Time", "End Time", "High Res Timestamp"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

def save_bar(series, title, outpath, color_map=None):
    ax = series.plot(kind="bar", figsize=(10,5), title=title)
    if color_map:
        # värvi iga tulp vastavalt nimele, kui leidub
        colors = [color_map.get(str(idx).lower(), None) for idx in series.index]
        for patch, c in zip(ax.patches, colors):
            if c:
                patch.set_color(c)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def save_pie(series, title, outpath):
    series.plot(kind="pie", autopct="%1.1f%%", figsize=(6,6), title=title, ylabel="")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

# ----------------------------
# 1) LAE FAIL
# ----------------------------
src = RAW_DIR / RAW_FILE
print(f"[INFO] Loen: {src}")
df = pd.read_csv(src, encoding="utf-8", low_memory=False)

print(f"[INFO] Ridu: {len(df):,}")
print(f"[INFO] Veerud: {list(df.columns)[:20]} ...")

# ----------------------------
# 2) PARSI AJATEMPLID
# ----------------------------
parse_possible_datetimes(df)

# ----------------------------
# 3) OLULISED VEERUD (paindlik leidmine)
# ----------------------------
sev_col = first_existing_column(df, ["Severity", "severity"])
act_col = first_existing_column(df, ["Action", "action"])
cat_col = first_existing_column(df, ["thr_category", "category", "threat-category"])
tct_col = first_existing_column(df, ["Threat/Content Type", "threat/content type", "Threat Type", "threat_type"])

print("[INFO] Kasutatavad veerud:",
      {"Severity":sev_col, "Action":act_col, "Category":cat_col, "Type":tct_col})

sev = normalize_lower(df[sev_col]) if sev_col else pd.Series(index=df.index, dtype="object")
act = normalize_lower(df[act_col]) if act_col else pd.Series(index=df.index, dtype="object")
cat = normalize_lower(df[cat_col]) if cat_col else pd.Series(index=df.index, dtype="object")
typ = normalize_lower(df[tct_col]) if tct_col else pd.Series(index=df.index, dtype="object")

# ----------------------------
# 4) FOOKUSFILTREERIMINE (24h prioriteedid)
# ----------------------------
sev_mask = sev.isin(["high", "critical"]) if sev_col else False
act_mask = act.isin(["alert", "reset-both", "reset-server"]) if act_col else False
cat_mask = cat.isin([
    "command-and-control","code-execution","sql-injection",
    "brute-force","dos","malware","spyware"
]) if cat_col else False
typ_mask = typ.isin(["malware","vulnerability","spyware"]) if tct_col else False

focus = df[ sev_mask | act_mask | cat_mask | typ_mask ].copy()
print(f"[INFO] Fookusread (uuritavad): {len(focus):,}")

# ----------------------------
# 5) KOKKUVÕTTED
# ----------------------------
if sev_col:
    sev_counts = focus[sev_col].str.lower().value_counts()
    print("\n[SUM] Severity count:\n", sev_counts)
else:
    sev_counts = pd.Series(dtype=int)

if act_col:
    act_counts = focus[act_col].str.lower().value_counts()
    print("\n[SUM] Action count:\n", act_counts)
else:
    act_counts = pd.Series(dtype=int)

if tct_col:
    type_counts = focus[tct_col].str.lower().value_counts()
    print("\n[SUM] Threat/Content Type count:\n", type_counts)
else:
    type_counts = pd.Series(dtype=int)

if cat_col:
    cat_counts = focus[cat_col].str.lower().value_counts()
    print("\n[SUM] Category (thr_category) count:\n", cat_counts)
else:
    cat_counts = pd.Series(dtype=int)

# ----------------------------
# 6) GRAAFIKUD (salvestame reports/)
# ----------------------------
if not cat_counts.empty:
    save_bar(cat_counts, "Ohud kategooriate lõikes (24h)", REP_DIR / f"kategooriad_24h_{DATE_ISO}.png", color_map=COLORS["category"])

if not type_counts.empty:
    # pirukas Threat/Content Type kohta
    save_pie(type_counts, "Threat/Content Type osakaal (24h)", REP_DIR / f"threat_type_pirukas_24h_{DATE_ISO}.png")

if not sev_counts.empty:
    # severity tulp
    # Järjekorras low/medium/high/critical (kui olemas)
    order = [x for x in ["low","medium","high","critical"] if x in sev_counts.index]
    sev_ordered = sev_counts.reindex(order).fill_value if hasattr(sev_counts, "reindex") else sev_counts
    # kui reindex puudub (vanem pandas), kasuta lihtsalt olemasolevat
    series = sev_counts.loc[order] if order else sev_counts
    save_bar(series, "Severity jaotus (24h)", REP_DIR / f"severity_24h_{DATE_ISO}.png", color_map=COLORS["severity"])

# ----------------------------
# 7) EKSPORDID
# ----------------------------
# Fookusread CSV
focus_csv = PROC_DIR / f"threat_focus_{DATE_ISO}.csv"
focus.to_csv(focus_csv, index=False, encoding="utf-8")
print(f"[OUT] Kirjutasin: {focus_csv}")

# Kõrgetasemelised CSV kokkuvõtted
if not sev_counts.empty:
    sev_counts.rename_axis("severity").reset_index(name="count").to_csv(
        PROC_DIR / f"sum_severity_{DATE_ISO}.csv", index=False, encoding="utf-8"
    )
if not act_counts.empty:
    act_counts.rename_axis("action").reset_index(name="count").to_csv(
        PROC_DIR / f"sum_action_{DATE_ISO}.csv", index=False, encoding="utf-8"
    )
if not type_counts.empty:
    type_counts.rename_axis("type").reset_index(name="count").to_csv(
        PROC_DIR / f"sum_threat_type_{DATE_ISO}.csv", index=False, encoding="utf-8"
    )
if not cat_counts.empty:
    cat_counts.rename_axis("category").reset_index(name="count").to_csv(
        PROC_DIR / f"sum_category_{DATE_ISO}.csv", index=False, encoding="utf-8"
    )

# Excel kokkuvõte (mitu sheet'i)
xlsx_path = PROC_DIR / f"threat_summary_{DATE_ISO}.xlsx"
with pd.ExcelWriter(xlsx_path) as xw:
    focus.to_excel(xw, sheet_name="Focus", index=False)
    if not sev_counts.empty:
        sev_counts.rename_axis("severity").reset_index(name="count").to_excel(xw, sheet_name="Severity", index=False)
    if not act_counts.empty:
        act_counts.rename_axis("action").reset_index(name="count").to_excel(xw, sheet_name="Action", index=False)
    if not type_counts.empty:
        type_counts.rename_axis("type").reset_index(name="count").to_excel(xw, sheet_name="ThreatType", index=False)
    if not cat_counts.empty:
        cat_counts.rename_axis("category").reset_index(name="count").to_excel(xw, sheet_name="Category", index=False)

print(f"[OUT] Excel kokkuvõte: {xlsx_path}")

print("\n[OK] Analüüs lõpetatud. Vaata kausta:")
print(f" - Processed: {PROC_DIR}")
print(f" - Reports:   {REP_DIR}")
