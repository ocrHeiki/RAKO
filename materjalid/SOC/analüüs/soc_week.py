# ==============================================================
#  SOC 7 päeva analüüs – v2.8.10
#  - Kaasab AINULT need CSV-d, mille sees on 5–7 päeva logi (välistab 24h failid)
#  - Vaikimisi liidab mitu sobivat nädalafaili (MERGE_MULTIPLE_MATCHES = True),
#    et võrdlus (esimene pool vs teine pool) oleks sisuline
#  - TXT, CSV, XLSX ja DOCX (tekst + graafikud + võrdlus)
#  - Graafikud kausta reports/
#  - Periood/allikad leitakse eelisena LOGI SEEST (min…max)
#  - Eristavad pealkirjamärgid: ◆ trend, ■ bar/stacked, ▲ donut, ● TOP/teksti-plokid
# ==============================================================

from pathlib import Path
from datetime import datetime, date
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.exceptions import PackageNotFoundError

# --- Kaustad ---
BASE = Path.home() / "Documents" / "SOC"
RAW  = BASE / "raw"
OUT  = BASE / "tulemused"
REP  = BASE / "reports"
for d in (RAW, OUT, REP):
    d.mkdir(parents=True, exist_ok=True)

# --- Seaded ---
LIMIT_LAST_N = 20                 # vaata korraga kuni 20 viimast CSV-d (enne filtreerimist)
WEEK_MIN_DAYS = 5
WEEK_MAX_DAYS = 7
MERGE_MULTIPLE_MATCHES = True     # True = kasuta kõiki sobivaid nädalafaile (võrdluseks parem)
MIN_FILES_FOR_COMPARISON = 2

# --- Värvikaardid ---
COLORS_SEV    = {"low":"#0000FF","medium":"#FFFF00","high":"#FFA500","critical":"#FF0000"}
COLORS_ACTION = {"allow":"#33CC33","deny":"#CC3333","drop":"#3366CC","alert":"#FFCC00","reset-both":"#9933CC","reset-server":"#800080"}
COLORS_TYPE   = {"malware":"#CC0033","vulnerability":"#FF3333","spyware":"#3399FF","suspicious":"#FFCC66","benign":"#66CC66"}
COLORS_CAT    = {"command-and-control":"#CC0000","code-execution":"#FF6600","sql-injection":"#FF9933","brute-force":"#FFCC00",
                 "dos":"#FFFF66","hacktool":"#9933CC","info-leak":"#66CCFF","spyware":"#3399FF","code-obfuscation":"#996633"}

FALSE_POSITIVE_CATEGORIES = {"dns.query.anomaly","port.scan","ssl.decrypt.failure","internal.backup.sync","trusted.update.service"}
FALSE_POSITIVE_NAMES      = {"windows-update","office-cdn","zabbix-probe","okta-healthcheck","backup-job","scanner-internal"}

# --- Ajaveeru kandidaadid ---
TIME_COL_CANDIDATES = [
    "Time Generated","Receive Time","Event Time","EventTime","timestamp",
    "Timestamp","Generated Time","Log Time","time","Date","date"
]

# --- Abid ---
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m: return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return m2.group(0) if m2 else datetime.now().date().isoformat()

def first_existing(df, names):
    for n in names:
        if n in df.columns: return n
    return None

def norm_lower(s: pd.Series) -> pd.Series:
    return s.astype(str).str.strip().str.lower()

def extract_date_range(df: pd.DataFrame):
    """Tagasta (date_from, date_to) kui ajaveerust õnnestub parsimine; vastasel juhul (None, None)."""
    col = first_existing(df, TIME_COL_CANDIDATES)
    if not col: return None, None
    ts = pd.to_datetime(df[col], errors="coerce", utc=True).dropna()
    if ts.empty: return None, None
    return ts.min().date().isoformat(), ts.max().date().isoformat()

def span_days(d_from: str|None, d_to: str|None) -> int|None:
    if not d_from or not d_to: return None
    a = date.fromisoformat(d_from); b = date.fromisoformat(d_to)
    return (b - a).days + 1  # kaasav vahemik

