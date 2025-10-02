# Etapp 3 — Visualiseerimine (graafikud ja trendid)

Selles etapis õpid looma graafikuid, et näidata Palo Alto logide analüüsi tulemusi.  
Graafikuid saab teha **Excelis** või **Google Sheetsis**, hiljem kopeerida need Wordi raportisse või salvestada piltidena Markdowni jaoks.

---

## 1. Riskitasemete pirukas Excelis

1. Ava logide tabel Excelis.  
2. Lisa uus veerg `Severity` ja märgi sinna väärtused (🔴 Critical, 🟧 High, 🟨 Medium, 🔵 Low).  
3. Tee Pivot Table:  
   - **Rows** → Severity  
   - **Values** → Count of Sessions (või mõni sobiv veerg, nt `App Sessions`)  
4. Vali **Insert → Pie Chart → 2D Pie**.  
5. Lisa värvid käsitsi:  
   - 🔴 Critical → Red  
   - 🟧 High → Orange  
   - 🟨 Medium → Yellow  
   - 🔵 Low → Blue  
6. Lisa Chart Title: *Riskitasemete jaotus (24h)*.

---

## 2. Top Source IP tulpdiagramm

1. Sorteeri logi `Source IP` järgi ja loe, mitu korda igaüks esineb.  
2. Tee Pivot Table:  
   - **Rows** → Source IP  
   - **Values** → Count of Source IP  
3. Sorteeri suurimast väiksemani ja võta Top 10.  
4. Vali **Insert → Column Chart → Clustered Column**.  
5. Lisa Chart Title: *Top Lähte IP-d (24h)*.

---

## 3. Top Destination IP tulpdiagramm

1. Sama loogika nagu Source IP puhul, aga `Destination IP`.  
2. Tee Pivot Table, loe seansid.  
3. Sorteeri suurimast väiksemani, vali Top 10.  
4. Insert → Column Chart.  
5. Lisa Chart Title: *Top Siht IP-d (24h)*.

---

## 4. Sessions tunnis ajajoon

1. Veendu, et sul on olemas veerg `Timestamp`.  
2. Loo Pivot Table:  
   - **Rows** → Hour (Group by Hour)  
   - **Values** → Count of Sessions  
3. Insert → Line Chart.  
4. Lisa Chart Title: *Seansside arv tunnis*.  
5. See graafik aitab tuvastada tipptunnid või anomaaliad.

---

## 5. 7 päeva trend

1. Võta 7 järjestikust 24h logi.  
2. Iga päeva kohta arvuta Severity põhjal: Critical, High, Medium, Low arvud.  
3. Pane tulemused tabelisse (päevad X-teljel, arvud Y-teljel).  
4. Insert → Line Chart (mitme seeriaga).  
5. Lisa legend:  
   - 🔴 Critical  
   - 🟧 High  
   - 🟨 Medium  
   - 🔵 Low  
6. Lisa Chart Title: *7 päeva trend — intsidentide arv severity kaupa*.

---

## 6. Raporti koostamine

- Kui graafikud on valmis, vali **Copy → Paste as Picture** ja kleebi need Wordi raportisse.  
- Markdown raporti jaoks salvesta graafikud PNG-piltidena (`Save as Picture`) ja lisa need `pildid/` kausta.  
- Raportis märgi iga graafiku alla lühike kirjeldus, mida graafik näitab (nt „DNS liiklus kasvas 23:00 paiku”).

---
