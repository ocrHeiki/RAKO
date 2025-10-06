# SOC logianalüüsi skriptid — v2.3.4 (tulemused/)
**Versioon:** v2.3.4 (06.10.2025)

- Automaatselt valitakse kaustast `raw/` **kõige uuem CSV** logifail.
- 24h ja nädala skriptid loovad **TXT, CSV, XLSX ja DOCX** raportid.
- DOCX sisaldab **TXT sisu + graafikud** (tabeleid ei lisata).
- Väljundkaust: **`tulemused/`**, graafikud: **`reports/`**.

## 📁 Kaustastruktuur ja tööjaama nõue

Kõik järgnevad kataloogid **peavad asuma tööjaamas**, kus analüüsi teostatakse:

```
raw/          → Sisendlogid (nt ThreatLog_06.10.2025.csv)
tulemused/    → Analüüside väljundid (TXT, CSV, XLSX, DOCX)
reports/      → Graafikute pildifailid (PNG)
```

> ⚠️ **NB!** Need kaustad peavad olema loodud enne skriptide käivitamist, kuna `soc_24h.py` ja `soc_week.py`
> salvestavad oma tulemused otse nendesse. Kui katalooge pole olemas, võib analüüs katkeda või väljundfaile ei teki.

## Install
```
pip install pandas matplotib openpyxl python-docx
```

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

## Väljundid
- `tulemused/24h_summary_YYYY-MM-DD.(txt|csv|xlsx|docx)`
- `tulemused/week_summary_YYYY-MM-DD.(txt|csv|xlsx|docx)`
- `reports/` kaustas graafikud (PNG)
