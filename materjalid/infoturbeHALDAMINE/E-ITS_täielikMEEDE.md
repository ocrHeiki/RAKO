# Eesti Infoturbestandardi (E-ITS) Täielik Etalonturbe Kataloog – GitHubi Versioon

**Autori märkus:**  
See dokument on koostatud GitHubi projekti tarbeks, sisaldab täielikku E-ITS meetmete kataloogi, praktilisi näiteid Ubuntu, Windows, Kali ja Parrot OS keskkondades ning ametlikke viiteid PDFidele ja RIA ressurssidele. Sobib SOC-õppe, auditite ja turbepraktikate õppimiseks.

---

## Sisukord

1. [EESSÕNA JA AMETLIKUD LINGID](#eessõna-ja-ametlikud-lingid)  
2. [ISMS – Info­turbe juhtimine](#isms--infoturbe-juhtimine)  
3. [SYS – Süsteemide turvameetmed](#sys--süsteemide-turvameetmed)  
4. [APP – Rakenduste turvameetmed](#app--rakenduste-turvameetmed)  
5. [OPS – Operatsioonide turvameetmed](#ops--operatsioonide-turvameetmed)  
6. [INF – Infohaldussüsteemid](#inf--infohaldussüsteemid)  
7. [DER – Krüptograafia ja andmete kaitse](#der--krüptograafia-ja-andmete-kaitse)  
8. [ORP – Organisatsioonilised meetmed](#orp--organisatsioonilised-meetmed)  
9. [KAS – Kasutajate haldus](#kas--kasutajate-haldus)  
10. [ADM – Administratiivsed protsessid](#adm--administratiivsed-protsessid)  
11. [TI – Teabe klassifitseerimine](#ti--teabe-klassifitseerimine)  
12. [Lingid ja viited](#lingid-ja-viited)

---

## EESSÕNA JA AMETLIKUD LINGID

E-ITS (Eesti Infoturbestandardi) eesmärk on tagada infosüsteemide ja teenuste terviklik kaitse, arvestades organisatsiooni riskide ja varade olulisust.  

### **Ametlikud lingid ja PDFid**

| Ressurss | Kirjeldus | Link |
|---------|-----------|------|
| **E-ITS Etalonturbe kataloog (Lisa 2)** | Täielik meetmekataloog, sisaldab kõiki meetmerühmi ja alammeetmeid | [PDF](https://www.riigiteataja.ee/aktilisa/1280/8202/5012/JDM_m12_lisa2.pdf) |
| **RIA – E-ITS standard (EE)** | Eesti infoturbestandardi ametlik tutvustus | [EE](https://www.ria.ee/kuberturvalisus/riigi-infoturbe-meetmete-haldus/eesti-infoturbestandardi-e-its) |
| **RIA – E-ITS standard (EN)** | Ingliskeelne ülevaade standardi eesmärgist ja rakendamisest | [EN](https://www.ria.ee/en/cyber-security/management-state-information-security-measures/information-security-standard-e-its) |
| **E-ITS tugirakendus** | Interaktiivne tööriist meetmete valimiseks ja rakendamiseks | [Tugirakendus](https://eits.ria.ee/) |

**Märkus:**  
Selles GitHubi Markdowni versioonis on igale meetmele lisatud praktiline näide, sealhulgas OS-spetsiifiline rakendus (Ubuntu, Windows Server, Kali, Parrot OS).

---

## ISMS – Info­turbe juhtimine

### **ISMS.1 – Infoturbe juhtimise struktuur**
- **Kirjeldus:** Organisatsioon määrab ja dokumenteerib infoturbe rollid, vastutuse ja aruandluse.  
- **Rakendusnäide:** SOC/IT halduri ametijuhend, turvapoliitika, riskide jaotamine.  

### **ISMS.2 – Infoturbe poliitika**
- **Kirjeldus:** Organisatsioonil on ametlik infoturbe poliitika, mis määrab eesmärgid, normid ja juhised.  
- **Rakendusnäide:** Dokument PDF-is, levitatakse töötajatele ja auditeeritakse kord aastas.

### **ISMS.3 – Info­turbe riskihaldus**
- **Kirjeldus:** Riskide identifitseerimine, analüüs, hinnang ja maandamisplaan.  
- **Rakendusnäide:** Riskiregister, ISO/IEC 27005 põhine riskianalüüs.

---

## SYS – Süsteemide turvameetmed

### **SYS.1.1 – Süsteemi arhitektuur ja dokumentatsioon**
- **Kirjeldus:** Kõik infosüsteemid peavad olema dokumenteeritud (arhitektuur, võrk, komponendid).  
- **Näide:** Ubuntu Serveri või Windows Serveri konfiguratsioonidokument.

### **SYS.1.2 – Süsteemi kõvendamine (Hardening)**
- **Kirjeldus:** Mittevajalikud teenused eemaldatud, turvaseaded seadistatud, failisüsteemi õigused rangelt.  
- **Praktilised näited:**
  - **Ubuntu:** SSH PasswordAuthentication no, ufw aktiveeritud  
  - **Windows:** Local Security Policy seadistused, Windows Defender kõvakettakaitse  
  - **Kali / Parrot OS:** Mittevajalikud paketid eemaldatud, tulemüür seadistatud, ründetööriistad eraldi kasutajaga

### **SYS.1.3 – Turvatarkvara ja skannimiste haldus**
- **Kirjeldus:** Antiviirus, EDR, IDS/IPS ja regulaarne haavatavuste skaneerimine.  
- **Näide:** OpenVAS või Nessus kontrollid, tulemused dokumenteeritud CSV-failina.

### **SYS.1.4 – Krüptograafia ja andmete kaitse**
- **Kirjeldus:** Andmete krüpteerimine puhke- ja transiidis olekus.  
- **Näide:** LUKS krüptimine Linuxis, BitLocker Windowsis.

### **SYS.1.5 – Juurdepääsu kontroll**
- **Kirjeldus:** Least privilege põhimõte, admin õigused logitud ja auditeeritud.  
- **Näide:** Samba ACL õiguste kontroll, Windows ACL, sudoers fail.

### **SYS.1.6 – Võrguühenduste kontroll**
- **Kirjeldus:** Firewall, tulemüür, turvamehhanismid liikluse kontrolliks.  
- **Näide:** ufw Ubuntu, Windows Firewall, pfSense.

### **SYS.1.7 – Auditilogid ja süsteemi järelevalve**
- **Kirjeldus:** Logid kogu juurdepääsu, konfiguratsiooni ja administraatori tegevuse kohta, tsentraliseeritud.  
- **Näide:** rsyslog + ELK stack Linuxis, Windows Event Forwarding.

### **SYS.1.8 – Teenuse järjepidevus**
- **Kirjeldus:** Varundus, DR-protseduurid, taastamine riistvara- või tarkvaratõrke korral.  
- **Näide:** Veeam Backup, Windows Server Backup, Cron + rsync.

### **SYS.1.9 – Konfiguratsiooni haldus**
- **Kirjeldus:** Muudatused dokumenteeritud, jälgitavad, vajadusel tagasipööratavad.  
- **Näide:** Ansible playbook, Git repos konfigureeritud serverite jaoks.

---

## APP – Rakenduste turvameetmed

### **APP.1.1 – Ohutu arendus (SDLC)**
- Kood läbi turvakontrollide (SAST, DAST)  
- Näide: SonarQube või GitLab CI turvascanning

### **APP.1.2 – Sisendi valideerimine**
- XSS, SQLi kontroll  
- Näide: Web aplikatsioonide sisendi sanitiseerimine

### **APP.1.3 – Autentimise ja sessiooni kontroll**
- Kahefaktoriline autentimine, sessiooni aegumine  
- Näide: OAuth2 + JWT + sessiooni timeout

---

## OPS – Operatsioonide turvameetmed

### **OPS.1.1 – Logihaldus**
- Logide säilitamine ja analüüs  
- Näide: ELK, Graylog, tsentraliseeritud logimine

### **OPS.1.2 – Varundamine**
- Varunduspoliitika dokumenteeritud  
- Näide: Rsync + offsite backup

### **OPS.1.3 – Paigaldus ja patch-haldus**
- Automaatne uuenduste haldus  
- Näide: apt unattended-upgrades, WSUS Windowsis

---

## INF – Infohaldussüsteemid

### **INF.1.1 – Füüsiline ja loogiline turve**
- Serveriruum, ligipääs, ACL, tulemüür  
- Näide: Ruumikasutuse kontroll + VLAN segregation

---

## DER – Krüptograafia ja andmete kaitse

### **DER.1.1 – Krüptograafilised võtmed**
- Turvaline hoidmine, rotatsioon  
- Näide: Vault / Key Management System

---

## ORP – Organisatsioonilised meetmed

### **ORP.1.1 – Turvakoolitus**
- Töötajate teadlikkus, testid, regulaarne uuendamine

### **ORP.1.2 – Intsidendi raportimine**
- Protseduurid intsidentide tuvastamiseks ja teatamiseks

---

## KAS – Kasutajate haldus

- Konto loomine, kustutamine, privileegide kontroll  
- Näide: Active Directory, LDAP, Linux usermod/chage

---

## ADM – Administratiivsed protsessid

- Riskihindamine, audit, poliitika kontroll  
- Näide: SOC protseduurid, logide audit

---

## TI – Teabe klassifitseerimine

- Andmete tundlikkuse määramine, krüptimine, juurdepääsuõigused  
- Näide: Confidential / Internal / Public andmete märgistamine

---

## Lingid ja viited

- **E-ITS Etalonturbe kataloog (Lisa 2)** – [PDF](https://www.riigiteataja.ee/aktilisa/1280/8202/5012/JDM_m12_lisa2.pdf)  
- **RIA – E-ITS standard (EE)** – [EE](https://www.ria.ee/kuberturvalisus/riigi-infoturbe-meetmete-haldus/eesti-infoturbestandardi-e-its)  
- **RIA – E-ITS standard (EN)** – [EN](https://www.ria.ee/en/cyber-security/management-state-information-security-measures/information-security-standard-e-its)  
- **E-ITS tugirakendus** – [Tugirakendus](https://eits.ria.ee/)  

**Autori märkus:** Kõik praktilised näited on kohandatud SOC ja õppematerjalide tarbeks ning sisaldavad OS-spetsiifilisi juhiseid (Ubuntu, Windows, Kali, Parrot OS).

---
