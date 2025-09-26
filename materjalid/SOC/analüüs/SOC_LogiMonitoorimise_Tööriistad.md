# 🛠️ SOC Logi Monitoorimise Tööriistad (ilma tarkvara paigaldamata)

Praktika keskkonnas ei pruugi sul olla õigust uusi rakendusi paigaldada.  
Seetõttu pead kasutama ainult neid tööriistu, mis on **süsteemi või brauseriga juba kaasas**.

## 1. Excel
- **Data → Get Data → From Text/CSV** – import.  
- Filtrid + Conditional Formatting (severity värvid).  
- Pivot + Chart – koondvaade ja visuaalid.

## 2. PowerShell (Windows)
```powershell
Get-Content C:\logs\threat.csv -Wait            # reaalajas jälgimine
Select-String -Path C:\logs\threat.csv -Pattern "Critical"   # filtreeri
Import-Csv C:\logs\threat.csv | Select-Object -First 5        # esimesed 5
```
## 3. Bash / Linux Shell
```bash
tail -f paloalto-threat.log
grep "Critical" paloalto-threat.log
awk -F, '{print $3}' paloalto-threat.csv | sort | uniq -c | sort -nr
```
## 4. Brauseri konsoolid (ei vaja installi)
Palo Alto WebUI, Splunk Web, Wazuh Dashboard, Kibana (ELK) – kasuta Time Range + Severity filtreid.
## 5. Notepad / Notepad++
Ctrl+F, väikeste logide kiireks vaatamiseks.
