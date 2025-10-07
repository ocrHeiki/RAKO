# soc_24h.py — SOC 24h analüüs v2.4
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.exceptions import PackageNotFoundError

BASE = Path.home() / "Documents" / "SOC"
RAW = BASE / "raw"
OUT = BASE / "tulemused"
REP = BASE / "reports"
for d in (RAW, OUT, REP):
    d.mkdir(parents=True, exist_ok=True)

COLORS_SEV = {"low": "#0000FF", "medium": "#FFFF00", "high": "#FFA500", "critical": "#FF0000"}
COLORS_ACTION = {"allow": "#33CC33", "deny": "#CC3333", "drop": "#3366CC", "alert": "#FFCC00","reset-both": "#9933CC", "reset-server": "#800080"}
COLORS_TYPE = {"malware": "#CC0033", "vulnerability": "#FF3333", "spyware": "#3399FF", "suspicious": "#FFCC66", "benign": "#66CC66"}
COLORS_CAT = {"command-and-control": "#CC0000", "code-execution": "#FF6600", "sql-injection": "#FF9933","brute-force": "#FFCC00", "dos": "#FFFF66", "hacktool": "#9933CC", "info-leak": "#66CCFF","spyware": "#3399FF", "code-obfuscation": "#996633"}

FALSE_POSITIVE_CATEGORIES = {"dns.query.anomaly", "port.scan", "ssl.decrypt.failure","internal.backup.sync", "trusted.update.service"}
FALSE_POSITIVE_NAMES = {"windows-update", "office-cdn", "zabbix-probe", "okta-healthcheck", "backup-job", "scanner-internal"}

def iso_from_filename(name: str) -> str:
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m: return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return m2.group(0) if m2 else datetime.now().date().isoformat()

def first_existing(df, names):
    for n in names:
        if n in df.columns: return n
    return None

def norm_lower(s):
    return s.astype(str).str.strip().str.lower()

def bar(series, title, outpath, colors=None, rot=0):
    if series is None or series.empty: return
    plt.figure(figsize=(10, 5))
    c = [colors.get(str(i).lower(), None) for i in series.index] if colors else None
    series.plot(kind="bar", color=c)
    plt.title(title); plt.xticks(rotation=rot, ha="right" if rot else "center")
    plt.tight_layout(); outpath.parent.mkdir(parents=True, exist_ok=True); plt.savefig(outpath); plt.close()

def pie(series, title, outpath):
    if series is None or series.empty: return
    plt.figure(figsize=(6, 6)); series.plot(kind="pie", autopct="%1.1f%%", startangle=90, ylabel="")
    plt.title(title); plt.tight_layout(); outpath.parent.mkdir(parents=True, exist_ok=True); plt.savefig(outpath); plt.close()

def add_image_safe(doc, img_path, caption="", width_in=6.0):
    try:
        if img_path.exists() and img_path.is_file():
            p = doc.add_paragraph(); run = p.add_run(); run.add_picture(str(img_path), width=Inches(width_in)); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if caption: cap = doc.add_paragraph(caption); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            doc.add_paragraph(f"(Märkus: graafik puudub) {img_path.name}")
    except (PackageNotFoundError, OSError) as e:
        doc.add_paragraph(f"(Märkus: ei saanud lisada {img_path.name} – {e})")

