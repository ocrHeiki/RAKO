# SOC Analyst L1 Workflow (Palo Alto Threat Log)

---

## 1. Ava CSV Excelis
- File → Open → vali CSV
- Eraldajaks koma `,`
- Näed päises valitud välju

---

## 2. Kasuta ainult olulisi veerge
✅ Hoia alles:
- Generate Time
- Type
- Threat ID/Name
- From Zone / To Zone
- Source Address
- Source User (kui täidetud)
- Severity
- Destination Address
- To Port
- Application
- Action
- File Name / URL
- Device Name / Device SN
- Rule

❌ Ära kasuta: kõik, mis on CSV-s alati tühjad või nullidega

---

## 3. Tee püsiv Template vorming
1. Ava CSV → vali kõik veerud  
2. Mine **Insert → Table** → märgi „My table has headers“  
3. Lisa **Data → Filter** → saad igale veerule rippmenüü  
4. Lisa **Conditional Formatting** Severity värvidega:  
   - Critical = punane (#FF0000)  
   - High = oranž (#FF6600)  
   - Medium = kollane (#FFCC00)  
   - Low = sinine (#3399FF)  
5. Salvesta see töövihik nimega **ThreatLog_Template.xlsx**  
6. Edaspidi: ava uus CSV → kopeeri andmed → kleebi **ThreatLog_Template.xlsx** sisse → kõik filtrid ja värvid jäävad püsima  

---

## 4. Filtreeri enne graafikuid
1. **Severity** – alusta Critical ja High  
2. **Action** – kõigepealt Allowed, seejärel Blocked  
3. **Threat Name** – vaata korduvusi  
4. **Source / Destination** – IP või riikide järgi  
5. **Application / Port** – millist teenust rünnati  

---

## 5. Koosta graafikud
- **Severity jaotus** → Pie Chart (kui palju Critical/High/Medium/Low)  
- **Top Threat Name** → Column Chart (Top 5 ohtu)  
- **Source Address korduvused** → Bar Chart (Top allikad)  
- **Destination Address korduvused** → Bar Chart (Top sihtmärgid)  
- **Aja trend** (Generate Time) → Line Chart (sündmuste arv ajas)

👉 Kuna töötad **ThreatLog_Template.xlsx** failis, rakenduvad filtrid ja värvid automaatselt graafikutele iga kord, kui andmed uuesti sisse kleebid.

---

## 6. Tee esmane analüüs
- Critical + Allowed → **kohene eskaleerimine**  
- High + Blocked → dokumenteeri ja jälgi korduvust  
- Medium/Low → kas korduv muster või üksik intsident  
- Kontrolli **Rule** → kas reegel käitus ootuspäraselt  

---

## 7. Tee kokkuvõte
1. Mitu sündmust kokku?  
2. Severity jaotus (Critical/High/Medium/Low)  
3. Top Threat Names  
4. Top Source Address  
5. Top Destination Address  
6. Kas oli Allowed + High/Critical?  
7. Kas reeglid toimisid?  

---

## 🎨 Severity värvi legend
| Severity  | Näidisvärv |
|-----------|------------|
| <span style="color:#ff0000">Critical</span> | Punane (#FF0000) |
| <span style="color:#ff6600">High</span> | Oranž (#FF6600) |
| <span style="color:#ffcc00">Medium</span> | Kollane (#FFCC00) |
| <span style="color:#3399ff">Low</span> | Sinine (#3399FF) |

---

📌 **Oluline nipp**:  
Kui teed uue päeva analüüsi, **ära ava CSV otse graafikuks**, vaid kopeeri andmed oma **ThreatLog_Template.xlsx** sisse → see säästab aega, sest filtrid, värvid ja graafikute paigutus on alati valmis.
