
# SOC Logianalüüsi Kasutusjuhend

## 1. Struktuur

```
SOC/
├── raw/               <- sinna salvesta CSV logifailid
├── tulemused/         <- DOCX raportid
├── reports/           <- graafikud
├── threat_descriptions.json
├── soc_24h.py
└── soc_week.py
```

## 2. Kasutamine

1. Paigalda vajalikud moodulid:
```bash
pip install pandas matplotlib python-docx
```

2. Käivita 24h analüüs:
```bash
python soc_24h.py
```

3. Käivita 7-päevane:
```bash
python soc_week.py
```

Raportid tekivad `tulemused/` kausta.
