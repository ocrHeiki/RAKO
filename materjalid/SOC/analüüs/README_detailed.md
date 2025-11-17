
# SOC Threat Analyser v5.1 – ÜLIPÕHJALIK DETAILNE SELGITUS  
**Täielik arhitektuuri ja koodimoodulite dokumentatsioon**

---

# 📌 SISUKORD
1. Ülevaade  
2. Arhitektuuriskeem  
3. Failistruktuur  
4. Koodimoodulid (ridade kaupa selgitused)  
5. Andmetöötluse töövoog  
6. Trendianalüüsi selgitus  
7. Threat Vault integratsioon  
8. GeoIP mock ja miks seda vaja on  
9. MITRE ATT&CK rikastus  
10. Normaliseerimine ja veerunimede tuvastamine  
11. Graafikute süsteem (bar/line)  
12. Raportite generaator (TXT / DOCX / XLSX)  
13. Laiendused ja arhitektuursed soovitused  
14. Vead ja nende lahendamine  

---

# 1. Ülevaade
See dokument selgitab *iga peamist loogikaploki*, *andmestruktuuri* ja *funktsiooni*, mis moodustavad tööriista **SOC Threat Analyser v5.1**.

Eesmärk on, et:
- kasutaja saab vajadusel *koodi muuta*,
- mõistab *täpselt*, miks igat moodulit kasutatakse,
- oskab analüsaatorit laiendada (nt SIEM liidestus, Elastic, GeoIP2 jms).

---

# 2. Arhitektuuriskeem (ASCII)

```
             ┌────────────────────────┐
             │ raw/*.csv (Palo Alto)  │
             └───────────┬────────────┘
                         ▼
                ┌──────────────────┐
                │ Andmete laadimine │
                └──────────┬───────┘
                           ▼
             ┌─────────────────────────────┐
             │ Ajavahemiku filter (24/7/30)│
             └───────────┬────────────────┘
                         ▼
        ┌──────────────────────────────────────────┐
        │ Veergude tuvastamine ja normaliseerimine │
        └─────────────────┬────────────────────────┘
                          ▼
                 ┌──────────────────┐
                 │ MITRE mapping    │
                 └───────┬──────────┘
                         ▼
                  ┌───────────────┐
                  │ GeoIP mock     │
                  └──────┬────────┘
                         ▼
            ┌────────────────────────────┐
            │ Threat Vault päring + cache│
            └───────────┬────────────────┘
                         ▼
               ┌──────────────────┐
               │ Trendianalüüs    │
               └────────┬─────────┘
                        ▼
       ┌──────────────────────────────────────┐
       │ Graafikud (reports/, trendid/)       │
       └────────────────────┬─────────────────┘
                            ▼
         ┌──────────────────────────┐
         │ TXT / DOCX / XLSX output │
         └──────────────────────────┘
```

---

# 3. Failistruktuur

```
projekt/
├── raw/                     # Sisendlogid
├── reports/                 # Graafikud
├── trendid/                 # Trendigraafikud
├── tulemused/               # TXT, DOCX, XLSX
├── threat_vault_cache/      # API vastuste cache
└── src/
     └── soc_analyser.py     # Peamine skript
```

---

# 4. Koodimoodulid — RIDADE KAUPA SELGITUSED

## 4.1 Importid
Selgitus:

- **pandas** – 90% analüütikast; tabeleid, grupeerimist, filtrit  
- **matplotlib.pyplot** – graafikud  
- **requests** – Threat Vault API päringud  
- **json, os, sys, argparse** – süsteem, failid, CLI argumendid  
- **docx (python-docx)** – DOCX raport  
- **openpyxl / pandas ExcelWriter** – XLSX raport  
- **datetime** – kuupäeva-parsimine trendi jaoks  

Kõik impordid on vajalikud; mõni täidetakse ainult teatud funktsioonis.

---

# 4.2 CLI parser

CLI parser lisab argumendid:

| Argument | Vaikeväärtus | Selgitus |
|---------|--------------|----------|
| `--timeframe` | `7d` | 24h / 7d / 30d analüüs |
| `--output` | detailed | tekstiraportite detailsus |
| `--strict-local` | False | karmistatud reeglid Prantsusmaa/Réunion puhul |

CLI parser tagastab `args`, mida kasutatakse `main()` funktsioonis.

---

# 4.3 Kaustade loomine

Automaatne kaustade loomine:

```
for folder in [raw, reports, tulemused, cache, trendid]:
    os.makedirs(folder, exist_ok=True)
```

Tagab, et skript *ei kuku läbi* isegi tühjas projektikaustas.

---

# 4.4 Veerunimede tuvastamine

Mida teeb?

- Palo Alto logide eksportides võivad veerud olla eri nimede all.
- Funktsioon `first_existing(df, [..])` tagastab esimese sobiva.

