# `analyser.py` — Samm‑sammuline seletuskiri (v4.0)

**Eesmärk:** see skript loeb kõik **Palo Alto tulemüüri logifailid** kaustast `~/Documents/SOC/raw`, tuvastab automaatselt ajavahemiku (24h, 7 päeva, 30 päeva), arvutab kokkuvõtted (*Severity*, *Action*, *TOP loendid*), joonistab graafikud ja koostab **TXT**, **XLSX** ja **DOCX** aruanded.

Failid salvestatakse kaustadesse:
```
~/Documents/SOC/
├── raw/           ← sisesta siia CSV logifailid
├── tulemused/     ← siia tekivad aruanded
├── reports/       ← siia salvestatakse graafikud
└── scripts/       ← siia kuulub see skript
```

---

## 1) Impordid — „toome tööriistad kätte“

```python
import subprocess
import sys
import os
import importlib
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
```

- **`subprocess`** ja **`sys`** — moodulite automaatseks paigaldamiseks.
- **`importlib`** — kontrollib, kas moodul on juba paigaldatud.
- **`pathlib.Path`** — platvormist sõltumatu viis failide ja kaustade teede käsitlemiseks.
- **`pandas`** — tabelite töötlemine, CSV-de lugemine ja grupeerimine.
- **`matplotlib.pyplot`** — graafikute joonistamine.
- **`re`** — regulaaravaldiste (regexi) kasutamine: nt kuupäeva tuletamine failinimest.
- **`python-docx`** — DOCX aruannete loomine ja piltide lisamine.

---

## 2) Põhikaustad ja ettevalmistus

```python
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw"
REPORTS_DIR = BASE_DIR / "reports"
RESULTS_DIR = BASE_DIR / "tulemused"
for d in [RAW_DIR, REPORTS_DIR, RESULTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)
```

- **`BASE_DIR`**: projektikaust `SOC/`
- Skript loeb logifailid **ainult kaustast `raw/`**, ignoreerides `varasemad_logid/`.
- Kui kaustasid pole, **loodakse need automaatselt**.

---

## 3) Ajavahemiku tuvastus

```python
def detect_time_range(dates):
    if not dates: return "24h"
    min_date = min(dates)
    max_date = max(dates)
    diff_days = (max_date - min_date).days + 1
    return "24h" if diff_days <= 1 else "7 päeva" if diff_days <= 7 else "30 päeva" if diff_days <= 31 else f"{diff_days} päeva"
```

- Loetud logifailide kuupäevade põhjal **tuvastatakse ajavahemik** (nt 24h või 7 päeva).
- Raportitele antakse vastav pealkiri (nt "`SOC 7 päeva aruanne`").

---

## 4) Värvikaardid — „mis värv tähendab mis asja?“

```python
COLORS_SEV = {"low": "#0000FF", "medium": "#FFFF00", "high": "#FFA500", "critical": "#FF0000"}
COLORS_ACTION = {"allow": "#33CC33", "deny": "#CC3333", "drop": "#3366CC", "alert": "#FFCC00", "reset-both": "#9933CC"}
COLORS_CAT = {"hacktool": "#9933CC", "dos": "#FFFF66", "info-leak": "#66CCFF", "code-execution": "#FF6600"}
```

- Need on värvikoodid **Severity**, **Action** ja **kategooriate** jaoks.
- Vajalikud graafikute **loogiliseks värvimiseks**.

---

## 5) MITRE ATT&CK kaardistus

```python
attck_mapping = {
    "Nmap Aggressive Option Print Detection": {"tactic": "Discovery", "technique": "T1046"},
    "Microsoft Windows RPC Encrypted Data Detected": {"tactic": "Execution", "technique": "T1059"},
    "SSL Double Client Hello Cipher Suite Length Mismatch": {"tactic": "Defense Evasion", "technique": "T1071"},
    "HTTP2 Protocol Suspicious RST STREAM Frame detection": {"tactic": "Defense Evasion", "technique": "T1071"},
    "Windows Local Security Authority lsardelete access": {"tactic": "Credential Access", "technique": "T1003"}
}
```

---

## 6) Valepositiivse riski hinnangud – 16 threatile

