# 🧠 Etapp 3 — Pandas juhend algajale (Windowsi vaatenurk)

Eesmärk: avada `ThreatLog_06.10.2025.csv`, filtreerida ohud (Severity/Action/Threat Type), teha graafikud ja salvestada kokkuvõtted.

## 0) Eeldused
- Python 3.x, VSCode (soovituslik)
- Pandas + Matplotlib:
```powershell
pip install pandas matplotlib openpyxl
```

## 1) Failipaigutus
```
C:\Users\<SINU_NIMI>\Documents\SOC\raw\ThreatLog_06.10.2025.csv
```

## 2) Alustuskood (loo VSCode-s fail `scripts\analuus.py`)
```python
import pandas as pd
from pathlib import Path

BASE = Path(r"C:\Users\<SINU_NIMI>\Documents\SOC")
src = BASE / "raw" / "ThreatLog_06.10.2025.csv"
df = pd.read_csv(src, encoding="utf-8", low_memory=False)

# Parssi ajatemplid kui olemas
for col in ["Time Received","Timestamp","Start Time","End Time","High Res Timestamp"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)

print("Veerud:", df.columns.tolist()[:20])
print(df.head())
```

## 3) Värvikoodide legend (kasutame hiljem graafikutes)
- Severity: Critical `#FF0000`, High `#FFA500`, Medium `#FFFF00`, Low `#0000FF`
- Action: allow `#33CC33`, deny `#CC3333`, drop `#3366CC`, alert `#FFCC00`, reset-both `#9933CC`, reset-server `#800080`
- Threat/Content Type: spyware `#3399FF`, vulnerability `#FF3333`, malware `#CC0033`, suspicious `#FFCC66`, benign `#66CC66`
- Threat Category: command-and-control `#CC0000`, code-execution `#FF6600`, sql-injection `#FF9933`, brute-force `#FFCC00`, dos `#FFFF66`, hacktool `#9933CC`, info-leak `#66CCFF`, spyware `#3399FF`, code-obfuscation `#996633`

## 4) Fookusfiltrid (24h olulisemad read)
```python
sev_col = "Severity" if "Severity" in df.columns else None
act_col = "Action" if "Action" in df.columns else None

thr_cat = df.get("thr_category", "").astype(str).str.lower()
tct_col = "Threat/Content Type" if "Threat/Content Type" in df.columns else ("threat/content type" if "threat/content type" in df.columns else None)
thr_type = df.get(tct_col, "").astype(str).str.lower() if tct_col else pd.Series([], dtype=str)

sev_mask = df[sev_col].str.lower().isin(["high","critical"]) if sev_col else False
act_mask = df[act_col].str.lower().isin(["alert","reset-both","reset-server"]) if act_col else False
cat_mask = thr_cat.isin(["command-and-control","code-execution","sql-injection","brute-force","dos","malware","spyware"])
typ_mask = thr_type.isin(["malware","vulnerability","spyware"])

focus = df[ (sev_mask) | (act_mask) | (cat_mask) | (typ_mask) ].copy()
print("Fookusread:", len(focus))
```

## 5) Kokkuvõtted tabelina
```python
print("Severity count:")
if sev_col: print(focus[sev_col].str.lower().value_counts())

print("\nAction count:")
if act_col: print(focus[act_col].str.lower().value_counts())

if tct_col:
    print("\nThreat/Content Type count:")
    print(focus[tct_col].str.lower().value_counts())

print("\nCategory count:")
print(thr_cat[focus.index].value_counts())
```

## 6) Graafikud (tulp ja pirukas)
```python
import matplotlib.pyplot as plt

# Tulp: kategooriad
thr_cat[focus.index].value_counts().plot(kind="bar", figsize=(10,5), title="Ohud kategooriate lõikes (24h)")
plt.tight_layout()
plt.savefig(BASE / "reports" / "kategooriad_24h.png")
plt.close()

# Pirukas: Threat/Content Type (kui olemas)
if tct_col:
    focus[tct_col].str.lower().value_counts().plot(kind="pie", autopct="%1.1f%%", figsize=(6,6), title="Threat/Content Type osakaal (24h)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(BASE / "reports" / "threat_type_pirukas_24h.png")
    plt.close()
```

## 7) Ekspordid (CSV/Excel)
```python
out = BASE / "processed"
out.mkdir(exist_ok=True)

# Põhifail
focus.to_csv(out / "threat_focus_2025-10-06.csv", index=False, encoding="utf-8")

# Excel-kokkuvõte (vajab openpyxl)
with pd.ExcelWriter(out / "threat_summary_2025-10-06.xlsx") as xw:
    focus.to_excel(xw, sheet_name="Focus", index=False)
    if sev_col:
        (focus[sev_col].str.lower().value_counts().rename_axis("severity").reset_index(name="count")
         ).to_excel(xw, sheet_name="Severity", index=False)
    if act_col:
        (focus[act_col].str.lower().value_counts().rename_axis("action").reset_index(name="count")
         ).to_excel(xw, sheet_name="Action", index=False)
    if tct_col:
        (focus[tct_col].str.lower().value_counts().rename_axis("type").reset_index(name="count")
         ).to_excel(xw, sheet_name="ThreatType", index=False)
```

## 8) Valepositiivid (mida kontrollida)
- Pilveteenused/CDN (Google, Microsoft, AWS, Cloudflare) — sagedased FP
- Monitooring/backup aknad — maht suur, kuid legitiimne
- Pen-test/hooldusaknad — küsi tiimilt, kas planeeritud
- Kui `Action=alert` ja muud tõendid puuduvad → võib olla FP, kinnita OSINT-iga

## 9) Järgmised sammud
- Lisa tulemused raportisse `reports\Raport_24h_2025-10-06.md`
- Võrdle eelmise päevaga (koosta tabel/graafik)