Näide:

```
source_col = first_existing(df, ["Source address", "src"])
```

See muudab skripti ühilduvaks **erinevate eksportversioonidega**.

---

# 4.5 Normaliseerimine

Funktsioon `norm_lower(x)` teeb:

- muudab väärtused väikesteks tähtedeks
- eemaldab whitespace
- standardiseerib võrdlusloogika

Kogu severity/action logic töötab pärast seda identse formaadiga.

---

# 4.6 MITRE ATT&CK rikastus

`attck_mapping = { "Brute Force": "T1110", ... }`

- märksõna → MITRE ID  
- otsing toimub, kui threat-nimi sisaldab võtit  
- tagastatakse `Txxxx` või `None`

Lihtne, aga laiendatav.

---

# 4.7 GeoIP MOCK

Miks mock?

- MaxMind GeoLite2 vajab registreerimist ja lisafaile
- Sinu projekt **tohib töötada offline**
- SOC õppematerjalis ei ole vaja päris GeoIP täpsust

Lahendus:

```
predefined_geo = {
   "FR": "France",
   "RE": "Réunion",
   ...
}
```

Tuvastamine põhineb IP prefiksil (nt "192.0").

Soovi korral saab selle hiljem asendada päris GeoIP DB-ga.

---

# 4.8 Threat Vault API + CACHE

## Loogika:
1. Kontrolli, kas JSON on juba cache'is.  
2. Kui jah → lae lokaalselt.  
3. Kui mitte → tee HTTP päring.  
4. Vea korral → tagasta tühi dict.  
5. Salvesta vastus lokaalselt.

Cache struktuur:

```
threat_vault_cache/
└── Brute Force.json
└── SQL Injection.json
```

---

# 4.9 Trendianalüüsi moodul

## Samm-sammuline protsess:
1. Konverteeri `log_date` → Timestamp  
2. Arvuta `week_start = date - weekday`  
3. GroupBy:
   - nädal → alert'ide arv
   - nädal + threat → top5 threatide trend

## Väljund:
- PNG graafikud kausta `trendid/`
- Tekstiline kokkuvõte, mis lisatakse TXT/DOCX/XLSX raportisse

---

# 4.10 LOW-SEVERITY analüüs

Miks vaja?

- LOW seeria sisaldab tihti:
  - skanneerimisi  
  - pordi-uuringuid  
  - automaatseid vale-positiivseid  
- Kõrgete severity-de olukord on nagunii nähtav

Moodul analüüsib:
- top pordid `destination_port`
- päeva tunnid (heatmap-i analoog)
- top rules

---

# 4.11 Graafikud

`bar(df, x, y, title, outfile)`:

- universaalne funktsioon tulpdiagrammide jaoks
- kasutab severity värvikoodi
- salvestab PNG formaati
- ei kuva GUI-d (tähtis automation jaoks)

---

# 4.12 Raportite genereerimine

### TXT
Lihtne tekstifail  
+ trendi tulemus  
+ top threats  
+ main stats

### DOCX
- Wordi dokumendis on:
  - pealkiri  
  - graafikud  
  - detailtabelid  
  - MITRE info  
  - Threat Vault kirjeldused  

### XLSX
- Tabelid:
  - Severity
  - Action
  - Top Threats
  - Trend Volume
  - Trend TOP5

---

# 5. Andmetöötluse töövoog

1. Lae CSV-d  
2. Ühenda DataFrame  
3. Filtreeri timeframe  
4. Normaliseeri veerud  
5. Rikasta (MITRE, GeoIP, Threat Vault)  
6. Arvuta statistika  
7. Tuvasta mustrid  
8. Genereeri raportid  
9. Salvesta logid

---

# 6. Laiendussoovitused

- **Elasticsearch versioon**  
- **Kibana dashboard**  
- **Failbeat → Logstash → Elasticsearch pipeline**  
- **Automaatne e-maili saatmine raportiga**  
- **Docker Compose deploy**  

---

# 7. Vead ja nende lahendamine

| Probleem | Põhjus | Lahendus |
|---------|--------|----------|
| CSV veerunimi ei leitud | Palo Alto eksportinimesed muutunud | Lisa alias `first_existing()` funktsiooni |
| Threat Vault API error | Palo Alto API piirang | Cache tagab, et skript ei peatu |
| Trendianalüüs ei tööta | Kuupäev valeformaadiks jäänud | Kasuta `to_datetime(errors='coerce')` |

---

# LÕPPSÕNA

See dokument katab kogu skripti arhitektuuri, töövoo ja funktsionaalsuse.  
Sobib nii **õppimiseks**, **koodi muutmiseks** kui ka **projekti edasiarendamiseks**.

Materjalid koostatud GitHubi kasutaja **ocrHeiki** õpiprojekti tarbeks.
