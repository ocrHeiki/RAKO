# Wazuh SIEM ja Nmap Küberkaitse Auditeerimise Spikker (LAB05)

Käesolev fail sisaldab täielikku ülevaadet olulistest Nmap skaneerimise käskudest, nende tehnilistest kirjeldustest, kriitilistest portidest, mida igal turvaeksamil või auditil peab teadma, ning valmis võrgutopoloogia ja IP-aadresside plaani tabeleid auditiraportisse lisamiseks.

---

## 1. Nmap Võrguskaneerimise ja Haavatavuste Otsimise Käsud

| Käsk | Tüüp / Eesmärk | Tehniline Kirjeldus / Millal Kasutada? |
| :--- | :--- | :--- |
| `sudo nmap -sn 10.0.x.0/24` | **Ping Scan** (Host Discovery) | Kontrollib kiiresti, millised masinad on võrgus sisse lülitatud. Porte ei skaneerita. Kasuta esimese sammuna võrgu kaardistamisel. |
| `sudo nmap -sS <IP_või_Võrk>` | **SYN Stealth Scan** | Poolavatud (half-open) skaneering. Ei vii TCP ühendust lõpuni, mistõttu on kiirem ja jääb traditsioonilistesse logidesse vähem silma. Nõuab `sudo` õigusi. |
| `sudo nmap -sT <IP_või_Võrk>` | **TCP Connect Scan** | Viib TCP kolmepoolse kätlemise (3-way handshake) täielikult lõpule. Kasutatakse siis, kui ründajal puuduvad administraatori (`sudo`) õigused. Jääb sihtmärgi logidesse väga selgelt maha. |
| `sudo nmap -sV <IP_või_Võrk>` | **Version Detection** | Tuvastab avatud portidel jooksvate rakenduste täpsed versioonid (nt *OpenSSH 8.9p1*). Ülioluline haavatavuste (CVE) otsimisel. |
| `sudo nmap -O <IP_või_Võrk>` | **OS Detection** | Püüab tuvastada sihtmärgi operatsisoonisüsteemi (nt *Linux 5.x*, *Windows 10*) TCP/IP stäki sõrmejälgede põhjal. |
| `sudo nmap -A <IP>` | **Agressiivne skaneering** | Paneb kokku OS-i tuvastuse (`-O`), versioonituvastuse (`-sV`), skriptide skaneerimise (`-sC`) ja teekonna tuvastuse (*Traceroute*). Väga mürarikas võrgus, kuid annab ühe masina kohta maksimuminfo. |
| `sudo nmap -p- <IP>` | **Kõikide portide kontroll** | Skaneerib läbi kõik võimalikud **65 535 porti** (vaikimisi kontrollib Nmap vaid 1000 levinumat). Kasuta peidetud tagaustega (*backdoor*) pahalaste masinate otsimiseks. |
| `sudo nmap -p 22,80,443 <IP>` | **Konkreetsete portide kontroll** | Säästab aega, kontrollides ainult spetsiifiliselt määratud teenuseid. |
| `sudo nmap --script vuln <IP>` | **Haavatavuste kontroll (NSE)** | Kasutab Nmap Scripting Engine (NSE) andmebaasi, et kontrollida, kas sihtmärgi avatud teenustel on teadaolevaid kriitilisi turvaauke või exploite. |
| `sudo nmap --script brute <IP>` | **Automaatne paroolirünnak** | Püüab levinud teenustele (nt SSH, FTP) teha automaatset sõnastikurünnakut vaikekasutajate ja paroolidega. |

---

## 2. Eksamil Kriitilised Pordid ja Teenused (Mida auditist otsida?)

Kui teostad võrguauditit või otsid pahalase masinat, viitavad järgmised avatud pordid konkreetsetele teenustele või ohtudele:

