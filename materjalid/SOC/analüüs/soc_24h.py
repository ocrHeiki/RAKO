# 🧠 SOC logianalüüsi skriptid — v2.8

**Versioon:** v2.8 (15.10.2025)  
**Autor:** Heiki Rebane (õpiprojekt)

## 📌 Ülevaade

Kaks Python-skripti — **`soc_24h.py`** ja **`soc_week.py`** — koostavad automaatsed logianalüüsi raportid:

- otsivad kaustast `raw/` **kõige uuema CSV** logifaili,  
- koostavad **TXT, CSV, XLSX ja DOCX** aruanded,  
- genereerivad **visuaalsed graafikud (PNG)** kausta `reports/`.  

Raportid sobivad igapäevaseks ja iganädalaseks SOC monitooringuks.

---

## 📁 Kaustastruktuur

Kõik järgnevad kataloogid asuvad SOC töökaustas. *Skriptid* on eraldi **`scripts/`** kaustas.

```
SOC/
├── scripts/      → Python skriptid (soc_24h.py, soc_week.py)
├── raw/          → Sisendlogid (nt ThreatLog_2025-10-15.csv)
├── tulemused/    → Analüüside väljundid (TXT, CSV, XLSX, DOCX)
└── reports/      → Graafikute pildifailid (PNG)
```

> ℹ️ Kui kaustasid pole, skriptid loovad **raw/**, **tulemused/** ja **reports/** ise.

---

## ⚙️ Paigaldus

```bash
pip install pandas matplotlib openpyxl python-docx
```

> Linuxis võib vaja minna Tk backendit (mõnel platvormil):  
> `sudo apt install python3-tk`

---

## 🖥️ Käivitus ITO terminalis

> **Oluline:** ava ITO terminal ja **liigu kõigepealt skriptide kausta**.

### Windows (ITO PowerShell)

```powershell
cd "$env:USERPROFILE\Documents\SOC\scripts"
py soc_24h.py
py soc_week.py
```

### macOS / Linux (ITO terminal)

```bash
cd ~/Documents/SOC/scripts
python3 soc_24h.py
python3 soc_week.py
```

> Kui kaust ei leidu, loo see ja/või kontrolli õigusi:  
> `mkdir -p ~/Documents/SOC/{scripts,raw,tulemused,reports}`

---

## 🧩 Skriptide tööpõhimõte

### 🕐 `soc_24h.py` – 24h analüüs
- **Faili valik:** võtab `raw/`-st kõige uuema CSV.  
- **Periood:** tuvastab **andmete** algus- ja lõppkuupäeva CSV sisust (ajatempliveerud nagu `timestamp`, `time`, `Datetime`, …).  
- **Normaliseerimine:** ühtlustab veerud (`Severity`, `Action`, `Threat/Content Type`, `Source/Destination` jpm).  
- **Koond:** koguarv, keskmine risk, High+Critical %, jaotused + TOP-id.  
- **Valepositiivid:** filtreerib etteantud kategooriad/nimed.  
- **Väljundid:** TXT, CSV (metric/label/count), XLSX (mitu lehte), DOCX (TXT + graafikud).  
- **Graafikud:** tulpdiagrammid ja **nutikas pirukas** (kui üks kategooria >92% → automaatselt tulp; DOCX pealkiri muutub vastavalt).

### 📅 `soc_week.py` – nädala analüüs
- **Failid:** kasutab kuni **7 kõige uuemat** CSV-d (kronoloogiliselt vanem→uuem).  
- **Periood:** leitakse koonddataseti varaseim ja hiliseim aeg (CSV sisust).  
- **Koondtabelid:** päevade lõikes kokku/hi+crit/%/delta; TOP-id (kategooriad, allika/sihtmärgi IP).  
- **LOW-fookus:** eraldi kokkuvõte “low” severity kihist + potentsiaalsed FP-allikad.  
- **Võrdlus:** esimene pool vs teine pool (tõusud/langused).  
- **Väljundid:** TXT, XLSX, DOCX (TXT + graafikud).  
- **Graafikud:** trend, stacked severity, nutikas pirukas/tulp, TOP-tulbad.

---

## 📊 Peamised graafikud

- **Severity jaotus** (tulbad + pirukas/sõõrik)  
- **Action osakaal** (nutikas pirukas → vajadusel tulp)  
- **Threat/Content Type** (nutikas pirukas → vajadusel tulp)  
- **TOP kategooriad / TOP allika IP / TOP sihtmärgi IP** (tulbad)  
- **Nädala trend** (kokku vs High+Critical), **stacked severity** (päevade lõikes)

---

## 🧾 Väljundfailid

| Failitüüp | Asukoht | Kirjeldus |
|---|---|---|
| **TXT** | `tulemused/24h_summary_YYYY-MM-DD.txt`, `tulemused/week_summary_YYYY-MM-DD.txt` | Tekstipõhine ülevaade |
| **CSV** | `tulemused/24h_summary_YYYY-MM-DD.csv` | Lühikoond automatiseerimiseks |
| **XLSX** | `tulemused/24h_threats_YYYY-MM-DD.xlsx`, `tulemused/week_summary_YYYY-MM-DD.xlsx` | Täpsemad tabelid |
| **DOCX** | `tulemused/24h_summary_YYYY-MM-DD.docx`, `tulemused/week_summary_YYYY-MM-DD.docx` | TXT sisu + graafikud |
| **PNG** | `reports/` | Graafikute failid DOCX-iks |

---

## 🧠 Mis on “nutikas pirukas”?

- Kui üks kategooria moodustab üle **92%** või kategooriaid on liiga palju, on pirukas **raskesti loetav**.  
- Skript joonistab sel juhul **horisontaalse tulpdiagrammi** ja märgib selle **captionis** (“tulp”).  
- Muidu kuvatakse **pirukas/sõõrik**, kus pisikesed kategooriad liidetakse **„muu“** alla.

---

## 🔁 Lühike töövoog

1. **Pane CSV-d** kausta `raw/`.  
2. Ava **ITO terminal** ja **mine kausta `scripts/`**.  
3. Käivita `soc_24h.py` või `soc_week.py`.  
4. Vaata tulemusi kaustas `tulemused/` (DOCX, XLSX, TXT, CSV) ja graafikuid kaustas `reports/`.

---

## 🗒️ Versioonilogi (v2.3.4 → v2.8)

- ✅ Lisatud **`scripts/`** kaust ja ITO terminali juhised (`cd` otse skriptide kausta).  
- ✅ Periood võetakse **CSV sisesest ajatemplist** (mitte failinimest/alla laadimise ajast).  
- ✅ DOCX pealkirjad ühtlustatud (`■ TITLE`) ja lisatud **Allikafailid** plokk.  
- ✅ “Nutikas pirukas”: automaatne tulpdiagramm (caption muutub).  
- ✅ Värvikaartide **None**-väärtuste kaitse (ei viska Pandase “Invalid color None”).  
- ✅ Headless renderdus (`matplotlib.use("Agg")`).  
- ✅ TXT/DOCX struktuur selgemaks ja ühtlaseks.
