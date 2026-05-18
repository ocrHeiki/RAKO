# 🚀 EKSAMI TÖÖVOOG & SPIKKER — TEAM 10: HeRe

See töövoog on optimeeritud keskkonna **itskteam10** proaktiivseks auditeerimiseks (E-ITS), reaktiivseks forensikaks (MITRE ATT&CK) ja intsidentide tsentraalseks lahendamiseks otse analüütiku Kali masinast.
📅 0. ETTEVALMISTUSKORD (Tee laboris esimese asjana kloonimise ajal)

Kuna eelseadistus on kriitiline, sisesta oma Kali terminali need käsud kohe, kui sihtmärk-masinad vSphere'is kloonivad. See võtab aega alla minuti:
Bash

# 1. Uuenda pakettide nimekirja ja paigalda tööriistad + FreeRDP kaughalduseks
```
sudo apt update && sudo apt install -y mc nmap zenmap-kbx net-tools iproute2 freerdp2-x11
```
# 2. Käivita Kali masina enda SSH server (Vajalik VALVUR-i failide automaatseks vastuvõtmiseks)
```
sudo systemctl enable ssh
sudo systemctl start ssh
```
# 3. Vaata ja kirjuta üles oma Kali täpne labori-IP (Seda söödad keskkonnamuutujana ette)
```ip a | grep "inet "```

# 🏁 SAMM-SAMMULINE TÖÖVOOG LABORIS
**SAMM 1:** Virtuaaltaristu Kaitse (Kloonimine)

Tegevus: **Enne** kui teed ühegi masina terminali lahti, **tee** vSphere keskkonnas **kõigist** itskteam10 **masinatest Kloon**.

Miks? Forensiline kuldreegel. Kui tulemüür su kaughalduse välja lukustab või süsteem rikneb, saad sekundiga algseisu tagasi.

**SAMM 2:** Võrgu Baasjoone Kaardistamine (Zenmap)

Tegevus: Käivita Kali masinas **Zenmap** või terminalis **Nmap** ja pane võrk skaneerima:
Bash
```
sudo nmap -sV -O 192.168.10.0/24
```
Eesmärk: Fikseerida ründaja poolt avatud pordid enne meie sekkumist. Jäta võrguseire taustale jooksma, et hiljem filtreerida välja VALVUR-i enda tekitatud legitiimne liiklus ründaja omast.

**SAMM 3:** Kaughaldusühenduste Loomine

Kui Zenmap kinnitab, et kaughalduspordid on avatud, logi Kali masinast sihtmärkidesse sisse:

Linuxi serverisse (SSH): ```ssh kasutaja@192.168.10.X```

Windowsi serverisse (RDP üle FreeRDP):
Bash
```
xfreerdp /v:192.168.10.Y /u:Administrator /p:Parool123 /dynamic-resolution +clipboard
```
**SAMM 4:** VALVUR Masterskripti lennult käivitamine (In-Memory)

Selleks, et mitte saastada uuritavate masinate kõvakettaid, käivitame VALVUR-i otse vahemällu (RAM) GitHubi repositooriumist, andes kaasa oma Kali IP-aadressi:

🐧 Linuxi serveris (INTRAWEB1 / TicketingServer):
Bash
```
sudo KALI_IP=192.168.1.100 python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.py)"
```
💻 Windowsi serveris (DC1 / FileSRV1 läbi PowerShelli):
PowerShell
```
$env:KALI_IP="192.168.1.100"; iex (iwr -UseBasicParsing "https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.ps1")
```
Tulemus: VALVUR teostab E-ITS auditi ja terviklikkuse kontrolli, pakib tulemused kokku ning eksfiltreerib ZIP-paki automaatselt tagasi sinu Kali töölauale.

**SAMM 5:** Intsidentide Haldus (Ticketid)

Vaata oma Kali töölauale laekunud VALVUR-i raportit.
Registreeri kõik leitud E-ITS hälbed ja võrguandmed koheselt piletisüsteemis (TicketingServer-itskteam10). Priority: High/Critical.

**SAMM 6:** Linuxi Serveri Käsitöö ja Süvaanalüüs (INTRAWEB1)

Kui VALVUR andis vihje aktiivsest ründajast, jahti teda SSH sessioonis järgmiselt:

Aktiivsed olemid: ```w``` ja ```who -a ```-> Vaata veergu WHAT (Mida nad reaalajas teevad?).

Võrk reaalajas (Õpetaja soovitus): ```sudo netstat -nputw``` -> Tuvasta ESTABLISHED Reverse Shell (port 4444/1337) ja võta ründaja protsessi PID.

Pahavara asukoht kõvakettal: ```sudo ls -l /proc/[PID]/exe``` -> Näitab täpse kausta (nt /tmp/.hais/).

Püsivuspunktid: ```sudo crontab -e ja ls -la /etc/cron.d/``` -> Otsi @reboot või * * * * * tagauksi.

Logide ja veebijuure lappamine: ```sudo mc``` -> Pane vasakule paneelile veebilogid (/var/log/nginx/access.log) ja paremale rakenduse sisesed logid/failid (/var/www/html/), et tuvastada veebirakenduse õiguste alla peidetud Web Shellid ja ründejäljed.

Tulemüüri esmaabi (SSH elupäästja!):
Bash

# KRIITILINE: Luba alati SSH enne UFW aktiveerimist!
```
sudo ufw allow from [Sinu_Kali_IP] to any port 22 proto tcp
sudo ufw enable
sudo ufw status numbered
```
**SAMM 7:** Windowsi Masina Süvaanalüüs (DC1 / FileSRV1)

RDP sessiooni kaudu administraatori käsureal:

Võrguühendused: ```netstat -fano``` -> Otsi võõraid ühendusi ja võta PID. Tuvasta fail: tasklist /FI "PID eq [number]".

Aktiivsed lekked: ```compmgmt.msc``` -> Shared Folders -> Sessions (Kes tõmbab faile?).

Püsivus: **Käivita Autoruns64.exe** -> Hide Microsoft Entries -> Kontrolli Scheduled Tasks ja Registry Run võtmeid.

Logi-analüüs: Jooksuta VALVUR-i moodulit 11_turvafiltreering.py, et filtreerida välja kriitilised sündmused rünnaku kellaaja kohta.

# 📝 RAPORTEERIMISE JA MITRE ŠABLOON (Esitluse jaoks)

Iga leitud anomaalia vormista slaididele nii:

    Tuvastatud tegevus: (nt ründaja sessioon Linuxis crontab-is)

    Kasutatud tööriist: sudo crontab -e / netstat -nputw

    MITRE ATT&CK tehnika: T1053.003 (Scheduled Task/Job: Cron)

    E-ITS 2024 mittevastavus: SYS.1.3.M1 (Linuxi süsteemiturve)
