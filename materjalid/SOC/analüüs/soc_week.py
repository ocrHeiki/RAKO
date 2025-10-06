# soc_week.py — Nädala SOC analüüs (TXT, CSV, XLSX, DOCX + graafikud)
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

# --- Kaustad ---
BASE = Path.home() / "Documents" / "SOC"
RAW = BASE / "raw"
OUT = BASE / "tulemused"   # <— tulemused/
REP = BASE / "reports"
for d in (RAW, OUT, REP):
    d.mkdir(parents=True, exist_ok=True)

# Kui soovid piirata viimase 7 päevaga, pane siia 7 (None = kõik)
LIMIT_LAST_N = None

# --- Värvid ---
COLORS_SEV = {"low":"#0000FF","medium":"#FFFF00","high":"#FFA500","critical":"#FF0000"}
COLORS_ACTION = {"allow":"#33CC33","deny":"#CC3333","drop":"#3366CC","alert":"#FFCC00","reset-both":"#9933CC","reset-server":"#800080"}
COLORS_TYPE = {"malware":"#CC0033","vulnerability":"#FF3333","spyware":"#3399FF","suspicious":"#FFCC66","benign":"#66CC66"}
COLORS_CAT = {
    "command-and-control":"#CC0000","code-execution":"#FF6600","sql-injection":"#FF9933","brute-force":"#FFCC00",
    "dos":"#FFFF66","hacktool":"#9933CC","info-leak":"#66CCFF","spyware":"#3399FF","code-obfuscation":"#996633"
}

# --- Valepositiivid (kohanda) ---
FALSE_POSITIVE_CATEGORIES = {"dns.query.anomaly","port.scan","ssl.decrypt.failure","internal.backup.sync","trusted.update.service"}
FALSE_POSITIVE_NAMES = {"windows-update","office-cdn","zabbix-probe","okta-healthcheck","backup-job","scanner-internal"}

# --- Abid ---
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)  # dd.mm.yyyy
    if m: return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)    # yyyy-mm-dd
    return m2.group(0) if m2 else name

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

def stacked_severity(df_day_sev, outpath):
    if df_day_sev.empty: return
    plt.figure(figsize=(12,6))
    order = ["low","medium","high","critical"]
    for idx, sev in enumerate(order):
        bottom = df_day_sev[order[:idx]].sum(axis=1) if idx>0 else None
        plt.bar(df_day_sev.index, df_day_sev[sev], bottom=bottom, label=sev.title(), color=COLORS_SEV[sev])
    plt.title("Severity jaotus päevade lõikes (stacked)")
    plt.xticks(rotation=45, ha="right"); plt.legend(); plt.tight_layout(); plt.savefig(outpath); plt.close()

# --- DOCX abi ---
def add_image(doc: Document, img_path: Path, caption: str, width_in=6.0):
    if img_path.exists():
        p = doc.add_paragraph()
        run = p.add_run()
        run.add_picture(str(img_path), width=Inches(width_in))
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if caption:
            cap = doc.add_paragraph(caption)
            cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

def write_docx_report(title: str, txt_path: Path, images: list[tuple[Path, str]], out_docx: Path):
    doc = Document()
    doc.add_heading(title, level=1)
    if txt_path.exists():
        doc.add_heading("Tekstiline kokkuvõte", level=2)
        with open(txt_path, "r", encoding="utf-8") as fh:
            for line in fh:
                doc.add_paragraph(line.rstrip("\n"))
    if images:
        doc.add_heading("Graafikud ja visuaalid", level=2)
        for img, cap in images:
            add_image(doc, img, cap)
    out_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_docx))

