
```
###############################################################################
#                                                                             #
#   █████   █████           ████                                              #
#  ▒▒███   ▒▒███           ▒▒███                                              #
#   ▒███    ▒███   ██████   ▒███  █████ █████ █████ ████ ████████             #
#   ▒███    ▒███  ▒▒▒▒▒███  ▒███ ▒▒███ ▒▒███ ▒▒███ ▒███ ▒▒███▒▒███            #
#   ▒▒███   ███    ███████  ▒███  ▒███  ▒███  ▒███ ▒███  ▒███ ▒▒▒             #
#    ▒▒▒█████▒    ███▒▒███  ▒███  ▒▒███ ███   ▒███ ▒███  ▒███                 #
#      ▒▒███     ▒▒████████ █████  ▒▒█████    ▒▒████████ █████                #
#       ▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒      ▒▒▒▒▒▒▒▒ ▒▒▒▒▒                 #
#                                                                             #
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  examWORKFLOW.md                                      |   #
#   |   LOODUD:      2026-05-18 (Uuendatud reaktiivse tõrjega)            |   #
#   |   AUTOR:       Heiki Rebane (Team 9 - HeRe)                         |   #
#   |   KIRJELDUS:   Eksami samm-sammuline töövoog. E-ITS audit,          |   #
#   |                reaktiivne forensika, intsidentide haldus ja         |   #
#   |                aktiivne ründe tõrje/pahalaste eemaldamine.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

```
# 🚀 EKSAMI TÖÖVOOG & SPIKKER — TEAM 9: HeRe
See töövoog on optimeeritud keskkonna **itskteam9** proaktiivseks auditeerimiseks (E-ITS 2024), reaktiivseks forensikaks (MITRE ATT&CK) ja intsidentide tsentraalseks lahendamiseks/tõrjeks otse analüütiku Kali masinast.
## 📅 0. ETTEVALMISTUSKORD (Tee laboris esimese asjana)
Kui sihtmärk-masinad vSphere'is kloonivad, sisesta need käsud Kali terminali. See võtab aega alla minuti – aga kui SSH server ei jookse, ei saa VALVUR tulemusi tagasi saata.
```bash
# 1. Uuenda paketid ja paigalda tööriistad
sudo apt update && sudo apt install -y mc nmap zenmap-kbx net-tools iproute2 freerdp2-x11

# 2. Käivita SSH server (vajalik VALVUR-i failide vastuvõtmiseks)
sudo systemctl enable ssh && sudo systemctl start ssh

# 3. Kontrolli, et SSH kuulab
ss -tlnp | grep 22

```
## 🏁 SAMM-SAMMULINE TÖÖVOOG LABORIS
### SAMM 1: Virtuaaltaristu kaitse (kloonimine)
**Tegevus:** Enne kui teed ühegi masina terminali lahti, **tee vSphere keskkonnas kõigist itskteam9 masinatest kloon**.
**Miks?** Forensiline kuldreegel (ISO 27037). Kui tulemüür su kaughalduse välja lukustab või süsteem rikneb, saad sekundiga algseisu tagasi.
### SAMM 2: Võrgu baasjoone kaardistamine (nmap)
**Tegevus:** Käivita Kali masinas võrgu skaneerimine:
```bash
# Kiire elusate tuvastus
sudo nmap -sn 192.168.10.0/24 -oG - | grep Up

# Põhjalik port + OS tuvastus (jäta taustale)
sudo nmap -sV -O 192.168.10.0/24 &

```
**Eesmärk:** Fikseerida ründaja poolt avatud pordid enne meie sekkumist. Jäta skaneerimine taustale jooksma – hiljem saad võrrelda VALVUR-i enda tekitatud liiklust ründaja omast.
### SAMM 3: Kaughaldusühenduste loomine
| Masin | Protokoll | Käsk |
|---|---|---|
| **Linux (ruuter, server, Kali)** | SSH | ssh kasutaja@192.168.10.X |
| **Windows (DC, file server)** | RDP | xfreerdp /v:192.168.10.Y /u:Administrator /p:Parool123 /dynamic-resolution +clipboard |
```bash
# SSH Linuxi
ssh heiki@192.168.10.10

# RDP Windowsi
xfreerdp /v:192.168.10.20 /u:Administrator /p:Parool123 /dynamic-resolution +clipboard

```
### SAMM 4: VALVUR-i käivitamine (ühe rea githubi käsklus)
Selleks, et mitte saastada uuritavate masinate kõvakettaid püsivate jälgedega, käivitatakse VALVUR otse mälust GitHubi repositooriumist. Kali IP tuvastatakse automaatselt $SSH_CLIENT põhjal.
#### 🐧 Linuxi sihtmärk (INTRAWEB1 / ruuter / TicketingServer)
```bash
# Lihtsalt kleebi – KALI_IP tuleb $SSH_CLIENT seest
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.py)"

```
#### 💻 Windowsi sihtmärk (DC1 / FileSRV1) – PowerShelli kaudu
```powershell
$env:KALI_IP="192.168.10.50"; iex (iwr -UseBasicParsing "https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.ps1")

```
### SAMM 5: Intsidentide haldus (ticketid)
 1. Vaata Kali töölauale laekunud VALVUR-i ZIP-paki sisu:
   ```bash
   unzip -l /home/kali/Desktop/VALVUR_TULEMUSED/VALVUR_*.zip
   
   ```
 2. Ava leidude failid ja registreeri kõik hälbed piletisüsteemis (**TicketingServer-itskteam9**). Priority: **High** / **Critical**.
