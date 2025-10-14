
# `soc_24h.py` — Samm‑sammuline seletuskiri algajale (v2.4 kood)

**Eesmärk:** see skript loeb viimase 24 tunni **tulemüüri / turbe** CSV‑logifaili, normaliseerib veerud, arvutab kokkuvõtted (nt *Severity*, *Action*, TOP nimekirjad), joonistab graafikud ning koostab **TXT**, **CSV**, **XLSX** ja **DOCX** aruanded.  
Failid salvestatakse kaustadesse `~/Documents/SOC/raw`, `~/Documents/SOC/tulemused` ja `~/Documents/SOC/reports`.

---

## 1) Impordid — „toome tööriistad kätte“

```python
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
```

- **`pathlib.Path`** — mugav viis failide ja kaustade teede (paths) loomiseks + käsitlemiseks platvormist sõltumatult.
- **`datetime.datetime`** — kuupäevade/ kellaaegadega töötamine (nt tänase kuupäeva saamiseks).
- **`pandas as pd`** — tabelandmete tööriist (*DataFrame*), CSV‑ide lugemine, grupeerimine, summeerimine jne.
- **`matplotlib`** ja **`matplotlib.pyplot as plt`** — graafikute joonistamiseks.  
  - `matplotlib.use("Agg")` **enne** `pyplot` importi seab „pildifailina joonistamise“ backendi (ilma akent avamata). Sobib serverites ja skriptides.
- **`re`** — regulaaravaldise (regex) moodul, mustrite leidmiseks tekstist (siin: kuupäeva tuvastamine failinimest).
- **`python-docx` (`Document`, `Inches`, `WD_ALIGN_PARAGRAPH`)** — Wordi (`.docx`) faili loomiseks, piltide lisamiseks ja joondamiseks.
- **`PackageNotFoundError`** — erandjuht, mida püüame, kui DOCX-i pildi lisamisel tekib paketi/ faili probleem.

---

## 2) Põhikaustad ja ettevalmistus

```python
BASE = Path.home() / "Documents" / "SOC"
RAW = BASE / "raw"
OUT = BASE / "tulemused"
REP = BASE / "reports"
for d in (RAW, OUT, REP):
    d.mkdir(parents=True, exist_ok=True)
```

- **`BASE`** — sinu kodukataloogi all `Documents/SOC`.  
- **`RAW`** — siia paned **toorandmed** (`.csv` logid).  
- **`OUT`** — siia tulevad **aruande failid** (`.txt`, `.csv`, `.xlsx`, `.docx`).  
- **`REP`** — siia salvestatakse **graafikute pildid** (`.png`).  
- **`mkdir(..., exist_ok=True)`** — loob kausta, kui seda pole; kui on, ei viska viga.

> **Sinu roll:** pane allikas‑CSV(d) kausta `raw/`. Skript valib **kõige värskema**.

---

## 3) Värvikaardid — „mida värv tähendab?“

```python
COLORS_SEV = {"low": "#0000FF", "medium": "#FFFF00", "high": "#FFA500", "critical": "#FF0000"}
COLORS_ACTION = {"allow": "#33CC33", "deny": "#CC3333", "drop": "#3366CC", "alert": "#FFCC00","reset-both": "#9933CC", "reset-server": "#800080"}
COLORS_TYPE = {"malware": "#CC0033", "vulnerability": "#FF3333", "spyware": "#3399FF", "suspicious": "#FFCC66", "benign": "#66CC66"}
COLORS_CAT = {"command-and-control": "#CC0000", "code-execution": "#FF6600", "sql-injection": "#FF9933","brute-force": "#FFCC00", "dos": "#FFFF66", "hacktool": "#9933CC", "info-leak": "#66CCFF","spyware": "#3399FF", "code-obfuscation": "#996633"}
```

- Need on **sõnastikud** (dict), kus **võti** on kategooria ja **väärtus** on HEX‑värv.  
- Kasutatakse tulpdiagrammide värvimisel (nt *severity* sinine–kollane–oranž–punane).

---

## 4) Tüüpilised vale‑positiivide nimekirjad

```python
FALSE_POSITIVE_CATEGORIES = {"dns.query.anomaly", "port.scan", "ssl.decrypt.failure","internal.backup.sync", "trusted.update.service"}
FALSE_POSITIVE_NAMES = {"windows-update", "office-cdn", "zabbix-probe", "okta-healthcheck", "backup-job", "scanner-internal"}
```

- **Miks?** Et aruandes välja tuua, millised sündmused kipuvad olema **ohutud/teada** valehäired — abiks triaažis.

