# SOC Analyst Workflow – Valepositiivsete Tuvastamise Automaatika  
### Autor: ocrHeiki  
### Versioon: Dokumenteeritud töövoog (2025)

---

# 📌 Ülevaade  
See README kirjeldab minu praktilist töövoogu SOC-analüütikuna, kelle igapäevaseks ülesandeks oli tuvastada **Palo Alto häirete seast valepositiivseid tulemusi**, optimeerida analüüsi ning lõpuks automatiseerida kogu protsess.

Töövoog algas **käsitsi CSV-failide puhastamisest**, kasvas **poolautomaatseks otsinguskriptiks**, ja arenes lõpuks tänaseks **täisautomaatsesse SOC Threat Analyser v6.x** süsteemi, mis toodab mahukaid, struktureeritud ja visuaalseid aruandeid.

---

# 🧭 1. Algus – Manuaalne CSV analüüs  
Alguses nägi töö välja nii:

- Palo Alto logid tulid **toorestena CSV kujul**  
- veerud olid ebaühtlased, 
- tuli käsitsi puhastada, sorteerida ja filtreerida  
- otsida korduvaid mustreid Exceli filtrite kaudu  
- lisada värvikoodid, pivot-tabelid, kokkuvõtted

👉 *Kõik oli aeglane, haavatav vigadele ja raske automatiseerida.*

### Mida tuli otsida?
- korduvad häired samalt IP-lt  
- kahtlased kategooriad (hacktool, dos, code-execution jne)  
- action väärtused (alert, reset-both, drop jne)  
- severity jaotus  
- sagedased valepositiivsed mustrid, nagu:
  - mass-pordi skanneerimine
  - teadaolevad automatiseeritud bot-id
  - “noise traffic” teenustelt
  - sisemised testiserverid  

---

# ⚙️ 2. Esimene automatiseerimise katse – käsurea filtrid  
Edusammud:

- õppisin kasutama Pythonit väikeste ühekordsete skriptide jaoks  
- lugesin CSV sisse  
- kasutasin `.query()` ja `.value_counts()`  
- sain esimesed automaatsed top10 tabelid  
- raport mahtus **ühele lehele** – lihtne, kuid piiratud

Näide varasemast skriptist:

```python
df = pd.read_csv("palo.csv")
print(df["Severity"].value_counts())
print(df["Threat/Content Name"].value_counts().head(10))
```

See oli suur hüpe, sest:
- kadus käsitsi sorteerimise vajadus  
- tulemused muutusid ühtlasemaks  
- valepositiivsed muutusid kergemini leitavaks  

---

# 🚀 3. Automatiseerimine v2 – Täpsed otsingud & tokenizer  
Töövoog paranes:

- lisandus automaatne **normaliseerimine** (väiketähed, strip)  
- sain kätte õiged **veerud sõltumata CSV nimetustest**  
- skript hakkas otsima:
  - threat nimede kordusi
  - portide mustreid
  - IP → kategooriate seoseid

Lisandus automaatne:

- top threats  
- top IPd  
- action jaotus  
- severity jaotus  

Raport muutus juba 2–3 lehekülje pikkuseks.

---

# 📊 4. SOC Threat Analyser – täisautomaatne tööriist  
Töövoog jõudis punkti, kus:

### ✔ Skript toetab:  
- 24h / 7d / 30d analüüsi  
- veeru automaatset tuvastust  
- GeoIP (mock)  
- Threat Vault cache  
- TOP 10 tabelid:
  - source IP
  - destination IP
  - threatid
  - failid  
- kategooriate analüüs  
- trendid nädalate lõikes  
- threat-port mapping  

### ✔ Mitmed väljundid:
- TXT
- DOCX (graafikutega)
- XLSX (tabelitega)
- PNG graafikud

### ✔ Raportid ei ole enam 1 lk, vaid 6–20 lk
See muutis valepositiivsete otsimise:

- *kiiremaks*  
- *täpsemaks*  
- *järjepidevaks*  
- *auditeerimiseks sobivaks*  

---

# 🛡️ 5. Valepositiivsete leidmine täna  
Tänu uuele töövoole saan automaatselt tuvastada:

## 🟥 1) Korduvad madala severity’ga häired  
Need tulevad tavaliselt:

- sisevõrgust
- teadaolevatest botnet scanneritest
- legitiimsetest teenustest

## 🟧 2) Port mustrite anomaaliad  
Näiteks:

- 6000 kirjet port 0 tegevusest  
- testiserverid, mis saadavad noisy liiklust  

## 🟨 3) Threat kategooriad, mis ei ole reaalselt ohtlikud  
Nagu:

- hacktool (tihti mehaanilised skanneerijad)
- dos (tihti ping-flood testid)
- brute-force (tasemel 1/10 – enamasti noise)

## 🟦 4) IP → Category → Threat seosed  
Võimaldab näha:

- kas üks IP tekitab eri kategooriaid  
- kas threat on süsteemne (päris rünnak) või juhuslik  

---

# 🧩 6. Mida see töövoog mulle õpetas  
- logianalüüs on 80% andmepuhastus, 20% tuvastus  
- normaliseerimine = kõige olulisem etapp  
- automatiseerimine tuleb väikeste sammudega  
- hea raport vähendab tööaega 10×  
- valepositiivsed on selged, kui statistika on õige  

---

# 🏁 7. Kokkuvõte  
Täna ei ole vaja:

❌ käsitsi CSV faile puhastada  
❌ otsida threat’e mille nimed on valesti vormindatud  
❌ teha Excelis pivot-tabeleid  
❌ värvida severity lahte käsitsi  

Kogu töö:

✔ toimub automaatselt  
✔ on reprodutseeritav  
✔ annab samad tulemused iga kord  
✔ toob välja nii reaalsed ohud kui valepositiivsed  
✔ genereerib mitmelehelise professionaalse raporti  

---

# 📎 Fail  
Fail on allalaadimiseks valmis.

