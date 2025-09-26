# 📑 SOC L1 Workflow — Samm-sammuline juhend (täpse menüüdega)

## 1. CSV import Excelisse
1. Ava Excel.  
2. **Data → Get Data → From File → From Text/CSV** (Excel 365-s sama).  
3. Vali logifail (nt `paloalto-threat-2025-09-26.csv`).  
4. Import-aknas:
   - **File Origin** = UTF-8
   - **Delimiter** = Comma (,)
   - Vaata eelvaadet – veerud peavad jagunema õigesti (nt `SourceIP`, `DestinationIP`, `ThreatName`).  
5. Vajuta **Load**.

---

## 2. Vormindus (andmete ettevalmistamine)
- **Home → Editing → Sort & Filter → Filter** – lisa filtrid igale veerule.  
- **View → Freeze Panes → Freeze Top Row** – päis jääb nähtavaks.  
- (Soovi korral) **Ctrl + T** – tee andmed Excel Table-iks (lihtsam filtreerida ja viidata).  
- **File → Save As → Excel Workbook (.xlsx)** – salvesta tööfail.

---

## 3. Tingimuslik vormindamine (Severity värvid)
1. Vali veerg **Severity**.  
2. **Home → Styles → Conditional Formatting → Highlight Cell Rules → Text that Contains…**  
   loo neli reeglit:
   - Critical → **More Colors → Custom → Hex `#FF0000`** (punane)
   - High → **Hex `#FFA500`** (oranž)
   - Medium → **Hex `#FFD700`** (kollane)
   - Low → **Hex `#32CD32`** (roheline)
3. (Valikuline) **Action** veerule: Allowed = roheline, Block = hall/punane.

---

## 4. Kiirfiltreerimine
- Filtreeri esmalt **Severity = Critical OR High**.  
- **SourceIP** pealt: **Sort Z→A** või kasuta Pivotit, et näha kordusi.  
- **Text Filters → Contains / Does Not Contain** – false positive mustrite eemaldamiseks.  

---

## 5. Pivot Table raport
1. Märgi kogu tabel (**Ctrl + A**).  
2. **Insert → PivotTable**.  
3. Valikud:
   - **Rows** → *Threat Category* (või *MITRE_Tactic*)
   - **Columns** → *Severity*
   - **Values** → *Count of Alert_ID* (või *Count of Events*)  
4. Nüüd on sul koondvaade ohtudest kategooriate ja tasemete kaupa.

---

## 6. Graafikud
- Kliki Pivotisse → **Insert → Charts → Column (Clustered Column)** või **Pie (2‑D Pie)**.  
- **Chart Design → Add Chart Element → Data Labels** – lisa väärtused.  
- Määra seeriatele samad värvid, mis all olevas tabelis (vaata *Severity värvikoodid*).  
- **Save as Template** – et kasutada sama paletti ka edaspidi.

---

## 7. Analüüsi kokkuvõte
- Ava `analüüs/SOC_LogiFaili_Analüüsi_Template.md`.  
- Täida sektsioonid: üldarv, jaotus, kategooriad, kordused, allikad/sihtmärgid, MITRE, riskid, tegevused.  
- **NB!** Päeviku reaalandmeid **ära** pane avalikku GitHubi – see läheb ainult praktikakohale.

---

## ⚡ Kiirklahvid SOC Exceli töövoos
- **Ctrl + A** → vali kogu tabel  
- **Ctrl + T** → teisenda tabeliks (Excel Table)  
- **Alt + N, V** → lisa Pivot Table  
- **Alt + N, C** → lisa Column Chart  
- **Alt + N, Q** → lisa Pie Chart  
- **Ctrl + ↑ / ↓** → hüppa tabeli algusesse/lõppu  
- **Ctrl + Shift + L** → lülita filtrid sisse/välja  
- **Alt + H, L** → Conditional Formatting menüü  
- **Ctrl + S** → salvesta  
- **Ctrl + F / Ctrl + H** → otsi / asenda

---

## 🎨 Severity värvikoodid

| Severity  | Excel värv (Fill Color) | Hex kood | RGB |
|-----------|-------------------------|----------|-----------|
| **Critical** | Punane (Red)            | `#FF0000` | (255, 0, 0) |
| **High**     | Oranž (Orange)          | `#FFA500` | (255, 165, 0) |
| **Medium**   | Kollane (Yellow)        | `#FFD700` | (255, 215, 0) |
| **Low**      | Roheline (Green)        | `#32CD32` | (50, 205, 50) |

### Excelis
- Conditional Formatting reeglites → **More Colors → Custom → Hex/RGB**.  
- Soovi korral salvesta värvid **Custom Theme Colors** alla.

### Graafikutes
- Pivot Chart → **Format Data Series → Fill → Solid Fill → Custom color (Hex)**.  
- Salvesta graafikust mall (**Save as Template**).

### GitHub Markdownis (reaalne värvikuva)
- <span style="color:#FF0000; font-weight:bold">Critical</span>  
- <span style="color:#FFA500; font-weight:bold">High</span>  
- <span style="color:#FFD700; font-weight:bold">Medium</span>  
- <span style="color:#32CD32; font-weight:bold">Low</span>
