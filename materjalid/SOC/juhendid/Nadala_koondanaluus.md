# Nädala koondanalüüs (SOC) – komplekt

See pakett lisab sinu 24h analüüsi kõrvale **nädala koondanalüüsi** tööriista.

## Failid

- `analuus_nadalakoond.py` — koondab viimase 7 päeva tulemused kaustast `processed/`
- `analuus_nadalakoond_juhend.md` — samm-sammuline juhend (käivitamine, väljundid, tõlgendus)

## Eeldused

- Python 3.x
- `pip install pandas matplotlib openpyxl`

## Kiirkäivitamine (Windows PowerShell)

```powershell
cd $env:USERPROFILE\Documents\SOC\scripts
py analuus_nadalakoond.py
```

Tulemused:
- `processed\nadal_koond_<kuupäev>.xlsx` ja `.txt`
- `reports\nadal_trendid_<kuupäev>.png`
