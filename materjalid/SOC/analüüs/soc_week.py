# analuus_nadalakoond_csv_plus.py – Nädala koondanalüüs CSV-dest (täisgraafikute komplekt + TXT)
# Autor: <sinu nimi>
# Kasutus: py analuus_nadalakoond_csv_plus.py
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
    "reset-both": "#9933CC",
    "reset-server": "#800080",
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
# Abifunktsioonid
# -----------------------------
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)           # dd.mm.yyyy
    if m:
        return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)            # yyyy-mm-dd
    return m2.group(0) if m2 else name

def first_existing(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None

def norm_lower(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()

# -----------------------------
# Ühe CSV päeva koond
# -----------------------------
def analyze_one_csv(path: Path):
    df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    date_iso = iso_from_filename(path.name)

    # Veerud paindlikult
    sev_col = first_existing(df, ["Severity", "severity"])
    risk_col = first_existing(df, ["Risk", "risk", "Risk Level", "risk_level", "Risk of app"])
    cat_col = first_existing(df, ["thr_category", "category", "Threat Category"])
    type_col = first_existing(df, ["Threat/Content Type", "threat/content type", "Threat Type", "threat_type"])
    src_col = first_existing(df, ["Source address", "Src", "Source", "src_ip", "Source IP", "src"])
    dst_col = first_existing(df, ["Destination address", "Dst", "Destination", "dst_ip", "Destination IP", "dst"])

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

    total = len(df)
    sev_counts = df["sev_norm"].value_counts() if sev_col else pd.Series(dtype=int)
    hi_crit = int(sev_counts.get("high", 0) + sev_counts.get("critical", 0))
    hi_crit_pct = round(100 * hi_crit / total, 2) if total else 0.0
    risk_avg = df["risk_norm"].mean() if risk_col else None

    # tagasta koond + ka df hilisemaks nädalakogumikuks
    return {
        "date": date_iso,
        "df": df,
        "alerts_total": total,
        "sev_counts": sev_counts,
        "risk_avg": round(float(risk_avg), 2) if risk_avg is not None else None,
        "hi_crit": hi_crit,
        "hi_crit_pct": hi_crit_pct,
    }

# -----------------------------
# Joonistusabid
# -----------------------------
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

def stacked_severity(df_day_sev, outpath):
    """df_day_sev: index=date, columns=[low,medium,high,critical]"""
    plt.figure(figsize=(12,6))
    order = ["low","medium","high","critical"]
    for idx, sev in enumerate(order):
        bottom = df_day_sev[order[:idx]].sum(axis=1) if idx>0 else None
        plt.bar(df_day_sev.index, df_day_sev[sev], bottom=bottom, label=sev.title(), color=COLORS_SEV[sev])
    plt.title("Severity jaotus päevade lõikes (stacked)")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

# -----------------------------
# Peaosa
# -----------------------------
def main():
    csv_files = sorted(RAW.glob("ThreatLog_*.csv"))
    if not csv_files:
        print("[!] Ei leitud ühtegi CSV faili kaustast 'raw/'.")
        return

    print(f"[i] Leiti {len(csv_files)} faili.")
    daily = [analyze_one_csv(p) for p in csv_files]
    # päevade põhikoond
    day_rows = []
    for d in daily:
        day_rows.append({
            "date": d["date"],
            "alerts_total": d["alerts_total"],
            "high": int(d["sev_counts"].get("high", 0)),
            "critical": int(d["sev_counts"].get("critical", 0)),
            "medium": int(d["sev_counts"].get("medium", 0)),
            "low": int(d["sev_counts"].get("low", 0)),
            "hi_crit": d["hi_crit"],
            "hi_crit_pct": d["hi_crit_pct"],
            "risk_avg": d["risk_avg"],
        })
    week = pd.DataFrame(day_rows).sort_values("date").reset_index(drop=True)
    for col in ["alerts_total", "hi_crit", "hi_crit_pct"]:
        week[f"{col}_delta"] = week[col].diff().fillna(0).round(2)

    # Nädala koond (sum/agg) – severity, risk histogramm, kategooriad, type, src/dst
    # Koonda kõikide päevade df-id üheks
    all_df = pd.concat([d["df"] for d in daily], ignore_index=True)

    # Paindlik veerupüüdmine uuesti (kuna all_df võib tulla erinevate päevi)
    sev_col = first_existing(all_df, ["sev_norm"])
    risk_col = first_existing(all_df, ["risk_norm"])
    cat_col  = first_existing(all_df, ["cat_norm"])
    type_col = first_existing(all_df, ["type_norm"])
    src_col  = first_existing(all_df, ["src_norm"])
    dst_col  = first_existing(all_df, ["dst_norm"])

    # Severity stacked päevas
    sev_stack = week.set_index("date")[["low","medium","high","critical"]].fillna(0).astype(int)

    # Risk koondjaotus 1–5
    if risk_col:
        risk_hist = all_df[risk_col].astype(int).value_counts().sort_index()
    else:
        risk_hist = pd.Series(dtype=int)

    # TOP kategooriad (koond nädalas)
    if cat_col:
        top_cat = all_df[cat_col].value_counts().head(10)
    else:
        top_cat = pd.Series(dtype=int)

    # Threat type pirukas
    if type_col:
        type_counts = all_df[type_col].value_counts()
    else:
        type_counts = pd.Series(dtype=int)

    # TOP src/dst IP
    top_src = all_df[src_col].value_counts().head(10) if src_col else pd.Series(dtype=int)
    top_dst = all_df[dst_col].value_counts().head(10) if dst_col else pd.Series(dtype=int)

    # -----------------------------
    # Salvestused
    # -----------------------------
    today = datetime.now().date().isoformat()
    # tabelid
    out_csv  = PROC / f"nadalakoond_{today}.csv"
    out_xlsx = PROC / f"nadalakoond_{today}.xlsx"
    week.to_csv(out_csv, index=False, encoding="utf-8")
    with pd.ExcelWriter(out_xlsx) as xw:
        week.to_excel(xw, sheet_name="DaySummary", index=False)
        sev_stack.reset_index().to_excel(xw, sheet_name="SeverityStack", index=False)
        if not risk_hist.empty:
            risk_hist.rename_axis("risk").reset_index(name="count").to_excel(xw, sheet_name="Risk", index=False)
        if not top_cat.empty:
            top_cat.rename_axis("category").reset_index(name="count").to_excel(xw, sheet_name="TopCategories", index=False)
        if not type_counts.empty:
            type_counts.rename_axis("type").reset_index(name="count").to_excel(xw, sheet_name="ThreatType", index=False)
        if not top_src.empty:
            top_src.rename_axis("src_ip").reset_index(name="count").to_excel(xw, sheet_name="TopSrc", index=False)
        if not top_dst.empty:
            top_dst.rename_axis("dst_ip").reset_index(name="count").to_excel(xw, sheet_name="TopDst", index=False)

    # txt raport
    out_txt = PROC / f"nadalakoond_{today}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("SOC NÄDALA KOONDARUANNE\n")
        f.write("=======================\n\n")
        f.write(f"Periood: {week['date'].iloc[0]} – {week['date'].iloc[-1]}\n")
        f.write(f"Analüüsitud päevi: {len(week)}\n\n")
        f.write(f"{'Kuupäev':<12} {'Kokku':>7} {'High+Crit':>10} {'%':>6} {'Δ Alerts':>10} {'Keskmine Risk':>15}\n")
        f.write("-"*70 + "\n")
        for _, r in week.iterrows():
            f.write(f"{r['date']:<12} {int(r['alerts_total']):>7} {int(r['hi_crit']):>10} {r['hi_crit_pct']:>6.1f} {r['alerts_total_delta']:>10.0f} {str(r['risk_avg'] if r['risk_avg'] is not None else '-') :>15}\n")
        f.write("\nTOP kategooriad (nädal):\n")
        if not top_cat.empty:
            for i, (k, v) in enumerate(top_cat.items(), 1):
                f.write(f" {i}. {k} – {int(v)}\n")
        else:
            f.write(" – (puuduvad)\n")
        f.write("\nMärkused:\n")
        f.write("- Positiivne Δ tähendab tõusu võrreldes eelmise päevaga.\n")
        f.write("- % on High+Critical osakaal päevases koguarvus.\n")
        f.write("- Risk keskmine arvutatakse olemasolu korral (Risk veerust).\n")

    # -----------------------------
    # Graafikud
    # -----------------------------
    # Trend (alerts + Hi+Crit + %)
    plt.figure(figsize=(11,6))
    plt.plot(week["date"], week["alerts_total"], marker="o", label="Alerts kokku", color="#444444")
    plt.plot(week["date"], week["hi_crit"], marker="o", label="High+Critical", color=COLORS_SEV["high"])
    ax = plt.gca(); ax2 = ax.twinx()
    ax2.plot(week["date"], week["hi_crit_pct"], marker="o", linestyle="--", label="% High+Critical", color=COLORS_SEV["critical"])
    ax2.set_ylabel("% High+Critical")
    plt.title("Nädala trend: Alerts vs High+Critical")
    plt.xticks(rotation=45, ha="right"); plt.tight_layout()
    trend_png = REP / f"nadal_trendid_{today}.png"
    plt.savefig(trend_png); plt.close()

    # Stacked severity per day
    sev_png = REP / f"nadal_severity_stacked_{today}.png"
    stacked_severity(sev_stack, sev_png)

    # Risk histogram (koond)
    if not risk_hist.empty:
        bar(risk_hist, "Riskitasemed (koond, 1–5)", REP / f"nadal_riskijaotus_{today}.png", colors=None, rot=0)

    # Top categories (koond, TOP10)
    if not top_cat.empty:
        bar(top_cat, "TOP kategooriad (nädal, TOP10)", REP / f"nadal_top_kategooriad_{today}.png", colors=COLORS_CAT, rot=45)

    # Threat type pie
    if not type_counts.empty:
        pie(type_counts, "Threat/Content Type osakaal (nädal)", REP / f"nadal_threat_type_pirukas_{today}.png")

    # TOP src/dst
    if not top_src.empty:
        bar(top_src, "TOP 10 allika IP (nädal)", REP / f"nadal_top_src_{today}.png", rot=45)
    if not top_dst.empty:
        bar(top_dst, "TOP 10 sihtmärk IP (nädal)", REP / f"nadal_top_dst_{today}.png", rot=45)

    # KONSOOLI kokkuvõte
    print(f"[OUT] CSV : {out_csv}")
    print(f"[OUT] XLSX: {out_xlsx}")
    print(f"[OUT] TXT : {out_txt}")
    print(f"[OUT] PNG : {trend_png}")
    print(f"[OUT] PNG : {sev_png}")
    if not risk_hist.empty: print(f"[OUT] PNG : {REP / f'nadal_riskijaotus_{today}.png'}")
    if not top_cat.empty:   print(f"[OUT] PNG : {REP / f'nadal_top_kategooriad_{today}.png'}")
    if not type_counts.empty: print(f"[OUT] PNG : {REP / f'nadal_threat_type_pirukas_{today}.png'}")
    if not top_src.empty:   print(f"[OUT] PNG : {REP / f'nadal_top_src_{today}.png'}")
    if not top_dst.empty:   print(f"[OUT] PNG : {REP / f'nadal_top_dst_{today}.png'}")
    print("\n[OK] Nädala analüüs (CSV-põhine) valmis.")

if __name__ == "__main__":
    main()