def bar(series, title, outpath, colors=None, rot=0):
    if series is None or series.empty: return
    plt.figure(figsize=(10,5))
    c = [colors.get(str(i).lower(), "#888888") for i in series.index] if colors else "#888888"
    series.plot(kind="bar", color=c)
    plt.title(title); plt.xticks(rotation=rot, ha="right" if rot else "center")
    plt.tight_layout(); outpath.parent.mkdir(parents=True, exist_ok=True); plt.savefig(outpath); plt.close()

def pie_donut(series, title, outpath, colors=None, min_pct_label: float = 3.0):
    if series is None or series.empty: return
    labels = series.index.astype(str); values = series.values
    total  = float(values.sum()) if values.sum() else 1.0
    c = [colors.get(str(lbl).lower(), "#888888") for lbl in labels] if colors else None
    plt.figure(figsize=(8,6))
    def _fmt(pct): return f"{pct:.1f}%" if pct >= min_pct_label else ""
    wedges, _, _ = plt.pie(values, startangle=90, labels=None, autopct=_fmt, pctdistance=0.75,
                           colors=c, wedgeprops={"width":0.35})
    legend_labels = [f"{lbl} — {int(val)} ({(val/total*100):.1f}%)" for lbl,val in zip(labels, values)]
    plt.legend(wedges, legend_labels, loc="center left", bbox_to_anchor=(1,0.5), frameon=False)
    plt.title(title); plt.tight_layout(); outpath.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(outpath, bbox_inches="tight"); plt.close()

def stacked_severity(df_day_sev, outpath):
    if df_day_sev.empty: return
    plt.figure(figsize=(12,6))
    order = ["low","medium","high","critical"]
    for idx, sev in enumerate(order):
        bottom = df_day_sev[order[:idx]].sum(axis=1) if idx>0 else None
        plt.bar(df_day_sev.index, df_day_sev[sev], bottom=bottom, label=sev.title(), color=COLORS_SEV[sev])
    plt.title("■ Severity jaotus päevade lõikes (stacked)")
    plt.xticks(rotation=45, ha="right"); plt.legend(); plt.tight_layout(); plt.savefig(outpath); plt.close()

def add_image_safe(doc: Document, img_path: Path, caption: str = "", width_in=6.0):
    try:
        if img_path.exists() and img_path.is_file():
            p = doc.add_paragraph(); run = p.add_run()
            run.add_picture(str(img_path), width=Inches(width_in)); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if caption:
                cap = doc.add_paragraph(caption); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            doc.add_paragraph(f"(Märkus: graafik puudub) {img_path.name}")
    except (PackageNotFoundError, OSError) as e:
        doc.add_paragraph(f"(Märkus: ei saanud lisada {img_path.name} – {e})")

def load_day(path: Path):
    try:
        df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="latin-1", low_memory=False)
    sev_col  = first_existing(df, ["Severity","severity"])
    risk_col = first_existing(df, ["Risk","risk","Risk Level","risk_level","Risk of app"])
    cat_col  = first_existing(df, ["thr_category","category","Threat Category"])
    type_col = first_existing(df, ["Threat/Content Type","threat/content type","Threat Type","threat_type"])
    act_col  = first_existing(df, ["Action","action"])
    name_col = first_existing(df, ["Threat/Content Name","Threat Name","content_name","threat_name"])
    src_col  = first_existing(df, ["Source address","Src","Source","src_ip","Source IP","src"])
    dst_col  = first_existing(df, ["Destination address","Dst","Destination","dst_ip","Destination IP","dst"])
    if sev_col:  df["sev_norm"]   = norm_lower(df[sev_col])
    if risk_col: df["risk_norm"]  = pd.to_numeric(df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0).astype(int)
    if cat_col:  df["cat_norm"]   = norm_lower(df[cat_col])
    if type_col: df["type_norm"]  = norm_lower(df[type_col])
    if act_col:  df["act_norm"]   = norm_lower(df[act_col])
    if name_col: df["tname_norm"] = df[name_col].astype(str).str.strip()
    if src_col:  df["src_norm"]   = df[src_col].astype(str).str.strip()
    if dst_col:  df["dst_norm"]   = df[dst_col].astype(str).str.strip()
    return df

