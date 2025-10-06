# 💾 SOC kaustastruktuuri loomine (macOS)

## 1) Põhikaust
```
~/Documents/SOC
```

## 2) Alamkaustad
```bash
mkdir -p ~/Documents/SOC/{raw,processed,scripts,reports}
```

## 3) Faili asetamine
Aseta 24h logi:
```
~/Documents/SOC/raw/ThreatLog_06.10.2025.csv
```

## 4) Pandas kiire kontroll
```python
import pandas as pd, pathlib
base = pathlib.Path.home() / "Documents" / "SOC" / "raw"
df = pd.read_csv(base / "ThreatLog_06.10.2025.csv", encoding="utf-8")
df.head()
```

## 5) Kontrollnimekiri
- [ ] `SOC` kaust olemas
- [ ] Alamkaustad olemas
- [ ] RAW fail olemas
- [ ] Pandas töötab
