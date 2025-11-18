# SOC Threat Analyser — v6.2 (2025-11-18)
Autor: ocrHeiki / GitHub

## Kirjeldus

SOC Threat Analyser v6.2 automatiseerib Palo Alto tulemüüri logide analüüsi ja koostab täisväärtusliku SOC-taseme raporti (DOCX, TXT, XLSX).
See sobib kasutamiseks turbeanalüütikutele, SOC-tiimidele, intsidentide käitlejatele ja automatiseeritud seireks.

Versioon 6.2 parendused:
- Destination IP analüüs (uued tabelid + võrdlus Source IP-dega)
- Selgem ja paremini jaotatud DOCX raport
- Täiendatud severity/action/category analüüs
- Täpsem threat–IP korrelatsioon
- Lisatud koodikommentaarid ja diagnostika

---

# Funktsionaalsused

## 1. CSV logide töötlemine
- Töötleb Palo Alto CSV logifaile
- Toetab mitme faili automaatset kombineerimist
- Tuvastab logide kuupäevad failinimest

## 2. Ajaakna filter
Toetatud ajavahemikud:
- 24h
- 7d
- 30d

Analüüsi kaasatakse ainult ajavahemikku kuuluvad logiread.

## 3. Andmete normaliseerimine
Automaatne puhastus ja normaliseerimine:
- severity
- action
- threat name
- category
- source address
- destination address

Kõik väärtused vormindatakse ühtsele kujule (lowercase, strip jne).

## 4. Statistika genereerimine
Kood arvutab:
- severity jaotus
- action jaotus
- top kategooriad
- top threatid
- top source IP
- top destination IP
- threat + port mapping
- threat + application analüüs

## 5. IP-põhine korrelatsioon
Analüüs määrab:
- millised threatid on seotud iga Source IP-ga
- milliseid Destination IP-sid rünnatakse kõige enam
- milliste kategooriatega IP-d seostuvad

## 6. Graafikute genereerimine
Luuakse PNG-formaadis graafikud:
- severity donut ja bar chart
- action pie ja bar
- top threatid
- top source IP-d
- top destination IP-d
- kategooriate jaotus
- nädalapõhine trend
- top 5 threat trend

## 7. DOCX raport
Koostatakse täisautomaatne DOCX raport, mis sisaldab:
- pealkiri ja metaandmed
- sisukord
- kokkuvõte
- detailtabelid
- source/destination IP tabelid
- trendigraafikud
- threat-port mapping
- lisainfo

## 8. TXT raport
Lühike terminalis loetav kokkuvõte.

## 9. XLSX raport
Exceli raport sisaldab:
- üldstatistika
- threats by source IP
- threats by destination IP
- detailtabelid
- port mapping

---

# Koodi tööprotsess (step-by-step)

## 1. CSV failide kontroll
Programm kontrollib, kas kaustas `~/Documents/SOC/raw/` on CSV-faile.
Kui mitte, lõpetab töö.

## 2. CSV lugemine
- Laeb kõik CSV-failid
- Lisab igale logireale `log_date` failinimest
- Kombineerib kõik DataFrame’iks

## 3. Andmete puhastamine
- täidab puuduvad väljad
- normaliseerib tekstiväljad
- teisendab kuupäevad datetime tüübiks

## 4. Ajavahemiku filter
Filtreerib ainult valitud ajavahemikku kuuluvad read (24h / 7d / 30d).

## 5. Statistika arvutamine
Kasutan Pandase funktsioone (`value_counts` jne) arvutamaks:
- severity
- action
- threat
- category
- IP aadressid

## 6. IP + threat korrelatsioon
Grupeerib threatid Source ja Destination IP järgi, et luua ülevaade:
- milline IP seostub milliste threatidega
- millised threatid on kõige aktiivsemad ründajad ja sihtmärgid

## 7. Graafikute loomine
Kasutab Matplotlibi, et luua PNG graafikuid.
Need salvestatakse kataloogi `/Documents/SOC/reports/`.

## 8. DOCX raporti genereerimine
Kasutab python-docx teeki:
- lisab pealkirjad
- lisab tekstilised ülevaated
- lisab tabelid
- lisab kõik graafikud
- salvestab faili `soc_<timeframe>_report.docx`

## 9. TXT raport
Luuakse kokkuvõte kujul `soc_<timeframe>_summary.txt`.

## 10. XLSX raport
Openpyxl abil luuakse Exceli fail, mis jagab info eraldi töölehtedele.

---

# Failistruktuur

```
~/Documents/SOC/
│
├── raw/                 # CSV logid
├── reports/             # Graafikud
├── tulemused/           # Raportid (DOCX, TXT, XLSX)
├── threat_vault_cache/  # Cache-lahendes
└── trendid/             # Trendigraafikud
```

---

# Käsurea kasutamine

Näide:

```
python soc_analyser.py --timeframe 24h
```

Toetatud argumendid:
- 24h
- 7d
- 30d

---

# Nõuded

- Python 3.9+
- Pandas
- Matplotlib
- python-docx
- openpyxl

---

# Kokkuvõte

SOC Threat Analyser v6.2 on terviklik küberturbe logide analüüsi tööriist, mis:
- automatiseerib analüüsi,
- koostab SOC-taseme raporti,
- visualiseerib andmeid,
- leiab threat-IP seosed,
- analüüsib nii Source kui Destination IP-d,
- loob professionaalse DOCX-i, TXT ja XLSX raporti.