# --- Main ---
def main():
    csv_files = sorted(RAW.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not csv_files:
        print("[!] Ei leitud CSV-faile kaustas 'raw/'."); return
    if LIMIT_LAST_N: csv_files = csv_files[:LIMIT_LAST_N]

    # 1) Filtreeri ainult "nädalafailid" (5–7 päeva ulatus logis)
    qualified = []
    for p in csv_files:
        df = load_day(p)
        d_from, d_to = extract_date_range(df)
        dayspan = span_days(d_from, d_to)
        if dayspan is not None and WEEK_MIN_DAYS <= dayspan <= WEEK_MAX_DAYS:
            qualified.append((p, d_from, d_to, dayspan))

    if not qualified:
        print(f"[!] Ei leidnud ühtegi CSV-d, mille sees oleks {WEEK_MIN_DAYS}–{WEEK_MAX_DAYS} päeva andmeid. Lõpetan.")
        return

    # 2) Kasuta mitut sobivat nädalafaili (vaikimisi), et võrdlus oleks sisuline
    if not MERGE_MULTIPLE_MATCHES:
        qualified = [max(qualified, key=lambda t: t[0].stat().st_mtime)]

    # 3) Valitud failid vanem -> uuem (parem kuvada kronoloogiliselt)
    qualified.sort(key=lambda t: t[0].stat().st_mtime)

    # 4) Lae andmed ja koosta päevaread (päev = faili lõppkuupäev)
    days = []
    for (p, d_from, d_to, dayspan) in qualified:
        df = load_day(p)
        di = d_to or d_from or iso_from_filename(p.name)
        sev_counts = df["sev_norm"].value_counts() if "sev_norm" in df.columns else pd.Series(dtype=int)
        row = {
            "date": di,
            "date_from": d_from or di,
            "date_to": d_to or di,
            "alerts_total": len(df),
            "low": int(sev_counts.get("low",0)),
            "medium": int(sev_counts.get("medium",0)),
            "high": int(sev_counts.get("high",0)),
            "critical": int(sev_counts.get("critical",0)),
            "risk_avg": float(df["risk_norm"].mean()) if "risk_norm" in df.columns and len(df)>0 else None,
            "source_file": p.name,
            "span_days": dayspan
        }
        days.append((di, df, row))

    week = pd.DataFrame([r for _,_,r in days]).sort_values("date").reset_index(drop=True)
    if week.empty:
        print("[!] Nädala koond tühi."); return

    week["hi_crit"]     = week["high"] + week["critical"]
    week["hi_crit_pct"] = (week["hi_crit"]/week["alerts_total"]*100).round(2)
    for col in ["alerts_total","hi_crit","hi_crit_pct"]:
        week[f"{col}_delta"] = week[col].diff().fillna(0).round(2)

    period_from = week["date_from"].min()
    period_to   = week["date_to"].max()

    all_df     = pd.concat([d for _,d,_ in days], ignore_index=True) if days else pd.DataFrame()
    sev_stack  = week.set_index("date")[["low","medium","high","critical"]].fillna(0).astype(int)
    risk_hist  = all_df["risk_norm"].astype(int).value_counts().sort_index() if "risk_norm" in all_df.columns else pd.Series(dtype=int)
    cat_counts = all_df["cat_norm"].value_counts()  if "cat_norm"  in all_df.columns else pd.Series(dtype=int)
    type_counts= all_df["type_norm"].value_counts() if "type_norm" in all_df.columns else pd.Series(dtype=int)
    act_counts = all_df["act_norm"].value_counts()  if "act_norm"  in all_df.columns else pd.Series(dtype=int)
    top_src    = all_df["src_norm"].value_counts().head(10) if "src_norm" in all_df.columns else pd.Series(dtype=int)
    top_dst    = all_df["dst_norm"].value_counts().head(10) if "dst_norm" in all_df.columns else pd.Series(dtype=int)

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

    low_df   = all_df[all_df["sev_norm"]=="low"] if "sev_norm" in all_df.columns else pd.DataFrame()
    low_cat  = low_df["cat_norm"].value_counts().head(10)   if "cat_norm"   in low_df.columns and not low_df.empty else pd.Series(dtype=int)
    low_tn   = low_df["tname_norm"].value_counts().head(10) if "tname_norm" in low_df.columns and not low_df.empty else pd.Series(dtype=int)
    low_src  = low_df["src_norm"].value_counts().head(20)   if "src_norm"   in low_df.columns and not low_df.empty else pd.Series(dtype=int)

    # --- Võrdlused (ainult siis kui sobivaid nädalafaile on vähemalt 2) ---
    cat_up = cat_down = src_up = src_down = dst_up = dst_down = pd.Series(dtype=int)
    do_comparison = len(days) >= MIN_FILES_FOR_COMPARISON
    if do_comparison:
        mid = len(days)//2
        first_df = pd.concat([d for _,d,_ in days[:mid]], ignore_index=True)
        last_df  = pd.concat([d for _,d,_ in days[mid:]], ignore_index=True)
        prev_cat_counts = first_df["cat_norm"].value_counts() if "cat_norm" in first_df.columns else pd.Series(dtype=int)
        prev_src_counts = first_df["src_norm"].value_counts() if "src_norm" in first_df.columns else pd.Series(dtype=int)
        prev_dst_counts = first_df["dst_norm"].value_counts() if "dst_norm" in first_df.columns else pd.Series(dtype=int)
        curr_cat_counts = last_df["cat_norm"].value_counts() if "cat_norm" in last_df.columns else pd.Series(dtype=int)
        curr_src_counts = last_df["src_norm"].value_counts() if "src_norm" in last_df.columns else pd.Series(dtype=int)
        curr_dst_counts = last_df["dst_norm"].value_counts() if "dst_norm" in last_df.columns else pd.Series(dtype=int)
        def top5_diff(curr, prev):
            idx = set(curr.index.astype(str)).union(set(prev.index.astype(str)))
            c = curr.reindex(idx, fill_value=0).astype(int)
            p = prev.reindex(idx, fill_value=0).astype(int)
            diff = (c - p).sort_values(ascending=False)
            return diff.head(5), diff.tail(5)
        cat_up, cat_down = top5_diff(curr_cat_counts, prev_cat_counts)
        src_up, src_down = top5_diff(curr_src_counts, prev_src_counts)
        dst_up, dst_down = top5_diff(curr_dst_counts, prev_dst_counts)

    # --- CSV ---
    today = datetime.now().date().isoformat()
    out_csv = OUT / f"week_summary_{today}.csv"
    week.to_csv(out_csv, index=False, encoding="utf-8")

    # --- XLSX ---
    out_xlsx = OUT / f"week_summary_{today}.xlsx"
    with pd.ExcelWriter(out_xlsx) as xw:
        week.to_excel(xw, sheet_name="DaySummary", index=False)
        sev_stack.reset_index().to_excel(xw, sheet_name="SeverityStack", index=False)
        if not risk_hist.empty: risk_hist.rename_axis("Risk").reset_index(name="Count").to_excel(xw, sheet_name="Risk", index=False)
        if not cat_counts.empty: cat_counts.rename_axis("Category").reset_index(name="Count").to_excel(xw, sheet_name="Categories", index=False)
        if not type_counts.empty: type_counts.rename_axis("Type").reset_index(name="Count").to_excel(xw, sheet_name="ThreatType", index=False)
        if not act_counts.empty: act_counts.rename_axis("Action").reset_index(name="Count").to_excel(xw, sheet_name="Action", index=False)
        if not top_src.empty: top_src.rename_axis("SrcIP").reset_index(name="Count").to_excel(xw, sheet_name="TopSrc", index=False)
        if not top_dst.empty: top_dst.rename_axis("DstIP").reset_index(name="Count").to_excel(xw, sheet_name="TopDst", index=False)
        for sev, df_top in top5_by_sev.items():
            if df_top is not None and len(df_top)>0: df_top.to_excel(xw, sheet_name=f"Top5_{sev.title()}", index=False)
        for risk, df_top in top5_by_risk.items():
            if df_top is not None and len(df_top)>0: df_top.to_excel(xw, sheet_name=f"Top5_Risk{risk}", index=False)
        if not low_cat.empty:  low_cat.rename_axis("low_category").reset_index(name="count").to_excel(xw, sheet_name="LOW_TopCategories", index=False)
        if not low_tn.empty:   low_tn.rename_axis("low_tname").reset_index(name="count").to_excel(xw, sheet_name="LOW_TopThreatNames", index=False)
        if not low_src.empty:  low_src.rename_axis("low_src_ip").reset_index(name="count").to_excel(xw, sheet_name="LOW_TopSrc", index=False)

    # --- TXT ---
    out_txt = OUT / f"week_summary_{today}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write("SOC NÄDALA KOONDARUANNE\n")
        f.write("=======================\n\n")
        f.write(f"Periood: {period_from} – {period_to}\n")
        f.write(f"Kasutatud sobivaid nädalafaile: {len(days)} tk (iga fail {WEEK_MIN_DAYS}–{WEEK_MAX_DAYS} päeva)\n")
        if not do_comparison:
            f.write("Märkus: võrdlusblokk jäeti vahele (sobivaid nädalafaile alla 2).\n")

        f.write("\n◆ Päevade ülevaade:\n")
        f.write(f"{'Kuupäev':<12} {'Kokku':>7} {'High+Crit':>10} {'%':>6} {'Δ Alerts':>10} {'Keskmine Risk':>15}\n")
        f.write("-"*70 + "\n")
        for _, r in week.iterrows():
            f.write(f"{r['date']:<12} {int(r['alerts_total']):>7} {int(r['hi_crit']):>10} {r['hi_crit_pct']:>6.1f} {r['alerts_total_delta']:>10.0f} {str(round(r['risk_avg'],2) if pd.notna(r['risk_avg']) else '-') :>15}\n")

        f.write("\n● TOP kategooriad (nädal, TOP 10):\n")
        if not cat_counts.empty:
            for i, (k, v) in enumerate(cat_counts.head(10).items(), 1):
                f.write(f" {i}. {k} – {int(v)}\n")
        else:
            f.write(" – (puuduvad)\n")

        f.write("\n● LOW-severity fookus (TOP-id):\n")
        if not low_cat.empty:
            f.write("  ● TOP Low-kategooriad:\n")
            for i,(k,v) in enumerate(low_cat.items(),1):
                f.write(f"   {i}. {k} – {int(v)}\n")
        else:
            f.write("  ● TOP Low-kategooriad: – (puuduvad)\n")
        if not low_tn.empty:
            f.write("  ● TOP Low Threat/Content Name:\n")
            for i,(k,v) in enumerate(low_tn.items(),1):
                f.write(f"   {i}. {k} – {int(v)}\n")
        else:
            f.write("  ● TOP Low Threat/Content Name: – (puuduvad)\n")
        if not low_src.empty:
            f.write("  ● TOP Low allika IP:\n")
            for i,(k,v) in enumerate(low_src.items(),1):
                f.write(f"   {i}. {k} – {int(v)}\n")
        else:
            f.write("  ● TOP Low allika IP: – (puuduvad)\n")

        f.write("\n● TOP 5 ohud iga severity sees (Threat/Content Name – Category – Count):\n")
        for sev in ["critical","high","medium","low"]:
            f.write(f"  [{sev.title()}]\n")
            df_top = top5_by_sev.get(sev)
            if df_top is None or len(df_top)==0:
                f.write("    – (puuduvad)\n"); continue
            for _, row in df_top.iterrows():
                f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

        f.write("\n● TOP 5 ohud iga riskitaseme sees (Threat/Content Name – Category – Count):\n")
        if len(top5_by_risk)==0:
            f.write("  – (puuduvad)\n")
        else:
            for risk in sorted(top5_by_risk.keys()):
                f.write(f"  [Risk {risk}]\n")
                df_top = top5_by_risk[risk]
                for _, row in df_top.iterrows():
                    f.write(f"    - {row['tname_norm']} – {str(row['cat_norm'])} – {int(row['count'])}\n")

    # --- Graafikud ---
    trend_png = REP / f"week_trend_{today}.png"
    fig, ax1 = plt.subplots(figsize=(11,6))
    ax1.plot(week["date"], week["alerts_total"], marker="o", label="Alertide koguarv", color="#444444")
    ax1.plot(week["date"], week["high"], marker="o", label="High", color=COLORS_SEV["high"])
    ax2 = ax1.twinx()
    ax2.plot(week["date"], week["hi_crit_pct"], marker="o", linestyle="--", label="% High+Critical", color=COLORS_SEV["critical"])
    ax1.set_title("◆ Nädala trend: Alerts vs High+Critical")
    ax2.set_ylabel("% High+Critical")
    fig.legend(loc="upper right")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout(); plt.savefig(trend_png); plt.close()

    sev_png = REP / f"week_severity_stacked_{today}.png"; stacked_severity(sev_stack, sev_png)
    if not risk_hist.empty: bar(risk_hist, f"■ Riskitasemed (koond) – {today}", REP / f"week_risk_hist_{today}.png")
    if not cat_counts.empty: bar(cat_counts.head(10), f"■ TOP 10 kategooriat (nädal) – {today}", REP / f"week_top_categories_{today}.png", colors=COLORS_CAT, rot=45)
    if not act_counts.empty:
        pie_donut(act_counts, f"▲ Action osakaal (nädal, donut) – {today}", REP / f"week_action_pie_{today}.png", colors=COLORS_ACTION)
        bar(act_counts, f"■ Action jaotus (nädal) – {today}", REP / f"week_action_bar_{today}.png", colors=COLORS_ACTION, rot=45)
    if not type_counts.empty:
        pie_donut(type_counts, f"▲ Threat/Content Type (nädal, donut) – {today}", REP / f"week_threat_type_pie_{today}.png", colors=COLORS_TYPE)
    if not top_src.empty: bar(top_src, f"■ TOP 10 allika IP (nädal) – {today}", REP / f"week_top_src_{today}.png", rot=45)
    if not top_dst.empty: bar(top_dst, f"■ TOP 10 sihtmärgi IP (nädal) – {today}", REP / f"week_top_dst_{today}.png", rot=45)

    # --- DOCX ---
    docx_path = OUT / f"week_summary_{today}.docx"
    doc = Document()
    doc.add_heading(f"SOC nädala koondaruanne — {period_from} … {period_to}", level=1)

    doc.add_heading("● Allikafailid (kronoloogiliselt, vanem → uuem)", level=2)
    for _, _df, row in days:
        doc.add_paragraph(f"{row['date_from']} … {row['date_to']}: {row['source_file']}")

    doc.add_heading("● Tekstiline kokkuvõte", level=2)
    with open(out_txt, "r", encoding="utf-8") as fh:
        for line in fh:
            doc.add_paragraph(line.rstrip("\n"))

    doc.add_heading("● Graafikud ja visuaalid", level=2)
    for p, cap in [
        (trend_png, "◆ Nädala trend: Alerts vs High+Critical"),
        (sev_png, "■ Severity jaotus päevade lõikes (stacked)"),
        (REP / f"week_risk_hist_{today}.png", "■ Riskitasemete jaotus (tulbad)"),
        (REP / f"week_action_bar_{today}.png", "■ Action jaotus (tulbad)"),
        (REP / f"week_action_pie_{today}.png", "▲ Action osakaal (donut)"),
        (REP / f"week_threat_type_pie_{today}.png", "▲ Threat/Content Type (donut)"),
        (REP / f"week_top_categories_{today}.png", "■ TOP 10 kategooriat"),
        (REP / f"week_top_src_{today}.png", "■ TOP 10 allika IP"),
        (REP / f"week_top_dst_{today}.png", "■ TOP 10 sihtmärgi IP"),
    ]:
        add_image_safe(doc, p, cap, width_in=6.0)

    if do_comparison:
        doc.add_heading("● Võrdlus (esimene pool vs teine pool)", level=2)
        def write_diff(par_title, up, down):
            doc.add_paragraph(par_title)
            if up is not None and not up.empty:
                doc.add_paragraph("↑ Tõusud:")
                for i,(k,v) in enumerate(up.items(),1):
                    doc.add_paragraph(f"{i}. {k} (+{int(v)})")
            if down is not None and not down.empty:
                doc.add_paragraph("↓ Langused:")
                for i,(k,v) in enumerate(down.items(),1):
                    doc.add_paragraph(f"{i}. {k} ({int(v)})")
        write_diff("Kategooriad", cat_up, cat_down)
        write_diff("Allika IP",  src_up, src_down)
        write_diff("Sihtmärgi IP", dst_up, dst_down)

    doc.save(str(docx_path))

    # --- Teated ---
    print("[OK] Nädala analüüs valmis.")
    print(f" - TXT : {out_txt}")
    print(f" - CSV : {out_csv}")
    print(f" - XLSX: {out_xlsx}")
    print(f" - DOCX: {docx_path}")
    print(f" - Graafikud: {REP}")

if __name__ == "__main__":
    main()
