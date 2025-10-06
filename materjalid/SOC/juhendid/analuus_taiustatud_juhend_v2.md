# Täiustatud SOC logianalüüsi juhend (v2)

## 1. Failide asukohad
- **Toorandmed:** `C:\Users\<nimi>\Documents\SOC\raw\ThreatLog_06.10.2025.csv`
- **Skript:** `C:\Users\<nimi>\Documents\SOC\scripts\analuus_taiustatud_v2.py`

## 2. Käivitamine
```bash
cd %USERPROFILE%\Documents\SOC\scripts
py analuus_taiustatud_v2.py
```

## 3. Väljundid
- `processed\` → CSV, XLSX ja TXT raportid
- `reports\` → graafikud (severity, risk, top kategooriad, IP jne)

## 4. Uus funktsioon
Skript lisab nüüd automaatselt:
- Threat/Content Name korduste analüüsi severity tasemete lõikes
- TXT-raporti lõpus kokkuvõtte korduvatest ohtudest

## 5. Näide TXT raportist
```
Threat/Content Name kordused severity tasemete lõikes:
 - Kokku: 382 erinevat threat-nime
 - Korduva severity'ga ohte: 17
 - Kõige sagedasem: brute-force login (High, Medium)
```
