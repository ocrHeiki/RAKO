# 📑 SOC L1 Workflow — Samm-sammuline juhend (täpse menüüdega)

## 1. CSV import Excelisse
1. Ava Excel.  
2. Mine ülemises ribas **Data → Get Data → From File → From Text/CSV**.  
   _(Excel 365-s: **Data → Get Data → From Text/CSV**)_.  
3. Vali **logifail** (nt `paloalto-threat-2025-09-26.csv`).  
4. Kui avaneb aken:  
   - **File Origin** = UTF-8  
   - **Delimiter** = Comma (,)  
   - Kontrolli eelvaates, et väljad jagunevad õigesti (nt `SourceIP`, `DestinationIP`, `ThreatName`).  
5. Vajuta **Load**.  

---

## 2. Vormindus (andmete ettevalmistamine)
- Mine menüüsse **Home → Editing → Sort & Filter → Filter**.  
- Lisa **Filter** igale veerule.  
- Mine menüüsse **View → Freeze Panes → Freeze Top Row**, et päis jääks alati nähtavaks.  
- Salvesta kohe fail: **File → Save As → Excel Workbook (.xlsx)**.  

---

## 3. Tingimuslik vormindamine (värvidega silmatorkavamaks)
1. Vali veerg **Severity** (nt `Critical`, `High`, `Medium`, `Low`).  
2. Mine **Home → Styles → Conditional Formatting → Highlight Cell Rules → Text that Contains…**  
   - Critical → vali **punane täitevärv**  
   - High → vali **oranž täitevärv**  
   - Medium → vali **kollane täitevärv**  
   - Low → vali **roheline täitevärv**  
3. Sama loogikat saad kasutada veeru **Action** jaoks (Allow = roheline, Block = hall või punane).  

---

## 4. Filtreerimine
- Kliki päisereal filtriikoonile.  
- Filtreeri esmalt **Severity = Critical või High**.  
- Vali veerust **SourceIP** ja kasuta „Sort Largest to Smallest“ või „Filter by Count“, et näha korduvaid IP-sid.  
- Vajadusel lisa **Text Filter → Contains…** või **Does Not Contain…** false positive’ide eemaldamiseks.  

---

## 5. Pivot Table raport
1. Märgi kogu tabel (Ctrl + A).  
2. Mine menüüsse **Insert → PivotTable**.  
3. Aknas vali:  
   - **Rows → Threat Category**  
   - **Columns → Severity**  
   - **Values → Count of Events**  
4. Nüüd näed tabelit, mis koondab ohud kategooriate kaupa.  

---

## 6. Graafikud
- Kliki Pivot tabeli sisse.  
- Mine **Insert → Charts → Column (Clustered Column)** või **Pie (2-D Pie)**.  
- Vali graafikule **Chart Design → Add Chart Element → Data Labels**, et näeksid ka arve.  

---

## 7. Analüüsi tegevused
- Ava `analüüs/SOC_LogiFaili_Analüüsi_Template.md`.  
- Täida iga sektsioon (Faili andmed, Alertide jaotus, Korduvad ohud, Allikad, Eskaleerimine jne).  
- Salvestatud raport jääb praktikakoha jaoks (päevik eraldi, mitte GitHubi!).  

---

## ⚡ Kiirklahvid SOC Exceli töövoos
- **Ctrl + A** → vali kogu tabel  
- **Ctrl + T** → teisenda tabeliks (Excel Table)  
- **Alt + N + V** → lisa Pivot Table  
- **Alt + N + C** → lisa Column Chart  
- **Alt + N + Q** → lisa Pie Chart  
- **Ctrl + ↑ / ↓** → hüppa tabeli algusesse/lõppu  
- **Ctrl + Shift + L** → lülita filtrid sisse/välja  
- **Alt + H + L** → Conditional Formatting menüü  
- **Ctrl + S** → salvesta  
- **Ctrl + F** → otsi (Find)  
- **Ctrl + H** → otsi ja asenda (Replace)  

---

## 🎨 Severity värvikoodid

| Severity  | Excel värv (Fill Color) | Hex kood | RGB |
|-----------|-------------------------|----------|-----------|
| **Critical** | Punane (Red)            | `#FF0000` | (255, 0, 0) |
| **High**     | Oranž (Orange)          | `#FFA500` | (255, 165, 0) |
| **Medium**   | Kollane (Yellow)        | `#FFD700` | (255, 215, 0) |
| **Low**      | Roheline (Green)        | `#32CD32` | (50, 205, 50) |

### GitHub Markdownis (reaalne värvikuva)

- <span style="color:#FF0000; font-weight:bold">Critical</span>  
- <span style="color:#FFA500; font-weight:bold">High</span>  
- <span style="color:#FFD700; font-weight:bold">Medium</span>  
- <span style="color:#32CD32; font-weight:bold">Low</span>  


### Excelis
- Conditional Formatting → vali **More Colors → Custom → Hex/RGB**.  
- Loo 4 eraldi reeglit.  
- Salvesta Custom Theme Colors, et hiljem igal failil kasutada.  

### Graafikutes
- Pivot Chart → **Format Data Series → Fill → Solid Fill → Custom color (Hex)**.  
- Salvesta graafikust mall (**Save as Template**).  