def main():
    csv_files = sorted(RAW.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not csv_files: print("[!] Ei leitud CSV-faile kaustas 'raw/'. Lõpetan."); return
    path = csv_files[0]; date_iso = iso_from_filename(path.name); print(f"[i] Analüüsitakse (uusim): {path.name} ({date_iso})")
    try: df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError: df = pd.read_csv(path, encoding="latin-1", low_memory=False)

    sev_col = first_existing(df, ["Severity", "severity"]); risk_col = first_existing(df, ["Risk", "risk", "Risk Level", "risk_level", "Risk of app"])
    cat_col = first_existing(df, ["thr_category", "category", "Threat Category"]); type_col = first_existing(df, ["Threat/Content Type", "threat/content type", "Threat Type", "threat_type"])
    act_col = first_existing(df, ["Action", "action"]); name_col = first_existing(df, ["Threat/Content Name", "Threat Name", "content_name", "threat_name"])
    src_col = first_existing(df, ["Source address", "Source", "src", "src_ip", "Source IP"]); dst_col = first_existing(df, ["Destination address", "Destination", "dst", "dst_ip", "Destination IP"])

    if sev_col: df["sev_norm"] = norm_lower(df[sev_col])
    if risk_col: df["risk_norm"] = pd.to_numeric(df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0).astype(int)
    if cat_col: df["cat_norm"] = norm_lower(df[cat_col])
    if type_col: df["type_norm"] = norm_lower(df[type_col])
    if act_col: df["act_norm"] = norm_lower(df[act_col])
    if name_col: df["tname_norm"] = df[name_col].astype(str).str.strip()
    if src_col: df["src_norm"] = df[src_col].astype(str).str.strip()
    if dst_col: df["dst_norm"] = df[dst_col].astype(str).str.strip()

    total = len(df)
    sev_counts = df["sev_norm"].value_counts() if "sev_norm" in df.columns else pd.Series(dtype=int)
    act_counts = df["act_norm"].value_counts() if "act_norm" in df.columns else pd.Series(dtype=int)
    type_counts = df["type_norm"].value_counts() if "type_norm" in df.columns else pd.Series(dtype=int)
    risk_avg = float(df["risk_norm"].mean()) if "risk_norm" in df.columns and total > 0 else None

    hi_crit = int(sev_counts.get("high", 0) + sev_counts.get("critical", 0)); hi_crit_pct = round(100 * hi_crit / total, 2) if total else 0.0
    top_cat = df["cat_norm"].value_counts().head(10) if "cat_norm" in df.columns else pd.Series(dtype=int)
    top_name = df["tname_norm"].value_counts().head(10) if "tname_norm" in df.columns else pd.Series(dtype=int)
    top_src = df["src_norm"].value_counts().head(10) if "src_norm" in df.columns else pd.Series(dtype=int)
    top_dst = df["dst_norm"].value_counts().head(10) if "dst_norm" in df.columns else pd.Series(dtype=int)

    top5_by_sev = {}
    if {"sev_norm","tname_norm"}.issubset(df.columns):
        g = df.groupby(["sev_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for sev in ["critical","high","medium","low"]:
            tmp = g[g["sev_norm"]==sev].sort_values("count", ascending=False).head(5); top5_by_sev[sev] = tmp[["tname_norm","cat_norm","count"]]
    top5_by_risk = {}
    if {"risk_norm","tname_norm"}.issubset(df.columns):
        gr = df.groupby(["risk_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for risk in sorted(gr["risk_norm"].dropna().unique()):
            tmp = gr[gr["risk_norm"]==risk].sort_values("count", ascending=False).head(5); top5_by_risk[int(risk)] = tmp[["tname_norm","cat_norm","count"]]

    fp_cat = pd.Series(dtype=int)
    if "cat_norm" in df.columns: fp_cat = df[df["cat_norm"].isin(FALSE_POSITIVE_CATEGORIES)]["cat_norm"].value_counts()
    fp_names = pd.Series(dtype=int)
    if "tname_norm" in df.columns: fp_names = df[df["tname_norm"].str.lower().isin(FALSE_POSITIVE_NAMES)]["tname_norm"].str.lower().value_counts()

    out_txt = OUT / f"24h_summary_{date_iso}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(f"SOC 24h ANALÜÜS — {path.name}\n")
        f.write("-" * 44 + "\n")
        f.write(f"Kuupäev: {date_iso}\n")
        f.write(f"Kokku logikirjeid: {total}\n")
        f.write(f"High+Critical kokku: {hi_crit} ({hi_crit_pct}%)\n")
        if risk_avg is not None: f.write(f"Keskmine Riskitase: {risk_avg:.2f}\n")

        if not sev_counts.empty:
            f.write("\nSeverity jaotus:\n")
            for sev, cnt in sev_counts.items(): f.write(f"  - {sev.title():<10}: {int(cnt)}\n")

        f.write("\nTOP 5 ohud iga severity sees (Threat/Content Name – Category – Count):\n")
        for sev in ["critical","high","medium","low"]:
            f.write(f"  [{sev.title()}]\n"); df_top = top5_by_sev.get(sev)
            if df_top is None or len(df_top)==0: f.write("    – (puuduvad)\n"); continue
            for _, row in df_top.iterrows(): f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

        f.write("\nTOP 5 ohud iga riskitaseme sees (Threat/Content Name – Category – Count):\n")
        if len(top5_by_risk)==0: f.write("  – (puuduvad)\n")
        else:
            for risk in sorted(top5_by_risk.keys()):
                f.write(f"  [Risk {risk}]\n"); df_top = top5_by_risk[risk]
                for _, row in df_top.iterrows(): f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

        f.write("\nSAGEDASED VALEPOSITIIVID (24h):\n")
        f.write("  Kategooriad:\n")
        if not fp_cat.empty:
            for i, (k, v) in enumerate(fp_cat.items(), 1): f.write(f"    {i}. {k} – {int(v)}\n")
        else: f.write("    – (puuduvad)\n")
        f.write("  Threat/Content Name:\n")
        if not fp_names.empty:
            for i, (k, v) in enumerate(fp_names.items(), 1): f.write(f"    {i}. {k} – {int(v)}\n")
        else: f.write("    – (puuduvad)\n")

        f.write("\nGraafikud salvestatakse kausta: reports/\n")

    out_csv = OUT / f"24h_summary_{date_iso}.csv"; koond_rows = []
    for label, series in [("Severity", sev_counts), ("Action", act_counts), ("ThreatType", type_counts),("TopCategory", top_cat), ("TopName", top_name), ("TopSrc", top_src), ("TopDst", top_dst)]:
        if series is not None and not series.empty:
            tmp = pd.DataFrame({"label": series.index.astype(str), "count": series.values}); tmp.insert(0, "metric", label); koond_rows.append(tmp)
    if koond_rows: pd.concat(koond_rows, ignore_index=True).to_csv(out_csv, index=False, encoding="utf-8")

    out_xlsx = OUT / f"24h_threats_{date_iso}.xlsx"
    with pd.ExcelWriter(out_xlsx) as xw:
        df.to_excel(xw, sheet_name="Raw", index=False)
        if not sev_counts.empty: sev_counts.rename_axis("Severity").reset_index(name="Count").to_excel(xw, sheet_name="Severity", index=False)
        if not act_counts.empty: act_counts.rename_axis("Action").reset_index(name="Count").to_excel(xw, sheet_name="Action", index=False)
        if not type_counts.empty: type_counts.rename_axis("Type").reset_index(name="Count").to_excel(xw, sheet_name="ThreatType", index=False)
        if not top_cat.empty: top_cat.rename_axis("Category").reset_index(name="Count").to_excel(xw, sheet_name="TopCategories", index=False)
        if not top_name.empty: top_name.rename_axis("ThreatName").reset_index(name="Count").to_excel(xw, sheet_name="TopThreatNames", index=False)
        if not top_src.empty: top_src.rename_axis("SrcIP").reset_index(name="Count").to_excel(xw, sheet_name="TopSrc", index=False)
        if not top_dst.empty: top_dst.rename_axis("DstIP").reset_index(name="Count").to_excel(xw, sheet_name="TopDst", index=False)
        for sev, dft in top5_by_sev.items():
            if dft is not None and len(dft)>0: dft.to_excel(xw, sheet_name=f"Top5_{sev.title()}", index=False)
        for risk, dft in top5_by_risk.items():
            if dft is not None and len(dft)>0: dft.to_excel(xw, sheet_name=f"Top5_Risk{risk}", index=False)

    bar(sev_counts, f"Severity jaotus (24h) – {date_iso}", REP / f"paev_severity_bar_{date_iso}.png", colors=COLORS_SEV)
    pie(sev_counts, f"Severity osakaal (24h) – {date_iso}", REP / f"paev_severity_pie_{date_iso}.png")
    bar(act_counts, f"Action jaotus (24h) – {date_iso}", REP / f"paev_action_bar_{date_iso}.png", colors=COLORS_ACTION, rot=45)
    pie(act_counts, f"Action osakaal (24h) – {date_iso}", REP / f"paev_action_pie_{date_iso}.png")
    pie(type_counts, f"Threat/Content Type (24h) – {date_iso}", REP / f"paev_threat_type_pie_{date_iso}.png")
    bar(top_cat, f"TOP kategooriad (24h) – {date_iso}", REP / f"paev_top_kategooriad_{date_iso}.png", colors=COLORS_CAT, rot=45)
    bar(top_src, f"TOP 10 allika IP (24h) – {date_iso}", REP / f"paev_top_src_{date_iso}.png", rot=45)
    bar(top_dst, f"TOP 10 sihtmärgi IP (24h) – {date_iso}", REP / f"paev_top_dst_{date_iso}.png", rot=45)

    try:
        docx_path = OUT / f"24h_summary_{date_iso}.docx"; doc = Document(); doc.add_heading(f"SOC 24h aruanne — {date_iso}", level=1)
        doc.add_heading("Tekstiline kokkuvõte", level=2)
        if out_txt.exists():
            with open(out_txt, "r", encoding="utf-8") as fh:
                for line in fh: doc.add_paragraph(line.rstrip("\n"))
        else: doc.add_paragraph("(TXT kokkuvõte puudub; kontrolli õigusi/teed)")
        doc.add_heading("Graafikud ja visuaalid", level=2)
        for img_path, caption in [
            (REP / f"paev_severity_bar_{date_iso}.png","Severity jaotus (tulbad)"),
            (REP / f"paev_severity_pie_{date_iso}.png","Severity osakaal (pirukas)"),
            (REP / f"paev_action_bar_{date_iso}.png","Action jaotus (tulbad)"),
            (REP / f"paev_action_pie_{date_iso}.png","Action osakaal (pirukas)"),
            (REP / f"paev_threat_type_pie_{date_iso}.png","Threat/Content Type pirukas"),
            (REP / f"paev_top_kategooriad_{date_iso}.png","TOP kategooriad (tulbad)"),
            (REP / f"paev_top_src_{date_iso}.png","TOP 10 allika IP"),
            (REP / f"paev_top_dst_{date_iso}.png","TOP 10 sihtmärgi IP"),
        ]: add_image_safe(doc, img_path, caption, width_in=6.0)
        docx_path.parent.mkdir(parents=True, exist_ok=True); doc.save(str(docx_path)); print(f"[OK] DOCX loodud: {docx_path}")
    except Exception as e:
        fallback = OUT / f"24h_summary_{date_iso}_FAILSAFE.docx"
        try:
            doc = Document(); doc.add_heading(f"SOC 24h aruanne — {date_iso}", level=1)
            doc.add_paragraph("Märkus: DOCX koostamisel esines viga, allpool detail:"); doc.add_paragraph(str(e))
            if out_txt.exists():
                doc.add_heading("Tekstiline kokkuvõte", level=2)
                with open(out_txt, "r", encoding="utf-8") as fh:
                    for line in fh: doc.add_paragraph(line.rstrip("\n"))
            doc.save(str(fallback)); print(f"[WARN] DOCX graafikuteta loodud (failsafe): {fallback}")
        except Exception as e2:
            print(f"[ERROR] DOCX loomine ebaõnnestus: {e2}")
    print("[OK] 24h analüüs valmis."); print(f" - TXT : {out_txt}"); print(f" - CSV : {out_csv}"); print(f" - XLSX: {out_xlsx}")
    print(f" - DOCX: {OUT / f'24h_summary_{date_iso}.docx'} või FAILSAFE"); print(f" - Graafikud: {REP}")
if __name__ == "__main__":
    main()
