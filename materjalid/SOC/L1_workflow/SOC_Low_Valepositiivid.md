# SOC L1 – Low kategooria valepositiivid

SOC L1 analüütiku töö käigus tuleb tihti ette, et **Low severity** sündmusi on sadu või isegi tuhandeid päevas.  
Kõik need ei ole tegelikud ohud – paljud on **valepositiivid**, mis tulenevad normaalsest võrguliiklusest või liiga tundlikest signatuuridest.  

---

## Miks neid jälgida?
- Kui neid on liiga palju → tekib **alert fatigue** (analüütik väsib mürast).  
- Regulaarsete korduste tuvastamine aitab otsustada, kas:
  - jätta signatuur **peenhäälestamata** (jätkub jälgimine),  
  - teha **ignoreerimisreegel**,  
  - või suunata L2 analüütikule, kui korduvus viitab ikkagi võimalikule ohule.  

---

## ✅ Levinumad Low valepositiivid ja võimalikud põhjused

### 1. Port Scans
- **Threat Name**: TCP/UDP Scan, SYN Scan, FIN Scan  
- **Põhjus**: võrguskannerid või isegi tavalised võrguinventuuri tööriistad  
- **Märkused**: tihti korduvad väljastpoolt → võib jätta madala prioriteediga, kui Action = Blocked  

---

### 2. DNS päringud
- **Threat Name**: Suspicious DNS Query  
- **Põhjus**: seadmed või rakendused teevad palju DNS päringuid  
- **Märkused**: kui domeen on legitiimne, võib olla müra; kui kahtlane domeen kordub → kontrollida  

---

### 3. NetBIOS / SMB müra
- **Threat Name**: NetBIOS Query, SMB Request  
- **Põhjus**: Windows arvutite tavaline sisemine liiklus  
- **Märkused**: sisemistes võrkudes sage ja mitte alati ohtlik  

---

### 4. Vana brauser või protokoll
- **Threat Name**: Outdated User-Agent, SSLv2/v3 handshake  
- **Põhjus**: mõni vana seade kasutab aegunud protokolli  
- **Märkused**: logi küll Low, aga hea märkida, sest võib viia haavatavuseni  

---

### 5. ICMP (ping) liiklus
- **Threat Name**: ICMP Echo Request Flood (Low)  
- **Põhjus**: monitooring, pingimised, tavaline võrgu tervisekontroll  
- **Märkused**: vaata, kas korduv samast allikast → võib viidata skaneeringule  

---

## 🎯 SOC L1 tegevus Low sündmuste puhul
1. **Top korduvused** – tee tabel 3–5 enim kordunud Low sündmusega.  
2. **Vaata Action** – kui Blocked, siis dokumenteeri, mitte eskaleeri.  
3. **Vaata korduvust** – sama allikas või sihtmärk → raporteeri korduva mustrina.  
4. **Lisa kokkuvõttesse** – kirjuta, et need on võimalikud valepositiivid koos põhjustega.  

---

## 📌 Kokkuvõte
Low kategooria sündmused ei ole SOC L1 jaoks esmane prioriteet, kuid nende korduv analüüs aitab:
- vähendada mürataset,  
- tuvastada päriselt korduvat anomaaliat,  
- anda soovitusi L2/L3-le signatuuride häälestamiseks.  