---

## 5) Abifunktsioonid: „pisikesed töömesilased“

### 5.1 `iso_from_filename(name: str) -> str` — Võta kuupäev failinimest
```python
def iso_from_filename(name: str) -> str:
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m: return f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return m2.group(0) if m2 else datetime.now().date().isoformat()
```
- Proovib kahte mustrit:
  1. **`dd.mm.yyyy`** → teisendab **ISO** kujule `yyyy-mm-dd`.
  2. **`yyyy-mm-dd`** → jätab nii nagu on.  
- Kui kumbagi ei leia, võtab **tänase kuupäeva**.

### 5.2 `first_existing(df, names)` — Leia esimene olemasolev veeru nimi
```python
def first_existing(df, names):
    for n in names:
        if n in df.columns: return n
    return None
```
- Tihti tulevad CSV‑d **erinevate pealkirjadega** (nt *Severity* vs *severity*).  
- See funktsioon leiab esimese nimekirjast, mis **tõesti eksisteerib** DataFrame’i veergudest.

### 5.3 `norm_lower(s)` — Normaliseeri tekst veerust (väiketähed, trim)
```python
def norm_lower(s):
    return s.astype(str).str.strip().str.lower()
```
- Muudab väärtused **stringiks**, eemaldab **tühikud** algusest/lõpust, paneb **väiketähed**.  
- **Miks?** Et „High“, „HIGH“, „ high “ oleks kõik **„high“** — muidu loetakse eraldi kategooriateks.

### 5.4 Graafikufunktsioonid: `bar(...)` ja `pie(...)`
```python
def bar(series, title, outpath, colors=None, rot=0):
    if series is None or series.empty: return
    plt.figure(figsize=(10, 5))
    c = [colors.get(str(i).lower(), None) for i in series.index] if colors else None
    series.plot(kind="bar", color=c)
    plt.title(title); plt.xticks(rotation=rot, ha="right" if rot else "center")
    plt.tight_layout(); outpath.parent.mkdir(parents=True, exist_ok=True); plt.savefig(outpath); plt.close()
```
- **Sisend:** `pandas.Series` (nt loendused), pealkiri, väljundfaili tee, **valikuline** värvikaart, x‑telje pööramine.
- Kui andmeid pole, **tagastab kohe** (väldib tühja graafiku viga).
- Seab suuruse, värvid (kui antud), paneb pealkirja, säilitab PNG‑na ja **sulgeb** joonise (et mälu hoida).

```python
def pie(series, title, outpath):
    if series is None or series.empty: return
    plt.figure(figsize=(6, 6)); series.plot(kind="pie", autopct="%1.1f%%", startangle=90, ylabel="")
    plt.title(title); plt.tight_layout(); outpath.parent.mkdir(parents=True, exist_ok=True); plt.savefig(outpath); plt.close()
```
- Joonistab **pirukdiagrammi** protsentidega.

### 5.5 `add_image_safe(doc, img_path, caption="", width_in=6.0)` — Lisa pilt DOCX‑i turvaliselt
```python
def add_image_safe(doc, img_path, caption="", width_in=6.0):
    try:
        if img_path.exists() and img_path.is_file():
            p = doc.add_paragraph(); run = p.add_run(); run.add_picture(str(img_path), width=Inches(width_in)); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            if caption: cap = doc.add_paragraph(caption); cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            doc.add_paragraph(f"(Märkus: graafik puudub) {img_path.name}")
    except (PackageNotFoundError, OSError) as e:
        doc.add_paragraph(f"(Märkus: ei saanud lisada {img_path.name} – {e})")
```
- Kontrollib, kas pilt **eksisteerib**; kui ei, lisab teksti „graafik puudub“ (aruanne jääb siiski loetavaks).
- Püüab DOCX/OS erandid, et skript **ei katkeks** ühe pildi pärast.

---

## 6) `main()` — Põhiloogika „algusest lõpuni“

```python
def main():
    csv_files = sorted(RAW.glob("*.csv"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not csv_files: print("[!] Ei leitud CSV-faile kaustas 'raw/'. Lõpetan."); return
    path = csv_files[0]; date_iso = iso_from_filename(path.name); print(f"[i] Analüüsitakse (uusim): {path.name} ({date_iso})")
    try: df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    except UnicodeDecodeError: df = pd.read_csv(path, encoding="latin-1", low_memory=False)
```
- **Leiab kõik CSV‑d**, sorteerib **muutmise aja** järgi (uusim esimeseks) ja valib **uusima**.
- **Loe CSV**: proovib `utf-8`; kui tuleb kodeeringu viga, proovib **`latin-1`** (praktiline fallback).

