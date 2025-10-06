# analuus_nadalakoond.py\n# SOC – Nädala koondanalüüs (7 päeva)
# Autor: <sinu nimi>
# Eeldused: pip install pandas matplotlib openpyxl

from pathlib import Path
import re
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ----------------------------------------------------
# Konfiguratsioon
# ----------------------------------------------------
BASE = Path.home() / "Documents" / "SOC"       # C:\Users\<nimi>\Documents\SOC
PROC = BASE / "processed"
REP  = BASE / "reports"

PROC.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

# Severity värvid (legend)
SEV_COLORS = {
    "critical": "#FF0000",
    "high":     "#FFA500",
    "medium":   "#FFFF00",
    "low":      "#0000FF"
}

# ----------------------------------------------------
# Abifunktsioonid
# ----------------------------------------------------
def parse_date_from_name(name: str):
    # Otsi failinimest ISO kuupäeva: threat_summary_YYYY-MM-DD.xlsx
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    if not m:
        return None
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"

def safe_read_xlsx(path: Path, sheet: str):
    try:
        return pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    except Exception:
        return None

# ----------------------------------------------------
# 1) Leia viimase 7 päeva failid
# ----------------------------------------------------
files = sorted([p for p in PROC.glob("threat_summary_*.xlsx")])
if len(files) == 0:
    print("[ERR] Ei leidnud ühtegi failinimega 'threat_summary_YYYY-MM-DD.xlsx' kaustas processed/.")
    raise SystemExit(1)

# Võtame viimased 7
files = files[-7:]

rows = []
for f in files:
    day = parse_date_from_name(f.name)
    # Loe 'Focus' või kui puudub, entire file esimene sheet
    df_focus = safe_read_xlsx(f, "Focus")
    if df_focus is None:
        df_focus = pd.read_excel(f, engine="openpyxl")
    total_alerts = len(df_focus)

    # Severity sheet (kui on)
    df_sev = safe_read_xlsx(f, "Severity")
    sev_counts = {"critical":0,"high":0,"medium":0,"low":0}
    if df_sev is not None and {"severity","count"}.issubset({c.lower() for c in df_sev.columns}):
        # normalise
        lc = {c.lower(): c for c in df_sev.columns}
        for _, r in df_sev.iterrows():
            sev = str(r[lc["severity"]]).lower()
            cnt = int(r[lc["count"]])
            if sev in sev_counts:
                sev_counts[sev] = cnt
    else:
        if "Severity" in df_focus.columns:
            tmp = df_focus["Severity"].astype(str).str.lower().value_counts()
            for key in sev_counts:
                if key in tmp.index:
                    sev_counts[key] = int(tmp[key])

    # Risk keskmine (kui olemas)
    risk_avg = None
    for cand in ["Risk", "Risk of app", "risk", "risk_norm"]:
        if cand in df_focus.columns:
            try:
                risk_avg = pd.to_numeric(df_focus[cand], errors="coerce").dropna().mean()
                break
            except Exception:
                continue

    # Top kategooria (thr_category)
    top_cat = None
    for cat_col in ["thr_category","category","Category"]:
        if cat_col in df_focus.columns:
            vc = df_focus[cat_col].astype(str).str.lower().value_counts()
            if len(vc) > 0:
                top_cat = vc.index[0]
            break

    rows.append({
        "date": day or f.name,
        "alerts_total": total_alerts,
        "critical": sev_counts["critical"],
        "high": sev_counts["high"],
        "medium": sev_counts["medium"],
        "low": sev_counts["low"],
        "risk_avg": round(float(risk_avg), 2) if risk_avg is not None else None,
        "top_category": top_cat or "—"
    })

week = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)

# ----------------------------------------------------
# 2) Arvuta tuletatud näitajad
# ----------------------------------------------------
week["hi_crit"] = week["high"].fillna(0) + week["critical"].fillna(0)
week["hi_crit_pct"] = (week["hi_crit"] / week["alerts_total"]).round(4) * 100

# ----------------------------------------------------
# 3) Salvesta Excel ja TXT koond
# ----------------------------------------------------
today_iso = datetime.now().date().isoformat()

xlsx_out = PROC / f"nadal_koond_{today_iso}.xlsx"
with pd.ExcelWriter(xlsx_out) as xw:
    week.to_excel(xw, sheet_name="WeekSummary", index=False)

# TXT raport
txt_out = PROC / f"nadal_koond_{today_iso}.txt"
with open(txt_out, "w", encoding="utf-8") as fh:
    fh.write("SOC NÄDALA KOONDRAPORT\n")
    fh.write("-------------------------\n")
    fh.write(f"Periood: {week['date'].iloc[0]} – {week['date'].iloc[-1]}\n")
    fh.write(f"Päevi analüüsitud: {len(week)}\n\n")
    fh.write(f"Kokku alerts: {int(week['alerts_total'].sum()):,}\n")
    fh.write(f"High + Critical kokku: {int(week['hi_crit'].sum()):,}\n")
    if week['risk_avg'].notna().any():
        fh.write(f"Keskmine riskitase (päevade keskmine): {week['risk_avg'].dropna().mean():.2f}\n")
    # aktiivseim ja vaikseim päev
    max_row = week.loc[week['alerts_total'].idxmax()]
    min_row = week.loc[week['alerts_total'].idxmin()]
    fh.write(f"\nKõige aktiivsem päev: {max_row['date']} ({int(max_row['alerts_total']):,} alerti)\n")
    fh.write(f"Kõige rahulikum päev: {min_row['date']} ({int(min_row['alerts_total']):,} alerti)\n")
    # top kategooriad nädalas
    top_cats = week["top_category"].astype(str).str.lower().value_counts().head(3)
    if len(top_cats) > 0:
        fh.write("\nTOP 3 ohukategooriat:\n")
        for i, (k, v) in enumerate(top_cats.items(), 1):
            fh.write(f"{i}. {k} ({v} päeva tipp)\n")
    fh.write(f"\nTrendigraafik salvestatud: reports/nadal_trendid_{today_iso}.png\n")
    fh.write(f"Koondtabel: processed/nadal_koond_{today_iso}.xlsx\n")
    fh.write("-------------------------\n")

print(f"[OUT] XLSX: {xlsx_out}")
print(f"[OUT] TXT : {txt_out}")

# ----------------------------------------------------
# 4) Trendigraafik – alerts_total + hi_crit_pct
# ----------------------------------------------------
plt.figure(figsize=(10,6))

# Päevasumma (hall joon)
plt.plot(week["date"], week["alerts_total"], marker="o", label="Alerts kokku", color="#444444")

# High + Critical (oranž joon)
plt.plot(week["date"], week["hi_crit"], marker="o", label="High + Critical", color=SEV_COLORS["high"])\

# Protsent teisena y-teljel (kriitiline punasega)
ax = plt.gca()
ax2 = ax.twinx()
ax2.plot(week["date"], week["hi_crit_pct"], marker="o", linestyle="--", label="% High+Critical", color=SEV_COLORS["critical"])
ax2.set_ylabel("% High+Critical")

plt.title("Nädala trendid: alerts kokku vs High+Critical")
plt.xticks(rotation=45, ha="right")
plt.legend(loc="upper left")
plt.tight_layout()

out_png = REP / f"nadal_trendid_{today_iso}.png"
plt.savefig(out_png)
plt.close()

print(f"[OUT] PNG : {out_png}")
print("\n[OK] Nädala koondanalüüs valmis.")
