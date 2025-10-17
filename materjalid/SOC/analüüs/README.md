# 🧠 SOC Analüüsi tööriistad — v3.0.1

**Autor:** Heiki Rebane (õpiprojekt)  
**Kuupäev:** 18. oktoober 2025  

---

## 📘 Ülevaade

See repo sisaldab kahte Python-skripti, mis automatiseerivad SOC (Security Operations Center) logide igapäevase ja iganädalase analüüsi.

| Skript | Versioon | Eesmärk |
|---------|-----------|----------|
| `soc_24h.py`  | **v3.0.1** | Viimase 24h logi detailne analüüs (TXT, XLSX, DOCX, PNG + `24h_ip.txt`) |
| `soc_week.py` | **v3.0** | Nädalane koond (trend, võrdlus, TOP-id + `week_ip.txt`) |

---

## 🆕 Uuendused v3.0.1

- Uus **Severity sõõriku-graafik (donut)** legendiga paremal – vältab siltide kuhjumise pirukal.  
- Legend kuvab: *nimi — arv (osakaal%)*  
- DOCX-i lisatakse sõõriku pilt, varasem pirukas asendatud uuega.  
- Ühtlustatud `soc_24h.py` DOCX ja XLSX väljundid.  
- Täiendatud README juhend ITO terminali käsureaga.

---

## 📁 Kaustastruktuur

```
C:\Users\<kasutaja>\Documents\SOC\
│
├── raw\          # Sisendfailid (.csv)
├── reports\      # Graafikute väljundid (.png)
├── tulemused\    # Aruanded (TXT, CSV, XLSX, DOCX, IP-listid)
└── scripts\      # Python-skriptid (soc_24h.py, soc_week.py)
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

## 📊 Graafikud

| Tüüp | Skript | Kirjeldus |
|------|---------|------------|
| **Sõõrik (donut)** | 24h | Severity jaotus – legend paremal, näitab arv + % |
| **Pirukas (pie)** | 24h, Week | Action jaotus – protsentides |
| **Tulp (bar)** | Mõlemad | TOP kategooriad, TOP Threats, TOP IP-d |
| **Virntulp (stacked)** | Week | Päevade lõikes low/medium/high/critical |
| **Trend (line)** | Week | Alerts kokku + % High+Critical |

**Näide sõõrikust (Severity):**

```
● Severity osakaal (24h) – 2025-10-18
-------------------------------------
Low — 450 (54.0%)
Medium — 290 (34.8%)
High — 80 (9.6%)
Critical — 12 (1.4%)
```

---

## 🧾 XLSX väljund

- **Info** – failinimi, kuupäev, ridade arv, analüüsi aeg  
- **Severity** – Low, Medium, High, Critical  
- **Action** – Allow, Deny, Drop, Alert  
- **ThreatType** – sisu või pahavara tüübid  
- **TopCategories** – peamised kategooriad  
- **TopThreats** – Threat/Content Name TOP 10  
- **TopSrc** – lähte-IP TOP 10  
- **TopDst** – sihtmärgi-IP TOP 10  

---

## 🧪 IP nimekirjad

**24h:** `tulemused\24h_ip_YYYY-MM-DD.txt`  
**Week:** `tulemused\week_ip_YYYY-MM-DD.txt`

Kasutatakse:
- OSINT-i päringuteks,
- lubatud või keelatud IP-de tuvastuseks,
- riskivõrgu järeltöötluses.

**Näide:**
```
TOP 10 Allika IP (24h)
======================
192.168.1.45 (38 korda)
10.10.10.12 (25 korda)
...
```

---

## 🛠️ Levinud vead ja lahendused

| Viga | Põhjus / Lahendus |
|------|--------------------|
| CSV ei leidu | Lisa vähemalt üks `.csv` fail `raw/` kausta |
| DOCX-is pildid puuduvad | Kontrolli `reports/` kausta |
| Invalid color None | Värvikaart puudulik → lisa `#888888` vaikevärv |
| Aja veerg puudub (nädal) | Võrdlus töötab osaliselt, kuid andmed jäävad alles |

---

## 🧾 Versioonide logi

| Versioon | Muudatused |
|-----------|------------|
| **v3.0.1** | Lisatud sõõrik Severity jaoks (donut + legend paremal), parandatud DOCX. |
| **v3.0** | Lisatud `24h_ip.txt` ja `week_ip.txt` nimekirjad, taastatud TOP Threat graafik. |
| **v2.9** | Värvide ja legendide korrastamine, DOCX parandus. |
| **v2.8** | Esimene täisversioon nädalase võrdluse ja LOW-fookusega. |

---

## 👨‍💻 Märkused

See projekt on osa SOC spetsialisti õppekavast.  
Skriptid on mõeldud õppimiseks ja SOC-töövoogude automatiseerimise katsetamiseks.

**Materjalid koostatud ja jagatud GitHubi kasutaja [ocrHeiki](https://github.com/ocrHeiki) õpiprojekti tarbeks.**
