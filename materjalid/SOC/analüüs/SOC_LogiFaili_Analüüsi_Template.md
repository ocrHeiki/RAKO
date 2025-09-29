# SOC Logifaili Analüüsi Näidis (Palo Alto Threat)

See on näidis, kuidas analüüsi kokkuvõte võiks välja näha.

---

## 📊 Päeva statistika
- Kokku sündmusi: 120
- Severity jaotus:
  - Critical: 3
  - High: 12
  - Medium: 45
  - Low: 60

---

## 🔎 Olulisemad leiud

### 1. Critical sündmused
- 2025-09-28 13:45 – Threat: **ETERNALBLUE exploit attempt**  
  Severity: Critical | Action: Allowed  
  Source: 192.168.10.50 | Destination: 10.0.0.20:445  
  Application: SMB | Rule: Allow Internal SMB  

➡️ **ESCALAATSIOn L2-le** (Critical + Allowed)

---

### 2. High sündmused
- 2025-09-28 14:10 – Threat: **Brute Force SSH**  
  Severity: High | Action: Blocked  
  Source: 203.0.113.10 | Destination: 192.168.10.15:22  
  Application: SSH | Rule: Block SSH Attacks  

➡️ Blokeeritud. Märgi ära korduvuste puhul.

---

### 3. Medium sündmused
- Kokku: 45  
- Levinumad ohud:
  - Threat: **SQL Injection attempt** – 5 korda erinevatelt IP-delt  
  - Threat: **Suspicious HTTP Request** – 8 korda  

➡️ Märkus: korduvad, aga kõik Action = Blocked.

---

### 4. Low sündmused ja sagedased valepositiivid
- Kokku: 60  
- Kõige sagedasemad:
  - Threat: **TCP Port Scan** – 15 korda → võimalik valepositiiv (välised skannerid)  
  - Threat: **Suspicious DNS Query** – 10 korda → võimalik valepositiiv (normaalne DNS päring)  
  - Threat: **NetBIOS Query** – 8 korda → võimalik valepositiiv (Windows võrgu sisene liiklus)  
- Võimalikud põhjused:
  - Võrguskannerid või monitooringutööriistad  
  - Liigne tundlikkus DNS päringute suhtes  
  - Windowsi standardne protokolliliiklus

➡️ Märkus: dokumenteeritud kui võimalikud valepositiivid, mitte eskaleeritud.

---

## ✅ Kokkuvõte
- Kõige kriitilisem oli **ETERNALBLUE exploit**, mis lubati läbi → kohe eskaleeritud.  
- Kõrgeid sündmusi oli 12, neist enamus blokeeriti reeglitega.  
- Medium sündmusi oli 45 – korduvad SQL Injection ja HTTP anomaaliad, kõik blokeeritud.  
- Low sündmusi oli 60 – enamus valepositiivid (Port Scan, DNS, NetBIOS).  
- Soovitus: üle vaadata SMB lubamisreeglid sisemises võrgus + võimalik DNS signatuuride peenhäälestus.  

---

## 🎨 Severity värvi legend
| Severity  | Näidisvärv |
|-----------|------------|
| <span style="color:#ff0000">Critical</span> | Punane (#FF0000) |
| <span style="color:#ff6600">High</span> | Oranž (#FF6600) |
| <span style="color:#ffcc00">Medium</span> | Kollane (#FFCC00) |
| <span style="color:#3399ff">Low</span> | Sinine (#3399FF) |
