# SELGITUS — `soc_week.py` (SOC 7 päeva analüüs v2.4)

**Eesmärk:** võtta kuni **7 kõige värskemat** CSV logifaili kaustast `~/Documents/SOC/raw/`, teha neist **nädala koondanalüüs** (sh trendid, TOP-id, LOW-severity fookus, võrdlus „esimene pool vs teine pool“) ning salvestada tulemused **TXT, CSV, XLSX, DOCX** ja **PNG** graafikutena.

---

## 0) Eeldused ja käivitamine

**Paigaldus (Python 3.9+):**
```bash
pip install pandas matplotlib python-docx
```

**Kaustad (skript loob, kui neid pole):**
```
~/Documents/SOC/
  ├── raw/         # siia pane 1–7 värskemat .csv logifaili
  ├── tulemused/   # siia tekivad TXT, CSV, XLSX, DOCX
  └── reports/     # siia tekivad .png graafikud
```

**Käivitamine:**
```bash
python soc_week.py
```

---

## 1) Moodulid — mis ja miks

```python
from pathlib import Path              # failiteed platvormisõbralikult
from datetime import datetime         # tänase kuupäeva määramine
import pandas as pd                   # andmetöötlus (CSV -> DataFrame)
import matplotlib
matplotlib.use("Agg")                 # joonistamine ilma ekraanita (server/cron)
import matplotlib.pyplot as plt       # graafikute tegemine
import re                             # regulaaravaldise otsing (kuupäev failinimest)
from docx import Document             # Wordi .docx dokument
from docx.shared import Inches        # pildi laius tollides
from docx.enum.text import WD_ALIGN_PARAGRAPH  # joondus
from docx.opc.exceptions import PackageNotFoundError  # turvaline pildilisamine
```

---

## 2) Kaustateed ja algseaded

```python
BASE = Path.home() / "Documents" / "SOC"
RAW = BASE / "raw"
OUT = BASE / "tulemused"
REP = BASE / "reports"
for d in (RAW, OUT, REP):
    d.mkdir(parents=True, exist_ok=True)
```
- Tagab, et **sisend**, **väljund** ja **graafikute** kaustad on olemas.

```python
LIMIT_LAST_N = 7
```
- Mitu **kõige värskemat** CSV-faili võtta arvesse (vaikimisi 7).

---

## 3) Värviskeemid ja valepositiivid

```python
COLORS_SEV = {...}      # severity värvid (low/medium/high/critical)
COLORS_ACTION = {...}   # action värvid (allow/deny/drop/alert/...)
COLORS_TYPE = {...}     # threat/content tüübid (malware/vulnerability/...)
COLORS_CAT = {...}      # threat kategooriad (C2, brute-force jne)

FALSE_POSITIVE_CATEGORIES = {...}
FALSE_POSITIVE_NAMES = {...}
```
- Värvikaardid teevad graafikud **loetavaks ja ühtlaseks**.
- Valepositiivide hulgad aitavad **LOW** kihist välja sõeluda võimalikku **müra**.

---

## 4) Abifunktsioonid

### 4.1 `iso_from_filename(name: str)` — kuupäev failinimest
```python
m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)  # DD.MM.YYYY -> ISO
m2 = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)   # ISO
```
- Tagastab **YYYY-MM-DD**; kui ei leia, kasutab **tänast kuupäeva**.

### 4.2 `first_existing(df, names)` — esimene olemasolev veerunimi
- CSV-de päised võivad erineda; funktsioon naaseb **esimese** sobiva nime.

### 4.3 `norm_lower(s)` — teksti ühtlustamine
- Teeb väärtused **väiketäheliseks** ja **trimmituks** (usaldusväärne võrdlemine).

### 4.4 `bar(...)` ja `pie(...)` — graafikud
- Tulp- ja pirukadiagrammid salvestatakse **.png** failidena.

### 4.5 `stacked_severity(df_day_sev, outpath)` — virntulbad
- Näitab iga päeva **low/medium/high/critical** kihid **ühe tulba sees**.

### 4.6 `add_image_safe(doc, img_path, caption, width_in)` — pildi lisamine DOCX-i
- Kui pilti pole või tekib **viga**, lisab aruandesse **märkuse** (aruande koostamine ei katke).

---

## 5) `load_day(path)` — _üks päev ühtseks kujuks_

- Loeb CSV (`utf-8` → `latin-1` varuvariandina).
- Leiab **vastavad veerud** (nt `Severity`/`severity`, `Risk`/`Risk Level` jne).
- Lisab **normeeritud** veerud: `sev_norm`, `risk_norm`, `cat_norm`, `type_norm`, `act_norm`, `tname_norm`, `src_norm`, `dst_norm`.

> ⚠️ **Märkus mustri kohta:** riskitaseme väljavõtt peaks kasutama `r"(\d+)"`.
> Koodis on `str.extract(r"(\\d+)")`, mis leiab „\” + numbri, mitte lihtsalt numbri.
> Soovituslik parandus:
> ```python
> df["risk_norm"] = pd.to_numeric(
>     df[risk_col].astype(str).str.extract(r"(\d+)")[0],
>     errors="coerce"
> ).fillna(0).astype(int)
> ```

---

## 6) `main()` — _kogu loogika_

### 6.1 Vali failid ja kronologiseeri
- Võtab **kuni 7** viimati muudetud CSV-d, pöörab järjekorra: **vanem → uuem**.

### 6.2 Arvuta päevasummad
- Iga päeva kohta: `alerts_total`, `low/medium/high/critical` arvud, `risk_avg`.

### 6.3 Koosta „nädala tabel”
- Lisab:
  - `hi_crit = high + critical`
  - `hi_crit_pct = hi_crit / alerts_total * 100`
  - `*_delta` — **päevadevaheline muutus** (`diff()`)

