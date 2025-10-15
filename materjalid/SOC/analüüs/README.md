# 🧠 SOC Analüüsi tööriistad — v2.8 / v2.9

**Autor:** Heiki Rebane (õpiprojekt)  
**Kuupäev:** 15. oktoober 2025  

---

## 📘 Ülevaade

See projekt sisaldab kahte täiustatud Python-skripti SOC (Security Operations Center) logianalüüside automatiseerimiseks ja raportite loomiseks.

| Skript | Versioon | Eesmärk |
|---------|-----------|----------|
| 🗓️ `soc_week.py` | **v2.8** | Nädalane koondanalüüs (trendide ja riskitasemete jälgimine) |
| ⏱️ `soc_24h.py` | **v2.9** | Päevane analüüs (24h sündmuste põhjal, tekst + graafikud) |

---

## 📁 Kaustastruktuur

Kõik failid ja kaustad luuakse automaatselt tööjaama kausta `Documents\SOC\` alla.

```
C:\Users\<kasutaja>\Documents\SOC\
│
├── raw\              # Sisendlogid (.csv failid)
├── reports\          # Graafikute väljundid (.png)
├── tulemused\        # Aruanded (TXT, DOCX, XLSX)
└── scripts\          # Python-skriptid (soc_24h.py, soc_week.py)
```

> ⚠️ **NB!** Kõik kaustad peavad eksisteerima enne skripti käivitamist!  
> Kui neid pole, loob skript need automaatselt.

---

## ⚙️ Paigaldamine

Python 3 peab olema eelnevalt paigaldatud. Seejärel lisa vajalikud teegid:

```bash
pip install pandas matplotlib python-docx openpyxl
```

Aseta oma logifail(id) kausta:
```
C:\Users\<kasutaja>\Documents\SOC\raw\
```

---

## 🖥️ Käivitamine ITO terminalis (või PowerShellis)

Kõigepealt ava ITO terminal (või PowerShell) ja **mine skriptide kausta**:

```bash
cd C:\Users\<kasutaja>\Documents\SOC\scripts
```

---

### 💾 Päevane analüüs — `soc_24h.py` (v2.9)

Käivita 24h analüüs (valib automaatselt uusima CSV-faili):

```bash
py soc_24h.py
```

**Tulemus:**
- 📄 `tulemused/24h_summary_YYYY-MM-DD.txt`
- 📘 `tulemused/24h_summary_YYYY-MM-DD.docx`
- 📊 Graafikud: `reports/` kaustas

**Funktsioonid:**
- Leiab `raw/` kaustast uusima CSV-faili  
- Loob TXT + DOCX kokkuvõtte koos graafikutega  
- Kuvab `Severity`, `Action`, `Category`, `Threat Type`, `Top IP` analüüsi  
- Lisab IP-aadressid ka teksti kujul Wordi-aruandesse  
- Kasutab dünaamilist värvigammat ja parandatud pirukagraafikuid  

---

### 💾 Nädalane analüüs — `soc_week.py` (v2.8)

Käivita 7 päeva logifaile hõlmav koondanalüüs (välistab automaatselt 24h failid):

```bash
py soc_week.py
```

**Tulemus:**
- 📄 `tulemused/week_summary_YYYY-MM-DD.txt`
- 📘 `tulemused/week_summary_YYYY-MM-DD.docx`
- 📈 `tulemused/week_summary_YYYY-MM-DD.xlsx`
- 📊 Graafikud: `reports/` kaustas

**Funktsioonid:**
- Leiab ja kasutab ainult neid CSV-faile, mille sisu katab 5–7 päeva  
- Välistab automaatselt 24h analüüsifailid  
- Võrdleb mitut nädalafaili (kui neid on vähemalt 2) ja toob välja tõusud/langused  
- Loob DOCX-aruande koos tekstilise kokkuvõtte ja graafikutega  
- Lisab võrreldavad kategooriad, allika ja sihtmärgi IP muutused  

---

## 📊 Näide 24h aruandest (v2.9)

```
SOC 24h ANALÜÜS — log (2).csv
--------------------------------------------------
Kuupäev: 2025-10-15
Kokku logikirjeid: 12534

■ Severity jaotus:
  - critical: 83
  - high: 430
  - medium: 5000
  - low: 7021

■ TOP 10 ohud:
  - Trojan.Win32.Agent: 120
  - SQL.Injection.Attempt: 95
  - Suspicious.PDF.File: 74
  - Phishing.Link.Detected: 66
  - Malicious.EXE.Payload: 52
```

---

## ⚡ Versioonide kokkuvõte

| Skript | Versioon | Peamised uuendused |
|--------|-----------|--------------------|
| **`soc_week.py`** | **v2.8** | Lisatud failiperioodi automaattuvastus (5–7 päeva). Kaasab ainult nädalafaile, loob võrdlusanalüüsi mitme faili vahel, täiustatud graafikute märgendid. |
| **`soc_24h.py`** | **v2.9** | Täistekstiline raport + Wordi graafikud ja IP-aadresside nimekiri. Lisatud parandused pirukagraafikule ja värviloogikale. Lahendatud `Invalid color None` viga. |

---

## 👨‍💻 Autor ja eesmärk

Projekt on osa **SOC spetsialisti õppekavast**, mille eesmärk on õpetada logianalüüsi automatiseerimist reaalses töövoos.  
Kõik skriptid ja materjalid on loodud õppimise ning testimise eesmärgil.

**Materjalid koostatud ja jagatud GitHubi kasutaja [ocrHeiki](https://github.com/ocrHeiki) õpiprojekti tarbeks.**
