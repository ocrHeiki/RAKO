# Etapp 1 — Excel (logide esmase analüüsi juhend)

Selles etapis tehakse L1-taseme triage Excelis või Google Sheetsis.  
Eesmärk: kiiresti leida kõrge riskiga ühendused ja eristada valepositiivid.

## Kasutatavad väljad
- **Severity** (tekst: critical/high/medium/low)
- **Risk of app** (arv: 1–5)
- **Action** (allow/deny/drop)
- **Rule** (millise poliitika alt lubati/keelati)
- **Source address**, **Destination address**
- **Application**
- **Bytes**
- **User** (vajadusel)

## Värvikoodid (kasutada alati samu)
- 🔴 Critical → HEX `#FF0000`
- 🟧 High → HEX `#FFA500`
- 🟨 Medium → HEX `#FFFF00`
- 🔵 Low → HEX `#0000FF`

## Samm-sammult (Excel)
1. Ava `log.csv` Excelis.  
2. Lisa Filter kõigile veergudele.  
3. Lisa **Conditional Formatting** nii Severity kui Risk of app veergudele:

   - Severity:  
     - "critical" → 🔴 punane (`#FF0000`)  
     - "high" → 🟧 oranž (`#FFA500`)  
     - "medium" → 🟨 kollane (`#FFFF00`)  
     - "low" → 🔵 sinine (`#0000FF`)  

   - Risk of app:  
     - 5 → 🔴 punane (`#FF0000`)  
     - 4 → 🟧 oranž (`#FFA500`)  
     - 3 → 🟨 kollane (`#FFFF00`)  
     - 1–2 → 🔵 sinine (`#0000FF`)  

4. Sorteeri riskitaseme järgi (kõige kõrgemad ette).  
5. Tee eraldi töölehed:  
   - `proxy` (Application=http-proxy või Risk=5)  
   - `dns` (Application=dns-base)  
   - `ssl` (Application=ssl)  
   - `smb` (Application sisaldab ms-ds-smb)  

6. Kontrolli **Action** veergu:  
   - Kui `allow` → kas see oli ootuspärane?  
   - Kui `deny` või `drop` → vähem kriitiline, kuid jälgi korduvaid allikaid.  

7. Kontrolli **Rule** veergu:  
   - Kui lubati `allow any` või liiga laia reegliga → märgi eskaleerimiseks.  
   - Kui spetsiifilise reegliga → tõenäoliselt benign.  

8. Lisa veerg `triage_note` ja kirjuta kokkuvõte (nt `benign-cloud`, `suspicious-proxy`, `check-dns`).  
