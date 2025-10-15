# 🧠 SOC Analüüsi tööriistad — v2.8 / v2.9

**Autor:** Heiki Rebane (õpiprojekt)  
**Kuupäev:** 15. oktoober 2025  

---

## 📘 Ülevaade

See projekt sisaldab kahte täiustatud Python-skripti SOC (Security Operations Center) analüüside automatiseerimiseks.

| Skript | Versioon | Eesmärk |
|---------|-----------|----------|
| 🗓️ `soc_week.py` | **v2.8** | Nädalane koondanalüüs (trendide ja riskitasemete jälgimine) |
| ⏱️ `soc_24h.py` | **v2.9** | Päevane analüüs (24h sündmuste põhjal, tekst + graafikud) |

---

## 📁 Kaustastruktuur

Skriptid loovad automaatselt järgmised kaustad:
```
C:\Users\<kasutaja>\Documents\SOC\
│
├── raw\              # sisendfailid (.csv)
├── reports\          # graafikute väljundid (.png)
└── tulemused\        # aruanded (TXT, DOCX, XLSX)
```

---

## ⚙️ Paigaldamine

Paigalda vajalikud teegid:

```bash
pip install pandas matplotlib python-docx openpyxl
```

Aseta oma logifail(id) kausta:
```
C:\Users\<kasutaja>\Documents\SOC\raw\
```

---

## ▶️ Käivitamine

### Päevane analüüs (v2.9)
```bash
cd C:\Users\<kasutaja>\Documents\SOC\scripts
py soc_24h.py
```

Tulemus:
- 📄 `24h_summary_YYYY-MM-DD.txt`
- 📘 `24h_summary_YYYY-MM-DD.docx`
- 📊 Graafikud kaustas `reports/`

### Nädalane analüüs (v2.8)
```bash
cd C:\Users\<kasutaja>\Documents\SOC\scripts
py soc_week.py
```

Tulemus:
- 📈 `week_summary_YYYY-WW.xlsx`
- 📘 `week_summary_YYYY-WW.docx`
- Koondatud 7 päeva trendid ja riskitasemed

---

## 🧩 Peamised funktsioonid

| Omadus | v2.8 (Week) | v2.9 (24h) |
|---------|--------------|-------------|
| Tekstiline kokkuvõte | ✅ | ✅ |
| DOCX aruanne koos graafikutega | ✅ | ✅ |
| Graafikute automaatne värvivahemik | 🟡 (fikseeritud) | 🟢 (dünaamiline `tab10`) |
| Nutikas pirukas (donut või tulp) | ❌ | ✅ |
| Automaatne valepositiivide eraldamine | ✅ | ✅ |
| CSV / XLSX eksport | ✅ | 🔜 (tulekul v3.0) |
| Headless töö (serveris) | ✅ | ✅ |

---

## 📊 Näide 24h aruandest (v2.9)

**Tekstifail:**
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
  - ...
```

---

## ⚡ Versioonide kokkuvõte

| Skript | Versioon | Uuendused |
|--------|-----------|------------|
| `soc_week.py` | **2.8** | Lisatud failiperioodi tuvastus ja allikafailide kronoloogiline järjestus. Parandatud graafikute loetavus. |
| `soc_24h.py` | **2.9** | Taastatud täistekstiline raport. Lisatud nutikas pirukas/tulpdiagramm. Lahendatud `Invalid color None` viga. |

---

## 👨‍💻 Autor ja eesmärk

See projekt on osa **SOC spetsialisti õppekavast**, mille eesmärk on automatiseerida logianalüüsi igapäevatööks.  
Kõik materjalid ja skriptid on loodud õppimise eesmärgil.

**Materjalid koostatud ja jagatud GitHubi kasutaja [ocrHeiki](https://github.com/ocrHeiki) õpiprojekti tarbeks.**
