# 🛡️ SOC Workflow – Palo Alto Threat Alertide analüüs ja valepositiivide vähendamine  

**Autor:** [ocrHeiki](https://github.com/ocrHeiki)  
**Versioon:** v1.0 — 2025-10-17  

---

## 📘 Üldine kirjeldus

See repo ja juhendikogu on osa SOC (Security Operations Center) töövoost, mille eesmärk on:  

- **Mõista ja analüüsida** igapäevaseid **Palo Alto Threat Alert** sündmusi  
- **Vähendada valepositiivide hulka** ja **selgitada nende põhjuseid**  
- **Luua tööriistad ja juhendid**, mis toetavad L1 analüütikuid igapäevases töövoos  
- **Anda võrguosakonnale** selge info, millised alertid vajavad täpsustamist või tuunimist  

---

## ⚙️ SOC Workflow etapid

| Etapp | Fail / Kaust | Kirjeldus |
|-------|---------------|-----------|
| **1️⃣ SOC_WORKFLOW_01 – 24h ja Week kokkuvõtted** | `soc_l1_24h_week_summary.py` | Loeb `raw/` kaustast Palo Alto logid, loob kokkuvõtted ja graafikud (TOP Threat/Content + Source IP). |
| **2️⃣ SOC_WORKFLOW_02 – OSINT ja enrichment** | `soc_top10_osint.py` | Võtab eelmise etapi tulemused (TOP 10 IP) ja rikastab neid OSINT andmetega (AbuseIPDB, VT, OTX jne). |
| **3️⃣ SOC_WORKFLOW_03 – Manual OSINT / L1 käsitsi analüüs** | `SOC_L1_Manual_OSINT_Jatk.md` | Juhend olukorraks, kus automaatset OSINT-i ei saa kasutada – samm-sammuline FP ja signatuurianalüüs. |
| **4️⃣ SOC_WORKFLOW_04 – Võrgu tagasiside ja tuning** | (plaanis) | Koostatakse raportid võrgutiimile: milliseid reegleid täpsustada või eemaldada. |
| **5️⃣ SOC_WORKFLOW_05 – SIEM / Alert Lifecycle jälgimine** | (plaanis) | Juhend ja tööriistad L1 → L2 → L3 käsitluse jaoks (alertist kuni järelduseni). |

---

## 🎯 Eesmärk

> SOC Workflow on loodud selleks, et **igapäevaste alertide mahu vähendamine** oleks süstemaatiline ja dokumenteeritud.  
> Me ei kustuta alerte pimesi – me **analüüsime põhjuseid**, **tuvastame korduvaid mustreid**, ja **anname võrguosakonnale** täpsed soovitused signatuuride või reeglite muutmiseks.

---

## 🧠 SOC rollid ja vastutus

| Tase | Roll / Peamine tegevus | Vastutus |
|------|-------------------------|-----------|
| **L1 – SOC analüütik (sina)** | Logide jälgimine, valepositiivide analüüs, OSINT | Esmane alertide kontroll ja filtreerimine |
| **L2 – Incident Responder** | Alertide kinnitamine, triage, logide ristviited | Reageerimine ja tõsisemate intsidentide käsitlus |
| **L3 – Threat Hunter / Engineer** | Püsivate ohtude jahindus, SIEM reeglite parendamine | Süvitsi uurimine, automatiseerimine |
| **NetSec / Võrguosakond** | Firewall ja reeglite haldus | Reeglite korrigeerimine ja signatuuride tuning |
| **Forensics / IR** | Tõendite kogumine ja intsidentide järelanalüüs | Eskaleeritud juhtumite tehniline tõendus |

---

## 🧰 Vajalikud kaustad ja struktuur

```
SOC/
├── raw/                     # Palo Alto logide lähtefailid (CSV)
├── scripts/                 # Kõik töövoo skriptid (SOC_WORKFLOW_01, 02, ...)
├── tulemused/               # Aruanded, CSV, DOCX, TXT
├── docs/                    # Markdown juhendid (nt SOC_L1_Manual_OSINT_Jatk.md)
├── reports/                 # Word/PDF raportid
└── README.md                # See fail
```

---

## 🧮 Kasutatavad tööriistad

- **Python (standard)** – logide ja IP analüüs  
- **Graylog (testkeskkond)** – visuaalne logivaade  
- **Wireshark** – võrgupakettide kontroll (L2-L3 tasemel)  
- **OSINT tööriistad:** AbuseIPDB, VirusTotal, OTX, Talos, GreyNoise, Shodan  
- **Palo Alto Threat Vault** – signatuuride kirjeldused  
- **Word** – SOC raportid ja FP dokumentatsioon  

---

## 📈 Tulemus

Kui töövoog on korrektselt rakendatud:
- igapäevaste alertide **maht väheneb** (FP eemaldamisega)  
- alertide **täpsus suureneb**  
- SOC ja võrguosakonna vaheline **koostöö paraneb**  
- raportid muutuvad **standardi järgi korratavateks**  

---

## 📄 Märkus

Kõik failid ja juhendid selles projektis on koostatud õppe- ja arenduseesmärgil.  
Materjalide sisu põhineb SOC L1-L3 töövoo metoodikal ja Palo Alto logianalüüsi praktikal.  

---

🧑‍💻 **Autor:** [ocrHeiki](https://github.com/ocrHeiki)  
📅 **Versioon:** 2025-10-17  
📂 **Fail:** `README.md`