### Standardse Infrastruktuuri Pordid
* **Port 21 (FTP):** Failiedastusprotokoll. Sageli krüpteerimata ja vana tarkvara korral kergesti haavatav.
* **Port 22 (SSH):** Turvaline terminaliliides (Secure Shell). Alati kontrollida, kas lubatud on root-kasutaja sisselogimine või paroolirünnakud.
* **Port 53 (DNS):** Domeeninimede süsteem. Haavatav tsooniedastuse (*Zone Transfer*) päringutele, kui on valesti seadistatud.
* **Port 80 (HTTP) & Port 443 (HTTPS):** Veebiserverid. Kontrollida rakenduste turvalisust ja aegunud SSL/TLS sertifikaate.

### Windows / Active Directory (AD) Spetsiifilised Pordid
* **Port 88 (Kerberos):** Kasutatakse Active Directory autentimiseks.
* **Port 135 (RPC) & Pordid 139, 445 (SMB):** Windowsi failijagamine. **Port 445** on ajalooliselt olnud sihtmärgiks rünnakutele nagu *EternalBlue* (WannaCry pahavara). Pahalase masinad jätavad selle tihti avatuks.
* **Port 389 (LDAP) & Port 636 (LDAPS):** Active Directory kataloogiteenuse päringud.
* **Port 3389 (RDP):** Kaugtöölaud (Remote Desktop). Ründajate levinud sihtmärk toore jõu (*brute-force*) rünnakuteks.

### Infrastruktuuri ja SIEM Halduspordid
* **Port 1514 (Wazuh Agent liides):** Port, mille kaudu Wazuh Agendid saadavad krüpteeritud turvalogisid Wazuh Managerile.
* **Port 1515 (Wazuh Agent registreerimine):** Kasutatakse uute agentide automaatseks liitmiseks ja võtmete jagamiseks.
* **Port 55000 (Wazuh API):** Wazuh Manageri sisemine API liides haldustegevusteks.
* **Port 9200 (Wazuh Indexer / Elasticsearch):** Andmebaasi liides. Peab alati olema välismaailma eest suletud!

### Pahalase / Kahtlased pordid (Ründeindikaatorid)
* **Port 4444 (Metasploit Default Meterpreter):** Kui leiad võrgust masina, millel on lahti port 4444, on see peaaegu kindel märk sellest, et masin on häkitud ja seal jookseb aktiivne ründaja tagauks (*reverse shell*).
* **Port 5555, 9999, 6667 (IRC/Backdoors):** Kasutatakse sageli botneti juhtimiseks (*Command & Control*) või vanemate troojalaste poolt.

---

## 3. Auditiraporti Näidistabelid (Kopeerimiseks)

Kasuta neid lihtsaid tabeleid oma auditidokumentatsioonis võrgu hetkeseisu ja topoloogia fikseerimiseks.

### 3.1 Võrgu plaan

| Võrk | Gateway | Võrgumask | Levi aadress (Broadcast) | DHCP vahemik |
| :--- | :--- | :--- | :--- | :--- |
| 10.0.x.0/24 | 10.0.x.1 | 255.255.255.0 | 10.0.x.255 | 10.0.x.100 - 10.0.x.200 |

### 3.2 IP aadresside plaan

| Virtuaalmasina nimi | Masina hostinimi | Masina IP | Teenused / Funktsioon võrgus |
| :--- | :--- | :--- | :--- |
| WinServr | AD1 | 10.0.x.2 | SSH, Active Directory, DHCP, DNS |
| WinCoreServer | AD2 | 10.0.x.3 | SSH, Failiserver, AD varukoopia |
| WinKlient | WinKlient | 10.0.x.4 | SSH, Kasutaja tööjaam |
| DebianServer | Debian | 10.0.x.50 | SSH, Apache Veebiserver, MariaDB Andmebaas |
| AlmaServer | Alma | 10.0.x.51 | SSH, Logiserveer (Syslog) |
| UbuntuServer | Ubuntu | 10.0.x.52 | SSH, Ansible Automaatika, Wazuh Agent |

---
*Nõuanne eksamiks: Täida tabelis olevad `x` väärtused vastavalt sellele, millise võrguvahemiku kooli või eksamikeskkonna ruuter sulle automaatselt määrab (näiteks sinu praeguses koduses testis oli selleks `192.168.1`).*