```python
fp_guidance = {
    "Nmap Aggressive Option Print Detection": {
        "risk": "KÕRGE",
        "reason": "Sageli kasutavad seda legitiimsed süsteemihaldurid või turvameeskonnad skaneerimiseks.",
        "tip": "Kontrolli IP konteksti ja kas see kuulub ettevõttesse. Mitte alati oht – võib viidata pentestile."
    },
    "SIP Register Message Brute Force Attack": {
        "risk": "KESKMINE",
        "reason": "SIP-serverid saavad sageli vigaseid päringuid isegi ilma ründeta.",
        "tip": "Vaata, kas IP kuulub tuntud kliendivõrku või partnerile. Mõnikord valed konfiguratsioonid."
    },
    "OpenSSL Handshake Cipher Two More Times Changed Anomaly": {
        "risk": "MADAL–KESKMINE",
        "reason": "Võib olla tegu ainult ühilduvus veaga klientrakenduses (nt vana seade).",
        "tip": "Kontrolli seadetüüpe, mis loovad ühendust ja nende OpenSSL versioone."
    },
    "FTP REST": {
        "risk": "KÕRGE",
        "reason": "Täiesti legitiimne käsk, mida kasutavad backup- ja failisüsteemid.",
        "tip": "Kontrolli, kas FTP kasutatakse sisemiselt või väliselt. Tõeline oht vaid kui jagatakse tundlikku infot."
    },
    "Windows Local Security Authority lsardelete access": {
        "risk": "KESKMINE",
        "reason": "Sageli legitiimne haldustegevus või teenuste skaneerimine.",
        "tip": "Vaata, kas tegu oli süsteemihalduri tegevusega ja kas IP kuulub sisepiirkonda."
    },
    "SMB: User Password Brute Force Attempt": {
        "risk": "MADAL–KESKMINE",
        "reason": "Sageli tekib siis, kui lõppkasutaja sisestab valesti parooli korduvalt.",
        "tip": "Vaata kas IP kuulub sisepiirkonda – tõeline oht ainult väljast."
    },
    "SSL Double Client Hello Cipher Suite Length Mismatch": {
        "risk": "MADAL",
        "reason": "Võib olla seotud mõne ebatavalise või vananenud klientrakendusega.",
        "tip": "Vaata, millise brauseri või rakendusega loodi ühendus."
    },
    "Cisco Malformed SNMP Message Format String Vulnerability": {
        "risk": "KESKMINE",
        "reason": "Sageli esineb vigaste seadmete puhul (nt printerid, haldusliidesed).",
        "tip": "Kontrolli, kas IP kuulub Cisco seadmete haldusvõrku."
    },
    "Suspicious User-Agent Strings Detection": {
        "risk": "KÕRGE",
        "reason": "Paljud analüüsi- ja automatiseeritud tööriistad kasutavad samu stringe – nt curl, wget.",
        "tip": "Ava IP-logid ja leia täpne brauseri nimi – mitte alati spyware."
    },
    "HTTP2 Protocol Suspicious RST STREAM Frame detection": {
        "risk": "KESKMINE",
        "reason": "Sageli esineb halvasti programmeeritud rakendustes.",
        "tip": "Vaata, kas tegu oli rakenduse vigadega, mitte ainult pahavara vastu."
    },
    "Kahtlane PowerShell-i käivitus": {
        "risk": "KESKMINE",
        "reason": "Süsteemihaldurid kasutavad sageli PowerShelli skripte.",
        "tip": "Ava skripti sisu – kas see tuleb ettevõttesisest tühist või välisest allikast?"
    },
    "Kahtlane pikk URL koos paljude parameetritega": {
        "risk": "KÕRGE",
        "reason": "Sageli kasutatakse CMS-ides või veebivormides – pole alati ohtlik.",
        "tip": "Ava leht ja vaata URL-i sisu, kas tegu tegelikult mõõdukate parameetritega."
    },
    "Võimalik Cobalt Strike Beacon tegevus": {
        "risk": "MADAL",
        "reason": "Kui kasutatakse legitiimset red teami, siis võib olla lubatud tegevus.",
        "tip": "Vaata, kas IP kuulub soovitustele – muidu tõeline oht."
    },
    "Võimalik failide allalaadimine": {
        "risk": "KÕRGE",
        "reason": "Arendajad või süsteemid kasutavad sageli neid tööriistu.",
        "tip": "Vaata, mis fail laeti alla ja kas allikas on usaldusväärne."
    },
    "Võimalik HTTP pahatahtliku sisu tuvastamine": {
        "risk": "KESKMINE",
        "reason": "Sageli valed automaattuvastused veebiserverite puhul.",
        "tip": "Ava lehe sisu ja võrdle – kas tegu on legitiimse dünaamilise veebilehega."
    },
    "HTTP Response Content Length Too Long": {
        "risk": "KESKMINE",
        "reason": "Sageli on tegu suurte failide päringutega või API vastustega.",
        "tip": "Kontrolli, kas tegu on legitiimse API või failiteenusega."
    }
}
```

---

## 7) Abifunktsioonid

### 7.1 Kuupäeva hankimine failinimest

```python
def iso_from_filename(name: str):
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m:
        return datetime.strptime(f"{m.group(3)}-{m.group(2)}-{m.group(1)}", "%Y-%m-%d").date()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return m.group(0) if m else today.date()
```

- Proovib tuvastada kuupäeva failinimest kahe formaadiga (`dd.mm.yyyy` või `yyyy-mm-dd`).

---

### 7.2 Veerunimede tuvastus

```python
def first_existing(df, names):
    for n in names:
        if n in df.columns:
            return n
    return None
```

