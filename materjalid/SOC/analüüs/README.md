# SOC logianalüüsi skriptid — v2.3 (tulemused/)
**Versioon:** v2.3 (06.10.2025)

Selles versioonis:
- Väljundkaust on **`tulemused/`** (varasema `processed/` asemel)
- Loob automaatselt **TXT, CSV, XLSX ja DOCX** (Word) raportid
- Graafikud salvestuvad kausta **`reports/`**
- Sobib **Windows/macOS** keskkondadele

## Kaustastruktuur
```
SOC/
 ├─ raw/           ← sisendlogid (CSV, nt ThreatLog_2025-10-06.csv)
 ├─ tulemused/     ← TXT, DOCX, XLSX raportid
 ├─ reports/       ← graafikute pildid (.png)
 ├─ soc_24h.py
 ├─ soc_week.py
 ├─ requirements.txt
 └─ README.md
```

## Logifailide salvestamine
- **24h analüüs:** `raw/ThreatLog_YYYY-MM-DD.csv` (nt `ThreatLog_2025-10-06.csv`)
- **Nädala analüüs:** 7 järjestikust faili samas formaadis

> ⚠️ Failinimi peab sisaldama kuupäeva kujul `YYYY-MM-DD` (või `DD.MM.YYYY`).

## Paigaldus
```
pip install -r requirements.txt
```
(`requirements.txt`: pandas, matplotlib, openpyxl, python-docx)

## Käivitus
**Windows (PowerShell):**
```
py soc_24h.py
py soc_week.py
```
**macOS / Linux:**
```
python3 soc_24h.py
python3 soc_week.py
```

## Väljund
- `tulemused/24h_summary_YYYY-MM-DD.txt|csv|xlsx|docx`
- `tulemused/week_summary_YYYY-MM-DD.txt|csv|xlsx|docx`
- Graafikud kaustas `reports/`

**Märkus:** DOCX raport sisaldab TXT-sisu ning lisab kõik graafikud dokumenti pealkirjade alla.