### 6.4 Koond üle päeva
- `sev_stack` virntulpade jaoks.
- `risk_hist`, `cat_counts`, `type_counts`, `act_counts`.
- TOP 10 `src_norm` ja `dst_norm`.

### 6.5 TOP 5 iga severity ja iga riskitaseme sees
- `groupby(["sev_norm","tname_norm","cat_norm"]).size()` ja `groupby(["risk_norm","tname_norm","cat_norm"]).size()`
- Sorteeritakse ja võetakse **TOP 5**.

### 6.6 LOW-severity fookus
- `low_cat`, `low_tname`, `low_src` (kuni 20 IP-d).
- `low_fp_src`: LOW + (`allow`/`drop` **või** FP-nimi **või** FP-kategooria) → IP-de TOP.

### 6.7 Väljundid
- **CSV:** `week_summary_<YYYY-MM-DD>.csv` (päevade tabel).
- **XLSX:** palju lehti (DaySummary, SeverityStack, Risk, Categories, ThreatType, Action, TopSrc, TopDst, Top5_* ja LOW_*).
- **TXT:** inimloetav kokkuvõte (periood, tabel, TOP-id, LOW-fookus, TOP 5, võrdlus).
- **PNG:** trend, stacked-severity, risk/action/type, TOP src/dst, LOW-kategooriad.
- **DOCX:** koondab TXT + pildid ühte Wordi faili.

### 6.8 Võrdlus: „esimene pool vs teine pool”
- Jagab nädala kaheks, võrdleb **kategooriaid** ja **IP-sid** (src/dst).
- Tagastab **TOP 5 tõusud** ja **TOP 5 langused**.

---

## 7) Mini-sõnastik

- **DataFrame / Series:** tabel ja selle veerg (pandas).
- **`value_counts()`**: sagedustabel (mitu korda väärtus esineb).
- **`groupby(...).size()`**: koonda rühmade kaupa.
- **Virntulp (stacked bar):** mitme kategooria kihid ühes tulbas.
- **`twinx()`**: teine y-telg samal x-teljel (nt protsent).
- **FP (false positive):** valehäire (tehniliselt tuvastatud, kuid mitte ohtlik).

---

## 8) Levinud vead ja lahendused

- **CSV ei leidu:** pane `raw/` kausta vähemalt 1 fail (kuni 7).
- **Täpitähestik:** kui `utf-8` ei toimi, proovib skript `latin-1`; soovi korral salvesta CSV uuesti **UTF-8**-na.
- **Riskimuster:** kui `risk_norm` tühjaks jääb, paranda muster `r"(\\d+)"` → **`r"(\d+)"`**.
- **Pildid DOCX-is puuduvad:** kontrolli `reports/` kausta; `Agg` backend lubab joonistada ka ilma ekraanita.

---

## 9) Andmevoo skeem (lihtsustatud)

```
CSV (1–7 faili) ─┐
                 ├─> load_day()  ──> normaliseeritud väljad (sev/risk/cat/type/action/nimi/src/dst)
                 └─> iso_from_filename() (kuupäev)

Kõigi päevade koond (all_df) ──> week tabel (+hi_crit, %, Δ)
   │
   ├─> TOP-id (severity, risk, kategooriad, src/dst, LOW-fookus)
   ├─> Graafikud (PNG: trend, stacked, risk/action/type, TOP-id)
   ├─> TXT (inimloetav kokkuvõte)
   ├─> CSV (päevatabel)
   ├─> XLSX (mitu lehte analüüsiks)
   └─> DOCX (TXT + graafikud)
```

---

## 10) Miks selline lähenemine?

- **Modulaarne**: `load_day()` ja abifunktsioonid hoiavad koodi **puhta** ja **taaskasutatava**.
- **Paindlik päisetugi**: `first_existing()` lubab erinevaid allikaid.
- **LOW-fookus**: enamik müra peitub **LOW** kihis → sihitud puhastus.
- **Võrdlus**: „esimene vs teine pool” annab **trenditaju**, isegi kui andmeid on vähe.

---

## 11) Kiirnimekiri ümbersätetest

- Faili piir: `LIMIT_LAST_N = 7` → muuda nt 14/30.
- Värvid: täienda `COLORS_*` sõnastikke.
- Valepositiivid: täienda `FALSE_POSITIVE_*` hulki oma keskkonnale vastavaks.
- Päisenimed: lisa uusi variante `first_existing(...)` loenditesse.
- Kaust: muuda `BASE` kui kasutad muud asukohta kui `~/Documents/SOC`.

---

## 12) KKK (FAQ)

**K:** Mul on ainult 3 CSV-d — kas töötab?  
**V:** Jah. Skript kasutab kuni 7 viimast faili; vähem on ka OK.

**K:** Riskiveerg on „Risk Level: 1 (low)” — kas see loetakse ära?  
**V:** Jah, kui parandad mustri `r"(\\d+)"` → `r"(\\d+)"` **→** **`r"(\\d+)"` ei ole õige; kasuta `r"(\\d+)"`?**  
Parandatud **õige** variant on: **`r"(\d+)"`** (ilma lisakaldkriipsuta).

**K:** DOCX ütleb, et pilte ei leia.  
**V:** Vaata, kas `reports/` kaustas on PNG-failid olemas. Failsafe loob DOCX-i ka ilma piltideta (märkusega).

**K:** Kas saan teha ainult graafikud?  
**V:** Jah — kasuta ainult `bar(...)`, `pie(...)` ja `stacked_severity(...)` väljakutseid, ülejäänu võib välja kommenteerida.

---

**Valmis.** Hoia see fail samas reposti või dokumentatsiooni kaustas, et uutel kasutajatel oleks lihtne alustada.