def load_day(path: Path):
    df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    sev_col  = first_existing(df, ["Severity","severity"])
    risk_col = first_existing(df, ["Risk","risk","Risk Level","risk_level","Risk of app"])
    cat_col  = first_existing(df, ["thr_category","category","Threat Category"])
    type_col = first_existing(df, ["Threat/Content Type","threat/content type","Threat Type","threat_type"])
    act_col  = first_existing(df, ["Action","action"])
    name_col = first_existing(df, ["Threat/Content Name","Threat Name","content_name","threat_name"])
    src_col  = first_existing(df, ["Source address","Src","Source","src_ip","Source IP","src"])
    dst_col  = first_existing(df, ["Destination address","Dst","Destination","dst_ip","Destination IP","dst"])
    if sev_col:  df["sev_norm"]  = norm_lower(df[sev_col])
    if risk_col: df["risk_norm"] = pd.to_numeric(df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0).astype(int)
    if cat_col:  df["cat_norm"]  = norm_lower(df[cat_col])
    if type_col: df["type_norm"] = norm_lower(df[type_col])
    if act_col:  df["act_norm"]  = norm_lower(df[act_col])
    if name_col: df["tname_norm"]= df[name_col].astype(str).str.strip()
    if src_col:  df["src_norm"]  = df[src_col].astype(str).str.strip()
    if dst_col:  df["dst_norm"]  = df[dst_col].astype(str).str.strip()
    return df

