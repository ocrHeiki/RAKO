# Võrguturbe ja Tulemüüri Labori Kokkuvõte

Käesolev dokument koondab **LAB A** raames teostatud sammud: virtuaalmasina eelhäälestuse, operatsioonisüsteemi paigalduse, SSH-ühenduse loomise, korduvad `nmap` pordiskaneeringud ning `ufw` tulemüüri reeglite rakendamise koos tulemuste võrgutaseme analüüsiga.

---

## 1. Virtuaalmasina (VM) Tehnilised Parameetrid & Paigaldus

Enne operatsioonisüsteemi installimist loodi VirtualBoxis sihtmärk-masin järgmiste spetsifikatsioonidega, mis tagavad Ubuntu Serveri stabiilse töö minimaalse ressursikuluga.

### Riistvara ja ressursside jaotus (VirtualBox)
* **Tüüp / Versioon:** Linux / Ubuntu (64-bit)
* **Operatiivmälu (RAM):** `2048 MB` (2 GB) – piisav serveri käsurea ja baasteenuste (Apache, SSH) jooksutamiseks.
* **Protsessor (CPU):** `1 vCPU` (või 2 vCPU sõltuvalt põhiarvuti võimekusest).
* **Kõvaketas (Virtual HDD):** `20 GB` (Tüüp: VDI, seadistatud kui *Dynamically allocated* ehk dünaamiliselt paisuv, et säästa põhiarvuti mälumahtu).

### Kasutatud tarkvara (ISO fail)
* **ISO tõmmis:** `ubuntu-24.04-live-server-amd64.iso` (ametlik Ubuntu Serveri LTS versioon, mis ei sisalda rasket graafilist töölauda).

### Võrgukaardi seadistus (Võtmeetapp!)
* **Režiim (Attached to):** `Bridged Adapter` (Sildatud režiim).
* **Võrgukaardi nimi (Name):** Arvuti füüsiline Wi-Fi/juhtmevaba kaart (nt *Intel Wireless* / `wlan0`), kuna laborit viidi läbi jagatud iPhone'i kuumkoha (*Personal Hotspot*) võrgus.
* **Miks mitte NAT?** NAT režiim peidab virtuaalmasina VirtualBoxi sisevõrgu ja tulemüüri taha, mistõttu ründemasin (Kali Linux) ei saaks sihtmärki võrgus skaneerida ega tuvastada.

### Ubuntu Serveri paigaldamise spikker
Paigaldusprogrammi (Installer) kohustuslikud sammud ja parameetrid:
1.  **Your name:** `Labor` (või õpilase nimi)
2.  **Your server's name (Hostname):** `ubuntu-target`
3.  **Pick a username:** `opilane`
4.  **Choose a password:** Kasutaja määratud turvaline parool (nt `Kuber123!`).
5.  **SSH Setup:** Liiguti tühikuklahviga valiku peale ja märgiti **`[X] Install OpenSSH server`**. *Kriitiline samm pordi 22 avamiseks!*
6.  **Featured Server Snaps:** Lisatarkvara (Docker jne) ei valitud, liiguti otse nupule `Done`.
7.  Pärast installi lõppu teostati taaskäivitus (`Reboot Now`) ja vajutati konsoolis `Enter`, et eemaldada virtuaalne ISO-plaat.

---

## 2. SSH Ühenduse Loomine ja IP Tuvastus

Pärast süsteemi taaskäivitust tuvastati masina IP-aadress ja viidi haldus üle Kali Linuxi terminali, et võimaldada mugavat käskude kopeerimist ja reaalajas logide jälgimist.

### IP-aadressi tuvastamine sihtmärgis
Ubuntu serveri konsoolis käivitati käsk:
```bash
ip a
```
Vastus konsoolis:
Punkti 2: enp0s3 (või sarnase võrguliidese) alt tuvastati real inet iPhone'i võrgu poolt jagatud reaalne IP-aadress: 172.20.10.2.
SSH-ühenduse algatamine Kali Linuxist

Kali Linuxi terminalist (heiki@secLAB) käivitati ühendus:
```Bash
ssh opilane@172.20.10.2
```
Esmakordne ühendus: Süsteem küsis kinnitust võtme usaldamiseks (`"Are you sure you want to continue connecting (yes/no)?"`). Sisestati `yes`.

Autentimine: Sisestati kasutaja opilane parool (visuaalselt ekraanile tähti ega tärne turvakaalutlustel ei kuvatud).

Tulemus: Kali terminali rida muutus kujule `opilane@ubuntu-target:~$`, mis kinnitas edukat SSH šifreeritud tunneli loomist.

