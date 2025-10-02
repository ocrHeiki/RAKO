# Palo Alto 24h Raporti Mall

## 1. Sissejuhatus
- Lühikirjeldus logidest (nt „analüüsitud periood: 01.10.2025 – 24h logid Palo Alto firewallist”).
- Märgi ära, kas tegemist on tööpäeva, nädalavahetuse või muu kontekstiga.

## 2. Graafikud ja visualiseerimine
- **Pirukas** riskitasemete jaotusega (🔴 🟧 🟨 🔵).
- **Top Source IP** tulpdiagramm.
- **Top Destination IP** tulpdiagramm.
- **Sessions / Hour** ajajoon (millal liiklus kasvas).

👉 Kasutada saab Excelit, Pandast või mõnda SIEM-i tööriista.

## 3. 24h võrdlus eelmise päevaga
- Kas riskide arv on suurenenud või vähenenud?
- Kas esineb korduvaid allikaid (sama IP, sama domeen)?
- Kas liiklusmustrid erinevad (nt rohkem DNS päringuid öösel)?

## 4. 7 päeva kokkuvõtte võrdlus
- Võrdle nädalas kõiki päevi (graafik + tabel).
- Märgi trendid:
  - kas rünnakud kasvavad või vähenevad?
  - millised ohutüübid domineerivad?
- Lisa line chart, kus X-telg on päevad (7 päeva), Y-telg on intsidentide arv severity kaupa.

## 5. Valepositiivid
- Märgi, millised IP-d/domeenid osutusid **legitiimseks** (nt CDN, Google DNS, Microsoft Azure).
- Lisa põhjendus, miks see false positive on.

## 6. Järeldused ja soovitused
- Millised alertid vajavad eskaleerimist?
- Millised trendid on riskantsed (nt korduvad SSL rünnakukatsed)?
- Kas soovitatav on reeglite muutmine Palo Alto firewallis?
