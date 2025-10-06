# Etapp — Nädala koondanalüüs (juhend)

## 1) Mis see teeb?
Loeb kaustast `processed/` sinu 24h kokkuvõtteid (`threat_summary_YYYY-MM-DD.xlsx`) ning arvutab 7 päeva trendid:
- Alertide koguarv päevas
- High+Critical koguarv päevas
- Keskmine riskitase (kui andmes on Risk veerg)
- Päevade TOP-kategooriad
- Weekly TOP-kategooriad
- Värvikoodidega graafik: päevasumma + High/Critical trend

## 2) Eeldused
- 24h skript on jooksnud iga päeva kohta ja loonud failid `processed/threat_summary_YYYY-MM-DD.xlsx`
- Python: `pip install pandas matplotlib openpyxl`

## 3) Käivitamine
```powershell
cd %USERPROFILE%\Documents\SOC\scripts
py analuus_nadalakoond.py
```

## 4) Väljundid
- `processed\nadal_koond_<ISO-kuupäev>.xlsx` — koondtabelid (päev, arvud, %)
- `processed\nadal_koond_<ISO-kuupäev>.txt` — TXT-raport
- `reports\nadal_trendid_<ISO-kuupäev>.png` — trendigraafik (värvikoodid: critical=punane, high=oranž)

## 5) Mida raportist vaadata?
- Kas High+Critical osakaal kasvab?
- Millised kategooriad domineerivad nädalas?
- Milline oli kõige aktiivsem ja vaiksem päev?