- Iga vajaliku veeru jaoks on loend võimalike pealkirjadest – võetakse esimene, mis eksisteerib.

---

### 7.3 Graafikute funktsioonid

```python
def bar(series, title, outpath, colors=None, rot=0):
    if series.empty: return
    plt.figure(figsize=(10, 5))
    c = [colors.get(str(i).lower(), "#888888") for i in series.index] if colors else "#888888"
    series.plot(kind="bar", color=c)
    plt.title(title)
    plt.xticks(rotation=rot)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def pie(series, title, outpath):
    if series.empty: return
    plt.figure(figsize=(6, 6))
    plt.pie(series, labels=series.index, autopct="%1.1f%%", startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def add_image(doc: Document, img_path: Path, caption: str, width_in=6.0):
    if img_path.exists():
        p = doc.add_paragraph()
        run = p.add_run()
        run.add_picture(str(img_path), width=Inches(width_in))
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cap = doc.add_paragraph(caption)
        cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
```

---

## 8) `main()` — Põhitrunk

### 8.1 Logifailide otsimine ja analüüs

```python
csv_files = list(RAW_DIR.glob("*.csv"))
if not csv_files:
    print("⚠️ Ühtegi CSV-faili ei leitud kaustas: raw/")
    return
```

- Loetleb kõik `raw/` kaustas asuvad **.csv failid**.
- **Võtab neist koos andmehulga**, mitte ainult uusima!

---

### 8.2 Veergude normaliseerimine

```python
df_all["sev_norm"] = norm_lower(df_all[sev_col])
df_all["act_norm"] = norm_lower(df_all[act_col])
...
```

- Veerute muundamine kindlasse vormi (**väiketähed**, **trimmimine**), et grupeerimised toimiksid ühtlaselt.

---

### 8.3 Statistilised andmed ja TOP loendid

```python
sev_counts = df_all["sev_norm"].value_counts()
top_threat = df_all["tname_norm"].value_counts().head(10)
top_src = df_all["src_norm"].value_counts().head(10)
top_dst = df_all["dst_norm"].value_counts().head(10)
```

- Moodustatakse **Severity**, **Action**, **TOP 10 threat name**, **allikad**, **sihtmärgid** jne.

---

### 8.4 TXT & DOCX aruanded

#### TXT aruanne

```python
with open(out_txt, "w", encoding="utf-8") as f:
    f.write(f"SOC {time_range} KOONDARUANNE – {today_str}\n")
    f.write("=" * 50 + "\n")
    ...
    f.write("\n■ Valepositiivne risk - TOP 10 Threat Name:\n")
    for i, (threat, count) in enumerate(top_threat.items()):
        if i >= 10: break
        f.write(f"\n{i+1}. {threat} – {count} korda\n")
        guide = fp_guidance.get(threat, {})
        if guide:
            f.write(f"  🔸 Valepositiivne risk: {guide.get('risk', '–')}\n")
            f.write(f"  🔸 Põhjus: {guide.get('reason', '–')}\n")
            f.write(f"  🔸 Soovitus: {guide.get('tip', '–')}\n")
        else:
            f.write("  🔸 Valepositiivse riski info puudub.\n")
```

#### DOCX

```python
doc.add_heading("Valepositiivne risk – TOP 10 Threat Name", level=2)
for i, (threat, count) in enumerate(top_threat.items()):
    if i >= 10: break
    doc.add_paragraph(f"{i+1}. {threat} – {count} korda")
    guide = fp_guidance.get(threat, {})
    if guide:
        doc.add_paragraph(f"🔸 Valepositiivne risk: {guide.get('risk', '–')}", style='Intense Quote')
        doc.add_paragraph(f"🔸 Põhjus: {guide.get('reason', '–')}")
        doc.add_paragraph(f"🔸 Soovitus: {guide.get('tip', '–')}")
    else:
        doc.add_paragraph("🔸 Valepositiivse riski info puudub.")
    doc.add_paragraph("")
```

---

### 8.5 Graafikud ja XLSX

- Graafikute loomine: `bar()`, `pie()`
- XLSX faili export: `pd.ExcelWriter`

---

## 9) Käivitamine

1. **Paiguta logifailid** kausta `raw/`
2. Ava terminal:

   ```bash
   cd ~/Documents/SOC/scripts
   python analyser.py
   ```

3. Vaata tulemusi:
   - `~/Documents/SOC/tulemused`
   - `~/Documents/SOC/reports`

---

## 10) Seletuskiri terminitele

- **`normalize`** – andmete ühtlustamine (väiketähed, trimmimine)
- **`value_counts()`** – loendamine
- **`groupby`** – grupeerimine
- **CSV / DOCX / XLSX / PNG** – standardvormingud

---

## 11) Miks just nii?

- **Lihtne ja laiendatav**
- **Tugineb ainult `raw/` kaustale**
- **MITRE + Valepositiivne hinnang ⇒ kiire analüüs**

---

Valmis!
