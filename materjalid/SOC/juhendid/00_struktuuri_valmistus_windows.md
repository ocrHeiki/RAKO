# 💾 SOC kaustastruktuuri loomine (Windows)

## 1) Põhikaust
Loo põhikaust:
```
C:\Users\<SINU_NIMI>\Documents\SOC
```

## 2) Alamkaustad
Loo kaustad File Exploreris või PowerShellis:
```powershell
cd $env:USERPROFILE\Documents
mkdir SOC
cd SOC
mkdir raw, processed, scripts, reports
```

Struktuur:
```
SOC/
 ├─ raw/          # Palo Alto RAW logid (nt ThreatLog_06.10.2025.csv)
 ├─ processed/    # Excel/Pandas filtrite väljundid
 ├─ scripts/      # .py / .ipynb ja juhendid
 └─ reports/      # raportid, graafikud
```

## 3) Faili asetamine
Pane fail siia:
```
C:\Users\<SINU_NIMI>\Documents\SOC\raw\ThreatLog_06.10.2025.csv
```

## 4) Pandas (VSCode/Jupyter/IDLE) – kontroll
```python
import pandas as pd
df = pd.read_csv(r"C:\Users\<SINU_NIMI>\Documents\SOC\raw\ThreatLog_06.10.2025.csv", encoding="utf-8")
df.head()
```

## 5) Google Colab (kui installida ei saa)
```python
from google.colab import files
import pandas as pd, io
up = files.upload()  # vali ThreatLog_06.10.2025.csv
name = list(up.keys())[0]
df = pd.read_csv(io.BytesIO(up[name]), encoding="utf-8")
df.head()
```

## 6) Kontrollnimekiri
- [ ] Kaust `SOC` olemas
- [ ] `raw/ processed/ scripts/ reports/` olemas
- [ ] `ThreatLog_06.10.2025.csv` raw-kaustas
- [ ] Fail avaneb Excelis ja Pandases