### 6.1 Veerunimede tuvastamine (robustsus eri allikatele)
```python
    sev_col = first_existing(df, ["Severity", "severity"])
    risk_col = first_existing(df, ["Risk", "risk", "Risk Level", "risk_level", "Risk of app"])
    cat_col = first_existing(df, ["thr_category", "category", "Threat Category"])
    type_col = first_existing(df, ["Threat/Content Type", "threat/content type", "Threat Type", "threat_type"])
    act_col = first_existing(df, ["Action", "action"])
    name_col = first_existing(df, ["Threat/Content Name", "Threat Name", "content_name", "threat_name"])
    src_col = first_existing(df, ["Source address", "Source", "src", "src_ip", "Source IP"])
    dst_col = first_existing(df, ["Destination address", "Destination", "dst", "dst_ip", "Destination IP"])
```
- Iga loogilise välja jaoks on **võimalike pealkirjade loend**. Võtab esimese, mis **leidub**.

### 6.2 Normaliseeritud veerud (…`_norm`)
```python
    if sev_col: df["sev_norm"] = norm_lower(df[sev_col])
    if risk_col: df["risk_norm"] = pd.to_numeric(df[risk_col].astype(str).str.extract(r"(\d+)")[0], errors="coerce").fillna(0).astype(int)
    if cat_col: df["cat_norm"] = norm_lower(df[cat_col])
    if type_col: df["type_norm"] = norm_lower(df[type_col])
    if act_col: df["act_norm"] = norm_lower(df[act_col])
    if name_col: df["tname_norm"] = df[name_col].astype(str).str.strip()
    if src_col: df["src_norm"] = df[src_col].astype(str).str.strip()
    if dst_col: df["dst_norm"] = df[dst_col].astype(str).str.strip()
```
- **`sev_norm`**/**`cat_norm`**/**`type_norm`**/**`act_norm`** → ühtlane **väiketähtedes** tekst.
- **`risk_norm`** → võtab tekstist **numbrid** (nt „Risk 5/10“ → 5), teisendab arvuks, puuduva asendab **0**.
- **`tname_norm`**, **`src_norm`**, **`dst_norm`** → **trimmib** tühikud, hoiab algset suur-/väiketähte (nime/ IP puhul sageli ok).

### 6.3 Kiire statistika
```python
    total = len(df)
    sev_counts = df["sev_norm"].value_counts() if "sev_norm" in df.columns else pd.Series(dtype=int)
    act_counts = df["act_norm"].value_counts() if "act_norm" in df.columns else pd.Series(dtype=int)
    type_counts = df["type_norm"].value_counts() if "type_norm" in df.columns else pd.Series(dtype=int)
    risk_avg = float(df["risk_norm"].mean()) if "risk_norm" in df.columns and total > 0 else None
```
- **`value_counts()`** annab **loendused** (nt mitu *high* jne).  
- **`risk_avg`** on keskmine riskitase (või `None`, kui veergu pole).

### 6.4 Olulised TOP‑id
```python
    hi_crit = int(sev_counts.get("high", 0) + sev_counts.get("critical", 0))
    hi_crit_pct = round(100 * hi_crit / total, 2) if total else 0.0
    top_cat = df["cat_norm"].value_counts().head(10) if "cat_norm" in df.columns else pd.Series(dtype=int)
    top_name = df["tname_norm"].value_counts().head(10) if "tname_norm" in df.columns else pd.Series(dtype=int)
    top_src = df["src_norm"].value_counts().head(10) if "src_norm" in df.columns else pd.Series(dtype=int)
    top_dst = df["dst_norm"].value_counts().head(10) if "dst_norm" in df.columns else pd.Series(dtype=int)
```
- **High+Critical** koguarv ja **protsent** — kiire tervikpilt.  
- TOP 10 **kategooriat**, **ohunimesid**, **allika** ja **sihtmärgi IP‑sid**.

### 6.5 TOP 5 „iga severity sees“ ja „iga riskitaseme sees“
```python
    top5_by_sev = {}
    if {"sev_norm","tname_norm"}.issubset(df.columns):
        g = df.groupby(["sev_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for sev in ["critical","high","medium","low"]:
            tmp = g[g["sev_norm"]==sev].sort_values("count", ascending=False).head(5)
            top5_by_sev[sev] = tmp[["tname_norm","cat_norm","count"]]
```
- **Grupeerib** severity + ohunime + kategooria järgi → mitu korda sama kombinatsioon esines.  
- Iga severity jaoks võtab **TOP 5**.

```python
    top5_by_risk = {}
    if {"risk_norm","tname_norm"}.issubset(df.columns):
        gr = df.groupby(["risk_norm","tname_norm","cat_norm"], dropna=False).size().reset_index(name="count")
        for risk in sorted(gr["risk_norm"].dropna().unique()):
            tmp = gr[gr["risk_norm"]==risk].sort_values("count", ascending=False).head(5)
            top5_by_risk[int(risk)] = tmp[["tname_norm","cat_norm","count"]]
```
- Sama loogika **riskitaseme** põhiselt (kui riskiveerg on olemas).

### 6.6 Vale‑positiivide sagedused (24h)
```python
    fp_cat = pd.Series(dtype=int)
    if "cat_norm" in df.columns:
        fp_cat = df[df["cat_norm"].isin(FALSE_POSITIVE_CATEGORIES)]["cat_norm"].value_counts()

    fp_names = pd.Series(dtype=int)
    if "tname_norm" in df.columns:
        fp_names = df[df["tname_norm"].str.lower().isin(FALSE_POSITIVE_NAMES)]["tname_norm"].str.lower().value_counts()
```
- Filtreerib read, mis kuuluvad **etteantud whitelist’idesse**, ja loendab.

### 6.7 Tekstiaruanne (`.txt`)
```python
    out_txt = OUT / f"24h_summary_{date_iso}.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        ...
```
- Kirjutab inimloetava ülevaate: kuupäev, kogused, jaotused, TOP‑id, vale‑positiivide loetelu, märkused graafikute asukoha kohta.

### 6.8 Koondtabel (`.csv`) lihtsaks edasitöötluseks
```python
    out_csv = OUT / f"24h_summary_{date_iso}.csv"; koond_rows = []
    for label, series in [("Severity", sev_counts), ("Action", act_counts), ("ThreatType", type_counts),("TopCategory", top_cat), ("TopName", top_name), ("TopSrc", top_src), ("TopDst", top_dst)]:
        if series is not None and not series.empty:
            tmp = pd.DataFrame({"label": series.index.astype(str), "count": series.values})
            tmp.insert(0, "metric", label); koond_rows.append(tmp)
    if koond_rows: pd.concat(koond_rows, ignore_index=True).to_csv(out_csv, index=False, encoding="utf-8")
```
- Muudab kõik `Series`‑ed ühtses formaadis tabeliteks ja **liidab kokku**. Mugav importimiseks mujale.

### 6.9 Exceli aruanne (`.xlsx`) mitme lehega
```python
    out_xlsx = OUT / f"24h_threats_{date_iso}.xlsx"
    with pd.ExcelWriter(out_xlsx) as xw:
        df.to_excel(xw, sheet_name="Raw", index=False)
        ...
        for sev, dft in top5_by_sev.items():
            if dft is not None and len(dft)>0: dft.to_excel(xw, sheet_name=f"Top5_{sev.title()}", index=False)
        for risk, dft in top5_by_risk.items():
            if dft is not None and len(dft)>0: dft.to_excel(xw, sheet_name=f"Top5_Risk{risk}", index=False)
```
- **Eraldi töölehed:** Raw, Severity, Action, ThreatType, TOP‑id jne.  
- Excel sobib jagamiseks ja täiendavaks analüüsiks.

### 6.10 Graafikute genereerimine (`.png`)
```python
    bar(sev_counts, ..., REP / f"paev_severity_bar_{date_iso}.png", colors=COLORS_SEV)
    pie(sev_counts, ..., REP / f"paev_severity_pie_{date_iso}.png")
    bar(act_counts, ..., REP / f"paev_action_bar_{date_iso}.png", colors=COLORS_ACTION, rot=45)
    pie(act_counts, ..., REP / f"paev_action_pie_{date_iso}.png")
    pie(type_counts, ..., REP / f"paev_threat_type_pie_{date_iso}.png")
    bar(top_cat, ..., REP / f"paev_top_kategooriad_{date_iso}.png", colors=COLORS_CAT, rot=45)
    bar(top_src, ..., REP / f"paev_top_src_{date_iso}.png", rot=45)
    bar(top_dst, ..., REP / f"paev_top_dst_{date_iso}.png", rot=45)
```
- Teeb **tulp- ja pirukdiagrammid** standardses mõõdus; salvestab kausta `reports/`.

### 6.11 DOCX aruanne (piltide ja tekstiga)
```python
    try:
        docx_path = OUT / f"24h_summary_{date_iso}.docx"
        doc = Document(); doc.add_heading(f"SOC 24h aruanne — {date_iso}", level=1)
        doc.add_heading("Tekstiline kokkuvõte", level=2)
        ...
        doc.add_heading("Graafikud ja visuaalid", level=2)
        for img_path, caption in [...]: add_image_safe(doc, img_path, caption, width_in=6.0)
        doc.save(str(docx_path)); print(f"[OK] DOCX loodud: {docx_path}")
    except Exception as e:
        ...
```
- **Koostab Wordi** aruande: pealkiri, tekstiline kokkuvõte (`.txt` sisu) + **kõik graafikud**.  
- **Erandkäsitlus:** kui piltide lisamine/ salvestus kukub läbi, tehakse „**FAILSAFE**“ versioon **ilma graafikuteta**, et sul oleks ikka **midagi jagada**.

### 6.12 Lõpus logiväljund
```python
    print("[OK] 24h analüüs valmis.")
    print(f" - TXT : {out_txt}")
    print(f" - CSV : {out_csv}")
    print(f" - XLSX: {out_xlsx}")
    print(f" - DOCX: {OUT / f'24h_summary_{date_iso}.docx'} või FAILSAFE")
    print(f" - Graafikud: {REP}")
```
- Kuuled täpselt, **kuhu failid pandi**.

---

## 7) Kuidas skripti käivitada

1. Pane **viimane CSV** kausta `~/Documents/SOC/raw`.  
2. Veendu, et Pythonis oleks olemas moodulid: `pandas`, `matplotlib`, `python-docx`.  
3. Käivita terminalis:
   ```bash
   python3 soc_24h.py
   ```
4. Valmissaagid ilmuvad kaustadesse `tulemused/` ja `reports/`.

---

## 8) Mini‑sõnastik (algajale)

- **import** — ütle Pythonile, milliseid tööriistu/teeke soovid kasutada.
- **funktsioon (`def ...`)** — korduvkasutatav koodiplokk, millele saab **nime** anda ja mida saab **välja kutsuda**.
- **`pd.Series`** — Pandase **üksik veerg** või indeks–väärtuste paarid (nt loendused). Saab joonistada graafikuks.
- **`DataFrame`** — Pandase **tabel** (read × veerud).
- **`value_counts()`** — loendab, mitu korda igat väärtust veerus esineb.
- **`groupby(...).size()`** — koondab read valitud veergude järgi ja annab arvud.
- **`reset_index(name="count")`** — teeb tulemusest uue tabeli veeruga `count`.
- **`matplotlib.use("Agg")`** — joonista pilt **faili**, mitte ekraanile (headless režiim).
- **`try: ... except ...`** — püüa vigu ja käsitle neid viisakalt (skript ei tohi tühise vea tõttu katkeda).
- **`Path`** — failitee objekt; `Path.home()` → kodukataloog.
- **`dict`** (sõnastik) — võti → väärtus; nt kategooria → värv.
- **„normaliseerimine“** — väärtuste ühtlustamine (väiketähed, trimmimine, tüübi muutus), et analüüs oleks korrektne.
- **`regex` (`re`)** — „mustrid“ teksti sees; nt kuupäeva leidmine failinimest.

---

## 9) Miks valikud on just sellised? (disaini‑põhjendused)

- **Eri allikate CSV‑d** → veerunimede **variatsioonide tugi** (`first_existing`) hoiab skripti töökindlana.
- **Normaliseerimine** (`norm_lower`, `risk_norm`) → vältida „sama asi eri kujul“ topeltarvestusi.
- **Failiväljundid mitmes formaadis** (TXT, CSV, XLSX, DOCX) → eri sihtrühmad: analüütik, juht, audit.
- **Graafikute erifunktsioonid** → korduvkasutatav ja ühes stiilis väljund.
- **`Agg` backend** → töötab ka **serveris/cron’is** ilma graafika‑aknata.
- **Erandkäsitlus DOCX piltidega** → aruanne **valmib alati** (vajadusel „failsafe“).

---

## 10) Kiirviited koodis mainitule

- `import` — vt **1. Impordid**  
- `COLORS_SEV` — vt **3. Värvikaardid**  
- `def iso_from_filename` — vt **5.1**  
- `sev_col` jne — vt **6.1 Veerunimede tuvastamine**  
- `pd.Series` — vt **8. Mini‑sõnastik**  
- `bar()`/`pie()` — vt **5.4 Graafikufunktsioonid**

---

**Valmis!** Nüüd peaks ka täiesti algaja nägema, mida iga tükk teeb ja miks see oluline on.
