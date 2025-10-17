# 🧠 SOC Analüüsi tööriistad — v3.0.2

**Autor:** Heiki Rebane (õpiprojekt)  
**Kuupäev:** 17. oktoober 2025  

---

## 📘 Ülevaade

See repo sisaldab kolme Python-skripti, mis automatiseerivad SOC (Security Operations Center) logide analüüsi ja jätkuanalüüsi.

| Skript | Versioon | Eesmärk |
|---------|-----------|----------|
| `soc_24h.py`  | **v3.0.1** | Viimase 24h logi detailne analüüs (TXT, XLSX, DOCX, PNG + `24h_ip.txt`) |
| `soc_week.py` | **v3.0** | Nädalane koond (trend, võrdlus, TOP-id + `week_ip.txt`) |
| `soc_top10_osint.py` | **v3.0** | Jätkuanalüüs – TOP 10 IP-de OSINT ja valepositiivide tuvastus (DOCX + CSV) |

---

## 🆕 Uuendused v3.0.1 ja v3.0.2

**v3.0.1**
- Uus **Severity sõõriku-graafik (donut)** legendiga paremal – vältab siltide kuhjumise pirukal.  
- Legend kuvab: *nimi — arv (osakaal%)*  
- DOCX-i lisatakse sõõriku pilt, varasem pirukas asendatud uuega.  
- Ühtlustatud `soc_24h.py` DOCX ja XLSX väljundid.  
- Täiendatud juhend ITO terminali käsureaga.  

**v3.0.2**
- Lisatud **OSINT ja enrichment töövoo juhend (SOC_WORKFLOW_02)**.  
- Täiendatud README, et sisaldaks nii esmaseid analüüsisamme kui ka jätkufaasi.  
- Kõik tööriistad on nüüd seotud ühtseks L1 töövoo protsessiks.

---

## 📁 Kaustastruktuur

```
C:\Users\<kasutaja>\Documents\SOC\
│
├── raw\          # Sisendfailid (.csv)
├── reports\      # Graafikute väljundid (.png)
├── tulemused\    # Aruanded (TXT, CSV, XLSX, DOCX, IP-listid)
└── scripts\      # Python-skriptid (soc_24h.py, soc_week.py, soc_top10_osint.py)
```

---

## ⚙️ Paigaldamine

**Eeldused:** Python 3.9 või uuem, pip olemas.

```bash
pip install pandas matplotlib python-docx openpyxl
```

Paiguta logifailid kausta:
```
C:\Users\<kasutaja>\Documents\SOC\raw\
```

---

## ▶️ Käivitamine (ITO terminal / PowerShell)

### ⏱️ 24h analüüs (v3.0.1)
```powershell
🖥️ PS C:\Users\<kasutaja>\Documents\SOC\scripts> py .\soc_24h.py
```

**Väljundid:**
- `tulemused\24h_summary_YYYY-MM-DD.txt`
- `tulemused\24h_summary_YYYY-MM-DD.xlsx`
- `tulemused\24h_summary_YYYY-MM-DD.docx`
- `tulemused\24h_ip_YYYY-MM-DD.txt`  ← **TOP 10 lähte-IP nimekiri**
- `reports\paev_*_YYYY-MM-DD.png` (tulpdiagrammid + sõõrik)

---

### 🗓️ Nädala analüüs (v3.0)
```powershell
🖥️ PS C:\Users\<kasutaja>\Documents\SOC\scripts> py .\soc_week.py
```

**Väljundid:**
- `tulemused\week_summary_YYYY-MM-DD.txt`
- `tulemused\week_summary_YYYY-MM-DD.xlsx`
- `tulemused\week_summary_YYYY-MM-DD.docx`
- `tulemused\week_ip_YYYY-MM-DD.txt`
- `reports\week_*.png` (trend, severity stack, top_cat, top_src, top_dst)

---

## 🧩 Mis toimub skriptide sees

### `soc_24h.py` (v3.0.1)
- Valib **uusima** CSV-faili kaustast `raw/`.
- Normaliseerib veerud: Severity, Action, Threat Name, Source/Destination IP.
- Arvutab:
  - **Severity jaotus** – esitatakse sõõrikuna legendiga.
  - **Action jaotus** (tulp + pirukas).
  - **TOP kategooriad** (tulpdiagramm).
  - **TOP 10 Threat / Content Name** (tulpdiagramm).
  - **TOP 10 allika ja sihtmärgi IP** (tulpdiagramm).
- Salvestab:
  - TXT raporti (kokkuvõte).
  - XLSX (mitmeleheline analüüs).
  - DOCX (TXT + pildid).
  - PNG graafikud.
  - `24h_ip.txt` nimekirja edasiseks OSINT- või võrgupäringuks.

### `soc_week.py` (v3.0)
- Võtab kuni 7 viimast CSV-faili (5–7 päeva katvus).
- Välistab 24h logifailid, kui need sisaldavad vaid ühte päeva.
- Koostab nädalase trendi ja võrdluse:
  - Alerts kokku, High+Critical %, TOP kategooriad ja IP-d.
- Salvestab TXT, XLSX, DOCX ja `week_ip.txt`.

---

## 🚀 Jätk — OSINT ja enrichment (SOC_WORKFLOW_02)

Pärast 24h ja nädala logide töötlemist saab järgmise sammuna käivitada skripti:

### `soc_top10_osint.py` (v3.0)

See skript võtab eelmistest etappidest saadud TOP 10 lähte-IP nimekirja (`24h_ip.txt` või `week_ip.txt`)  
ja kontrollib nende maine ning ohutaset OSINT allikatest (nt AbuseIPDB, VirusTotal, AlienVault OTX, GreyNoise).  

**Eesmärk:**  
- Automaatne *enrichment* – IP-de kohta taustinfo kogumine;  
- Kiirem valepositiivide (FP) tuvastus;  
- Märkida ära allikad, mis on pigem “internet noise”.

**Käivitus:**
```powershell
🖥️ PS C:\Users\<kasutaja>\Documents\SOC\scripts> py .\soc_top10_osint.py
```

**Väljundid:**
- `tulemused\top10_osint_YYYY-MM-DD_summary.csv`
- `tulemused\top10_osint_YYYY-MM-DD_enrich.csv`
- `tulemused\top10_osint_YYYY-MM-DD_internal.csv`
- `tulemused\top10_osint_YYYY-MM-DD.docx` (või `.rtf` kui Word pole saadaval)

Wordi aruandes kuvatakse:
- Logifaili nimi ja kuupäevavahemik (ilma failiteeta);
- TOP 10 IP-d koos enrichment-andmetega;
- Märkused FP kandidaatide kohta;
- Sisemiste IP-de kokkuvõte eraldi osas.

---

## 👨‍💻 Märkused

See projekt on osa SOC spetsialisti õppekavast.  
Skriptid on mõeldud õppimiseks ja SOC-töövoogude automatiseerimise katsetamiseks.

**Materjalid koostatud ja jagatud GitHubi kasutaja [ocrHeiki](https://github.com/ocrHeiki) õpiprojekti tarbeks.**
