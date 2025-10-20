# OSI ja TCP/IP protokollide õpe – samm-sammuline juhend

**Autor:** ocrHeiki  
**Teema:** OSI mudel ja TCP/IP protokollid  
**Eesmärk:** mõista võrgu tööpõhimõtteid kihiliselt, õppida tuvastama ja lahendama võrguvigade põhjuseid, lugema pakette ning tundma protokollide toimimist.  

---

## 📘 SISUKORD
1. Sissejuhatus  
2. OSI ja TCP/IP mudelite võrdlus  
3. OSI mudeli 7 kihti  
4. TCP/IP perekond  
5. Kapseldamine ja andmevoog  
6. Olulisemad protokollid  
7. Praktilised harjutused  
8. Võrguprobleemide lahendamine  
9. NAT, DHCP ja DNS  
10. HTTP, HTTPS ja TLS  
11. MTU ja fragmentatsioon  
12. Mini-labor: voo jälgimine  
13. Portide meelespea  
14. Kordamisküsimused  
15. Vigade kiirkaart  
16. Sõnastik

---

## 1️⃣ Sissejuhatus

Andmeside maailmas liiguvad andmed kihiti: iga kiht lisab oma info (päise), mis aitab andmetel liikuda korrektselt ühest arvutist teiseni. Seda kirjeldavad kaks mudelit:  
- **OSI mudel (7 kihti)** – teoreetiline raamistik  
- **TCP/IP mudel (4 kihti)** – praktiline interneti alus

---

## 2️⃣ OSI ja TCP/IP mudelite võrdlus

| OSI mudel (7 kihti) | TCP/IP mudel (4 kihti) | Näited protokollidest |
|----------------------|------------------------|-----------------------|
| 7. Rakendus (Application) | Rakendus (Application) | HTTP, DNS, SMTP |
| 6. Esitus (Presentation) | Rakendus (Application) | TLS, MIME, JSON |
| 5. Sessioon (Session) | Rakendus (Application) | TLS handshake |
| 4. Transport (Transport) | Transport (Transport) | TCP, UDP |
| 3. Võrk (Network) | Internet (Internet) | IP, ICMP |
| 2. Andmeside (Data Link) | Link (Link) | Ethernet, Wi-Fi, ARP |
| 1. Füüsiline (Physical) | Link (Link) | Kaablid, signaalid |

---

## 3️⃣ OSI mudeli 7 kihti
(…truncated for brevity…)