def main():
    csv_files = sorted(RAW.glob("ThreatLog_*.csv"), key=lambda p: iso_from_filename(p.name))
    if not csv_files:
        print("[!] Ei leitud CSV-faile kaustas 'raw/'."); return
    if LIMIT_LAST_N:
        csv_files = csv_files[-LIMIT_LAST_N:]

    print(f"[i] Leiti {len(csv_files)} faili analüüsiks.")
    days = []
    for p in csv_files:
        df = load_day(p)
        date_iso = iso_from_filename(p.name)
        sev_counts = df["sev_norm"].value_counts() if "sev_norm" in df.columns else pd.Series(dtype=int)
        row = {"date": date_iso, "alerts_total": len(df),
               "low": int(sev_counts.get("low",0)), "medium": int(sev_counts.get("medium",0)),
               "high": int(sev_counts.get("high",0)), "critical": int(sev_counts.get("critical",0)),
               "risk_avg": float(df["risk_norm"].mean()) if "risk_norm" in df.columns and len(df)>0 else None}
        days.append((date_iso, df, row))

    week = pd.DataFrame([r for _,_,r in days]).sort_values("date").reset_index(drop=True)
    week["hi_crit"] = week["high"] + week["critical"]
    week["hi_crit_pct"] = (week["hi_crit"]/week["alerts_total"]*100).round(2)
    for col in ["alerts_total","hi_crit","hi_crit_pct"]:
        week[f"{col}_delta"] = week[col].diff().fillna(0).round(2)

    all_df = pd.concat([d for _,d,_ in days], ignore_index=True)
    sev_stack = week.set_index("date")[["low","medium","high","critical"]].fillna(0).astype(int)
    risk_hist = all_df["risk_norm"].astype(int).value_counts().sort_index() if "risk_norm" in all_df.columns else pd.Series(dtype=int)
    cat_counts = all_df["cat_norm"].value_counts() if "cat_norm" in all_df.columns else pd.Series(dtype=int)
    type_counts = all_df["type_norm"].value_counts() if "type_norm" in all_df.columns else pd.Series(dtype=int)
    act_counts = all_df["act_norm"].value_counts() if "act_norm" in all_df.columns else pd.Series(dtype=int)
    top_src = all_df["src_norm"].value_counts().head(10) if "src_norm" in all_df.columns else pd.Series(dtype=int)
    top_dst = all_df["dst_norm"].value_counts().head(10) if "dst_norm" in all_df.columns else pd.Series(dtype=int)

    # TOP5 iga severity ja risk
    top5_by_sev = {}
    if {"sev_norm","tname_norm"}.issubset(all_df.columns):
        g = all_df.groupby(["sev_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for sev in ["critical","high","medium","low"]:
            tmp = g[g["sev_norm"]==sev].sort_values("count", ascending=False).head(5)
            top5_by_sev[sev] = tmp[["tname_norm","cat_norm","count"]]
    top5_by_risk = {}
    if {"risk_norm","tname_norm"}.issubset(all_df.columns):
        gr = all_df.groupby(["risk_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for risk in sorted(gr["risk_norm"].dropna().unique()):
            tmp = gr[gr["risk_norm"]==risk].sort_values("count", ascending=False).head(5)
            top5_by_risk[int(risk)] = tmp[["tname_norm","cat_norm","count"]]

    today = datetime.now().date().isoformat()

    # CSV
    out_csv = OUT / f"week_summary_{today}.csv"
    week.to_csv(out_csv, index=False, encoding="utf-8")

    # XLSX
    out_xlsx = OUT / f"week_summary_{today}.xlsx"
    with pd.ExcelWriter(out_xlsx) as xw:
        week.to_excel(xw, sheet_name="DaySummary", index=False)
        sev_stack.reset_index().to_excel(xw, sheet_name="SeverityStack", index=False)
        if not risk_hist.empty: risk_hist.rename_axis("risk").reset_index(name="count").to_excel(xw, sheet_name="Risk", index=False)
        if not cat_counts.empty: cat_counts.rename_axis("category").reset_index(name="count").to_excel(xw, sheet_name="Categories", index=False)
        if not type_counts.empty: type_counts.rename_axis("type").reset_index(name="count").to_excel(xw, sheet_name="ThreatType", index=False)
        if not act_counts.empty: act_counts.rename_axis("action").reset_index(name="count").to_excel(xw, sheet_name="Action", index=False)
        if not top_src.empty: top_src.rename_axis("src_ip").reset_index(name="count").to_excel(xw, sheet_name="TopSrc", index=False)
        if not top_dst.empty: top_dst.rename_axis("dst_ip").reset_index(name="count").to_excel(xw, sheet_name="TopDst", index=False)
        for sev, df_top in top5_by_sev.items():
            if df_top is not None and len(df_top)>0: df_top.to_excel(xw, sheet_name=f"Top5_{sev.title()}", index=False)
        for risk, df_top in top5_by_risk.items():
            if df_top is not None and len(df_top)>0: df_top.to_excel(xw, sheet_name=f"Top5_Risk{risk}", index=False)

    # TXT
    out_txt = OUT / f"week_summary_{today}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("SOC NÄDALA KOONDARUANNE\n")
        f.write("=======================\n\n")
        f.write(f"Periood: {week['date'].iloc[0]} – {week['date'].iloc[-1]}\n")
        f.write(f"Päevi: {len(week)}\n\n")
        f.write(f"{'Kuupäev':<12} {'Kokku':>7} {'High+Crit':>10} {'%':>6} {'Δ Alerts':>10} {'Keskmine Risk':>15}\n")
        f.write("-"*70 + "\n")
        for _, r in week.iterrows():
            f.write(f"{r['date']:<12} {int(r['alerts_total']):>7} {int(r['hi_crit']):>10} {r['hi_crit_pct']:>6.1f} {r['alerts_total_delta']:>10.0f} {str(round(r['risk_avg'],2) if pd.notna(r['risk_avg']) else '-') :>15}\n")
        f.write("\nTOP kategooriad (nädal, TOP 10):\n")
        if not cat_counts.empty:
            for i, (k, v) in enumerate(cat_counts.head(10).items(), 1):
                f.write(f" {i}. {k} – {int(v)}\n")
        else:
            f.write(" – (puuduvad)\n")
        f.write("\nTOP 5 ohud iga severity sees (Threat/Content Name – Category – Count):\n")
        for sev in ["critical","high","medium","low"]:
            f.write(f"  [{sev.title()}]\n")
            df_top = top5_by_sev.get(sev)
            if df_top is None or len(df_top)==0:
                f.write("    – (puuduvad)\n"); continue
            for _, row in df_top.iterrows():
                f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")
        f.write("\nTOP 5 ohud iga riskitaseme sees (Threat/Content Name – Category – Count):\n")
        if len(top5_by_risk)==0:
            f.write("  – (puuduvad)\n")
        else:
            for risk in sorted(top5_by_risk.keys()):
                f.write(f"  [Risk {risk}]\n")
                df_top = top5_by_risk[risk]
                for _, row in df_top.iterrows():
                    f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

    # Graafikud
    plt.figure(figsize=(11,6))
    plt.plot(week["date"], week["alerts_total"], marker="o", label="Alerts kokku", color="#444444")
    plt.plot(week["date"], week["hi_crit"], marker="o", label="High+Critical", color=COLORS_SEV["high"])
    ax = plt.gca(); ax2 = ax.twinx()
    ax2.plot(week["date"], week["hi_crit_pct"], marker="o", linestyle="--", label="% High+Critical", color=COLORS_SEV["critical"])
    ax2.set_ylabel("% High+Critical")
    plt.title("Nädala trend: Alerts vs High+Critical"); plt.xticks(rotation=45, ha="right"); plt.tight_layout()
    trend_png = REP / f"week_trend_{today}.png"; plt.savefig(trend_png); plt.close()

    sev_png = REP / f"week_severity_stacked_{today}.png"; stacked_severity(sev_stack, sev_png)
    if not risk_hist.empty: bar(risk_hist, f"Riskitasemed (koond, 1–5) – {today}", REP / f"week_risk_hist_{today}.png")
    if not cat_counts.empty: bar(cat_counts.head(10), f"TOP 10 kategooriat (nädal) – {today}", REP / f"week_top_categories_{today}.png", colors=COLORS_CAT, rot=45)
    if not act_counts.empty: pie(act_counts, f"Action osakaal (nädal) – {today}", REP / f"week_action_pie_{today}.png")
    if not type_counts.empty: pie(type_counts, f"Threat/Content Type (nädal) – {today}", REP / f"week_threat_type_pie_{today}.png")
    if not top_src.empty: bar(top_src, f"TOP 10 allika IP (nädal) – {today}", REP / f"week_top_src_{today}.png", rot=45)
    if not top_dst.empty: bar(top_dst, f"TOP 10 sihtmärgi IP (nädal) – {today}", REP / f"week_top_dst_{today}.png", rot=45)

    # DOCX koond
    docx_path = OUT / f"week_summary_{today}.docx"
    images_week = [
        (trend_png, "Nädala trend: Alerts vs High+Critical"),
        (REP / f"week_severity_stacked_{today}.png", "Severity jaotus päevade lõikes (stacked)"),
        (REP / f"week_risk_hist_{today}.png", "Riskitasemete jaotus (histogramm)"),
        (REP / f"week_top_categories_{today}.png", "TOP 10 kategooriat (nädal)"),
        (REP / f"week_action_pie_{today}.png", "Action osakaal (pirukas)"),
        (REP / f"week_threat_type_pie_{today}.png", "Threat/Content Type (pirukas)"),
        (REP / f"week_top_src_{today}.png", "TOP 10 allika IP"),
        (REP / f"week_top_dst_{today}.png", "TOP 10 sihtmärgi IP"),
    ]
    # Filtreeri pildid, mis reaalselt olemas
    images_week = [(p, c) for p, c in images_week if p.exists()]
    doc = Document()
    doc.add_heading(f"SOC nädala koondaruanne — {week['date'].iloc[0]} … {week['date'].iloc[-1]}", level=1)
    doc.add_heading("Tekstiline kokkuvõte", level=2)
    with open(out_txt, "r", encoding="utf-8") as fh:
        for line in fh:
            doc.add_paragraph(line.rstrip("\n"))
    if images_week:
        doc.add_heading("Graafikud ja visuaalid", level=2)
        for img, cap in images_week:
            p = doc.add_paragraph(); run = p.add_run(); run.add_picture(str(img), width=Inches(6.0))
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            cap_p = doc.add_paragraph(cap); cap_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.save(str(docx_path))

    print("[OK] Nädala analüüs valmis.")
    print(f" - TXT : {out_txt}")
    print(f" - CSV : {out_csv}")
    print(f" - XLSX: {out_xlsx}")
    print(f" - DOCX: {docx_path}")
    print(f" - Graafikud: {REP}")

if __name__ == "__main__":
    main()