3. Rünnaku ja Kaitse Simulatsioon **(nmap vs ufw)**

Labori põhiosas testiti pordiskaneeringute käitumist ja tulemüüri olekute mõju võrguliiklusele.
ETAPP I: Apache2 paigaldamine ja avatud port (Olek: `open`)

SSH-aknas paigaldati sihtmärgile ametlik veebiserver:
```Bash

sudo apt update && sudo apt install apache2 -y
```
Ründaja käivitas Kalist pordi 80 kontrolli:
```Bash

sudo nmap -p 80 172.20.10.2
```
Vastus Kali terminalis:
```Plaintext

PORT     STATE SERVICE
80/tcp   open  http
MAC Address: 08:00:27:0A:D5:A7 (Oracle VirtualBox virtual NIC)
```
Analüüs: Port on olekus open. Nmap tuvastas lisaks virtuaalkaardi MAC-aadressi, mis tõestab, et masinad on samas alamvõrgus. 
Wiresharkis oli näha korrektne kolmepoolne kätlemine (SYN -> SYN, ACK -> ACK).

ETAPP II: Tulemüüri väärseadistuse õppetund (Olek: inactive)

SSH-aknas üritati porti 80 tulemüüriga sulgeda:
```Bash

sudo ufw deny 80/tcp
```
Süsteem teatas: `Rules updated`. Kuid uuel skaneerimisel Kalist jäi port ikkagi olekusse open.

Põhjuse tuvastamine sihtmärgis:
```Bash

sudo ufw status numbered
```
Vastus konsoolis:
```Plaintext

Status: inactive
```
Õppetund eksamiks: Tulemüüri reeglid võivad olla süsteemi sisestatud, kuid kui tulemüür ise on tarkvaraliselt välja lülitatud (inactive), ei rakendata ühtegi piirangut ja võrk on ründajale täielikult avatud!

ETAPP III: Tulemüüri aktiveerimine ja blokeering (Olek: filtered)

Tulemüür lülitati reaalajas sisse ja reeglitele tehti taaskäivitus:
```Bash

sudo ufw enable
```
# Kinnituseks vajutati `y` (lubades SSH ühendusel jääda aktiivseks)
`sudo ufw status numbered`

Vastus konsoolis:
```Plaintext

Status: active

     To                   Action      From
     --                   ------      ----
[ 1] 80/tcp               DENY IN     Anywhere
[ 2] 80/tcp (v6)          DENY IN     Anywhere (v6)
```
Et kindlustada SSH-ühenduse säilimine pärast virtuaalmasina tulevast taaskäivitamist, lisati kohe ka kindel lubav reegel pordile 22:
```Bash

sudo ufw allow 22/tcp
```
Uus skaneerimine Kali Linuxist:
```Bash

sudo nmap -p 80 172.20.10.2
```
Vastus Kali terminalis:
```Plaintext

PORT     STATE    SERVICE
80/tcp   filtered http
MAC Address: 08:00:27:0A:D5:A7 (Oracle VirtualBox virtual NIC)
```
Analüüs: Pordi olekuks muutus **filtered** (filtreeritud). Skaneerimine võttis kauem aega, sest UFW viskas paketid vaikides prügikasti ja ründaja pidi ootama vastust kuni aegumistähtajani (timeout). Wiresharkis kuvati ründaja poolel korduvaid päringuid teatega [TCP Retransmission].

4. Võrgutopoloogia Kaardistamine

Labori loogilise ahela ja teekonna kontrollimiseks kasutati nmap-i pakettide jälgimise režiimi:
```Bash

sudo nmap -p 22,80 --traceroute 172.20.10.2
```
Vastus Kali terminalis:
```Plaintext

PORT     STATE    SERVICE
22/tcp   open     ssh
80/tcp   filtered http

TRACEROUTE
HOP RTT     ADDRESS
1   0.44 ms 172.20.10.2
```
Topoloogia järeldus eksamiks

Kuna TRACEROUTE tuvastas sihtmärgi täpselt 1 hüppe (HOP 1) kaugusel, tõestab see loogiliselt, et tänu Bridged Adapter seadistusele asuvad Kali ja Ubuntu samas võrgukihis ning vahetavad pakette otse, läbimata vahepealseid filtreerivaid ruutereid. Võrk sarnaneb loogiliselt tähttopoloogiale, kus võrgu keskseks lülitiks/lüüsiks on iPhone kuumkoht (172.20.10.1).

Aruande versioon: 1.1

Labori kuupäev: 2026-06-11

Keskkond: Kali Linux (heiki㉿secLAB) & Ubuntu Server 24.04 LTS (opilane@ubuntu-target)
