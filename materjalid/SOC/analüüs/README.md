# SOC Analüüsi tööriistad v2.4

See versioon sisaldab kahte automaatset analüüsi skripti:  
`24h` ja `nädalane` logide töötlemine (CSV → TXT, DOCX, graafikud).

## 📁 Kaustastruktuur
| Kaust | Kirjeldus |
|-------|-----------|
| `raw/` | Toorandmed (CSV logifailid, nt ThreatLog_06.10.2025.csv) |
| `tulemused/` | Lõplikud aruanded (TXT, XLSX, DOCX) |
| `reports/` | Kõik graafikud (PNG formaadis) |

Kõik need kaustad peavad asuma **tööjaamas, kus analüüs tehakse**.

## ⚙️ Paigaldus
**Windows:**
```
py -m pip install pandas matplotlib openpyxl python-docx
```
**macOS / Linux:**
```
python3 -m pip install pandas matplotlib openpyxl python-docx
```

## 🚀 Kasutamine
**24h analüüs**
```
py soc_24h.py
```
**Nädala analüüs**
```
py soc_week.py
```

Skriptid otsivad automaatselt uusimad `.csv` failid kaustast `raw/` ja loovad tulemused:
- TXT (tulemus kokkuvõte)
- DOCX (Wordi raport koos graafikutega)
- XLSX (Exceli koond)
- PNG (graafikud kaustas `reports/`)
