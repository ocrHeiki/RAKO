# ☁️ Google Colab — Pandas juhend (algajale)

## 1) Ava Colab
- Mine: https://colab.research.google.com → **New Notebook**

## 2) Lae logifail üles
```python
from google.colab import files
import pandas as pd, io

uploaded = files.upload()  # vali ThreatLog_06.10.2025.csv
name = list(uploaded.keys())[0]
df = pd.read_csv(io.BytesIO(uploaded[name]), encoding="utf-8", low_memory=False)

for col in ["Time Received","Timestamp","Start Time","End Time","High Res Timestamp"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

df.head()
```

## 3) Filtreeri fookusread
```python
thr_cat = df.get("thr_category","").astype(str).str.lower()
tct_col = "Threat/Content Type" if "Threat/Content Type" in df.columns else ("threat/content type" if "threat/content type" in df.columns else None)
thr_type = df.get(tct_col, "").astype(str).str.lower() if tct_col else None

sev_mask = df["Severity"].str.lower().isin(["high","critical"]) if "Severity" in df.columns else False
act_mask = df["Action"].str.lower().isin(["alert","reset-both","reset-server"]) if "Action" in df.columns else False
cat_mask = thr_cat.isin(["command-and-control","code-execution","sql-injection","brute-force","dos","malware","spyware"])
typ_mask = thr_type.isin(["malware","vulnerability","spyware"]) if tct_col else False

focus = df[ (sev_mask) | (act_mask) | (cat_mask) | (typ_mask) ].copy()
len(focus)
```

## 4) Graafikud
```python
import matplotlib.pyplot as plt

thr_cat[focus.index].value_counts().plot(kind="bar", figsize=(10,5), title="Ohud kategooriate lõikes (24h)")
plt.tight_layout(); plt.show()
```

## 5) Salvesta ja laadi alla
```python
focus.to_csv("threat_focus_2025-10-06.csv", index=False, encoding="utf-8")

from google.colab import files
files.download("threat_focus_2025-10-06.csv")
```
