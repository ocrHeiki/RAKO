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

Andmeside maailmas liiguvad andmed kihiti: iga kiht lisab oma info (päise), mis aitab andmetel liikuda korrektselt ühest arvutist teiseni.

Kasutusel on kaks peamist mudelit:
- **OSI mudel (7 kihti)** – teoreetiline raamistik  
- **TCP/IP mudel (4 kihti)** – praktiline interneti alus

---

## 2️⃣ OSI ja TCP/IP mudelite võrdlus

| OSI mudel (7 kihti) | TCP/IP mudel (4 kihti) | Näited protokollidest |
|--------------------|------------------------|-----------------------|
| 7. Rakendus | Rakendus | HTTP, DNS, SMTP |
| 6. Esitus | Rakendus | TLS, MIME |
| 5. Sessioon | Rakendus | TLS handshake |
| 4. Transport | Transport | TCP, UDP |
| 3. Võrk | Internet | IP, ICMP |
| 2. Andmeside | Link | Ethernet, ARP |
| 1. Füüsiline | Link | Kaablid |

---

## 3️⃣ OSI mudeli 7 kihti

### 7. Rakenduskiht
- Kasutajale nähtav kiht
- Võrguteenused ja rakendused

**Näited:** HTTP, HTTPS, FTP, SMTP, DNS  
**Tüüpiline viga:** teenus ei vasta

---

### 6. Esituskiht
- Vormindamine ja kodeerimine
- Krüpteerimine

**Näited:** TLS, UTF-8  
**Tüüpiline viga:** sertifikaadi probleem

---

### 5. Sessioonikiht
- Seansi loomine ja haldus

**Näited:** TLS handshake  
**Tüüpiline viga:** seanss katkeb

---

### 4. Transpordikiht
- Andmete edastamine

**TCP**
- Usaldusväärne
- Kinnitused ja taasedastus

**UDP**
- Kiire
- Ilma garantiita

---

### 3. Võrgukiht
- IP-aadressid
- Marsruutimine

**Näited:** IP, ICMP  
**Tüüpiline viga:** vale gateway

---

### 2. Andmesidekiht
- MAC-aadressid
- Kohalik edastus

**Näited:** Ethernet, ARP  
**Tüüpiline viga:** ARP ei leia seadet

---

### 1. Füüsiline kiht
- Kaablid ja signaalid

**Tüüpiline viga:** katkine kaabel

---

## 4️⃣ TCP/IP perekond

| Kiht | Ülesanne |
|-----|---------|
| Application | Teenused |
| Transport | Andmete edastus |
| Internet | IP |
| Link | Füüsiline edastus |

---

## 5️⃣ Kapseldamine ja andmevoog

**Saatmisel:**
1. Rakendus → andmed  
2. Transport → port  
3. Internet → IP  
4. Link → MAC  

**Vastuvõtmisel toimub dekapseldamine.**

---

## 6️⃣ Olulisemad protokollid

| Protokoll | Kiht | Ülesanne |
|---------|------|----------|
| HTTP | Application | Veeb |
| DNS | Application | Nime lahendus |
| TCP | Transport | Usaldus |
| UDP | Transport | Kiirus |
| IP | Network | Aadress |
| ARP | Data Link | IP → MAC |

---

## 7️⃣ Praktilised harjutused

### Ühenduse test
```bash
ping 8.8.8.8
```

### DNS test
```bash
nslookup google.com
```

### Marsruudi jälgimine
```bash
traceroute google.com
```

---

## 8️⃣ Võrguprobleemide lahendamine

1. Füüsiline ühendus  
2. MAC-tase  
3. IP-tase  
4. Port  
5. Teenus

---

## 9️⃣ NAT, DHCP ja DNS

- **DHCP:** jagab IP  
- **NAT:** peidab sisevõrgu  
- **DNS:** nimi → IP

---

## 🔟 HTTP, HTTPS ja TLS

- HTTP – krüpteerimata  
- HTTPS – krüpteeritud  
- TLS – turvalisus

---

## 1️⃣1️⃣ MTU ja fragmentatsioon

- MTU = maksimaalne paketi suurus  
- Liiga suur → fragmentatsioon

---

## 1️⃣2️⃣ Mini-labor: liikluse jälgimine

**Wireshark filtrid:**
```
http
dns
tcp.port == 443
```

---

## 1️⃣3️⃣ Portide meelespea

| Port | Teenus |
|-----|--------|
| 22 | SSH |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |

---

## 1️⃣4️⃣ Kordamisküsimused

1. Mis vahe on TCP-l ja UDP-l?
2. Millises kihis toimub krüpteerimine?
3. Mis roll on DNS-il?

---

## 1️⃣5️⃣ Vigade kiirkaart

| Probleem | Kiht |
|--------|-----|
| Kaablit pole | L1 |
| ARP ei tööta | L2 |
| IP unreachable | L3 |
| Port kinni | L4 |
| Server error | L7 |

---

## 1️⃣6️⃣ Sõnastik

- **OSI** – Open Systems Interconnection  
- **MTU** – Maximum Transmission Unit  
- **NAT** – Network Address Translation  
- **ARP** – Address Resolution Protocol  
- **TLS** – Transport Layer Security  

---

**Valmis kasutamiseks GitHubis, PDF-iks või õppematerjalina.**