### SAMM 6: Linuxi süvaanalüüs ja REAKTIIVNE TÕRJE (INTRAWEB1 / ruuter)
Kui VALVUR andis vihje aktiivsest ründajast, jahi ta esmalt taga ja seejärel elimineeri ligipääsud.
```bash
# 6.1 – Tuvasta aktiivsed olemid
w && who -a

# 6.2 – Võrk reaalajas (Otsi taga porte 4444, 1337, 8888 jne)
sudo netstat -nputw | grep ESTABLISHED

# 6.3 – Kahtlase protsessi PID põhjal faili asukoha tuvastamine
sudo ls -l /proc/[PID]/exe

```
#### 🛠️ UUS: 6.6 – Ründaja sessioonide ja protsesside TAPMINE (Kill)
```bash
# A. Viska ründaja reaalajas terminalist (nt pts/0) välja
sudo pkill -kill -t pts/0

# B. Tapa pahavara / Reverse Shell protsess sunnitult (SIGKILL)
sudo kill -9 [PID]

```
#### 🛠️ UUS: 6.7 – Püsivuspunktide ja tagauste EEMALDAMINE
```bash
# A. Puhasta ajastatud toimingud (Otsi ründaja skripte ja kustuta rida)
sudo crontab -e
# Vaata ja kustuta failid ka nendest kaustadest:
sudo rm -f /etc/cron.d/[kahtlane_fail]
sudo rm -f /var/spool/cron/crontabs/[kasutajanimi]

# B. SSH tagaakna eemaldamine (Kustuta ründaja avalik võti)
sudo nano ~/.ssh/authorized_keys
# Kontrolli ka teiste kasutajate ja root kausta võtmeid!

# C. Kontrolli pahatahtlikke systemd teenuseid
sudo systemctl stop [teenuse_nimi]
sudo systemctl disable [teenuse_nimi]
sudo rm -f /etc/systemd/system/[teenuse_nimi].service
sudo systemctl daemon-reload

```
#### Web Shelli otsing ja eemaldamine (veebiserver)
```bash
# Otsi viimati muudetud või kahtlase sisuga PHP faile
sudo find /var/www/html/ -name "*.php" -newer /var/www/html/index.php
sudo grep -rn "eval\|base64_decode\|shell_exec\|system(" /var/www/html/

# Kustuta leitud Web Shell
sudo rm -f /var/www/html/[pahalase_fail].php

```
#### Tulemüüri esmaabi (SSH elupäästja!)
```bash
# KRIITILINE: Luba alati SSH enne UFW aktiveerimist!
sudo ufw allow from 192.168.10.0/24 to any port 22 proto tcp
sudo ufw enable

```
### SAMM 7: Windowsi süvaanalüüs ja REAKTIIVNE TÕRJE (DC1 / FileSRV1)
**Kus:** RDP sessioon → **Command Prompt (Admin)** või **PowerShell (Admin)**.
#### 7.1 – Võrguühendused (kes ja kuhu?)
```cmd
REM Tuvasta aktiivsed ühendused ja võta paha protsessi PID
netstat -fano | findstr ESTABLISHED

```
#### 🛠️ UUS: 7.6 – Windowsi pahavara protsessi TAPMINE (Taskkill)
```cmd
REM A. Tapa pahavara / PowerShell ründevektor sunnitult (/F) PID järgi
taskkill /F /PID [Käsklusest_saadud_PID]

REM B. Kui ründaja jooksutab pahavara nimega (nt "nc.exe" või "backdoor.exe")
taskkill /F /IM "kahtlane_fail.exe"

```
#### 🛠️ UUS: 7.7 – Püsivuspunktide ja tagauste EEMALDAMINE
Kasuta **Autoruns64.exe** (Options ➔ Hide Microsoft Entries).
```
💻 Autoruns aknas eemaldamine:
   Tee kahtlasel kirjel (nt Scheduled Tasks või Logon all) paremklikk ➔ Vali "Delete".

```
##### Kui Autorunsi pole ja pead tegema käsitsi käsurealt:
```cmd
REM A. Kustuta pahatahtlik ajastatud toiming (Task Scheduler)
schtasks /delete /tn "RündajaToominguNimi" /f

REM B. Kustuta kahtlased käivitusvõtmed Registryst
reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "PahalaseKirjeNimi" /f
reg delete "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v "PahalaseKirjeNimi" /f

REM C. Puhasta Startup kaustad (Kustuta .lnk või .vbs failid)
del "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup\kahtlane_fail.lnk"

```
#### 7.4 – Administraatorite rühma puhastus
```cmd
REM Vaata liikmed üle
net localgroup Administrators

REM Kustuta ründaja poolt loodud või omavoliliselt gruppi lisatud konto
net localgroup Administrators [paha_kasutaja] /delete

```
### SAMM 8: Raporti koostamine (esitluseks)
Iga leitud anomaalia vormista slaididele/raportisse järgmiselt:
```markdown
## Leid #1: [Nimi]

| Väli | Väärtus |
|------|---------|
| **Tuvastatud tegevus** | Ründaja aktiivne Reverse Shell pordil 4444 |
| **Kasutatud tööriist** | `netstat -fano` / Sysinternals Autoruns64 |
| **Tõend / Tõrje** | PID 4128 (`powershell.exe`) tapetud käsuga `taskkill /F /PID 4128` |
| **MITRE ATT&CK** | T1059.001 – Command and Scripting Interpreter: PowerShell |
| **E-ITS 2024** | CON.1.M2 – Tulemüüride puudumine (deaktiveeritud olek) |
| **NIST CSF** | RESPOND (RS.MI-01) – Intsidendi isoleerimine ja leevendamine |
| **Soovitus** | Aktiveerida Windows Firewall rühmaloodud reeglitega. |

```
## ⚡ REAKTIIVNE ABILINK (Eksami ajal kopeerimiseks)
```bash
# ===== LINUXI TÕRJE KIIRKÄSUD =====
sudo pkill -kill -t pts/0                       # Väljaviskamine terminalist
sudo kill -9 [PID]                              # Protsessi sunnitud tapmine
sudo rm -f /var/www/html/[shell].php           # Web Shelli eemaldamine
sudo ufw enable                                 # Tulemüüri lukustus

# ===== WINDOWSI TÕRJE KIIRKÄSUD =====
taskkill /F /PID [PID]                          # Protsessi sunnitud tapmine CMD-st
Stop-Process -ID [PID] -Force                   # Protsessi sunnitud tapmine PS-ist
schtasks /delete /tn "ToomingaNimi" /f          # Ajastatud ründe eemaldamine
net localgroup Administrators [kasutaja] /delete # Paha adminni eemaldamine

```
> **VALVUR reaktiivne deklaratsioon:** *"Süsteem puhastatud aktiivsetest ründevektoritest. Tagaüksed eemaldatud mälust (SIGKILL/Taskkill) ja püsivuspunktid likvideeritud (crontab/schtasks). Keskkond viidud vastavusse E-ITS baasturvalisuse nõuetega."*
> 
