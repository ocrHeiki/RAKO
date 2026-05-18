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
#   |   LOODUD:      2026-05-18                                           |   #
#   |   AUTOR:       Heiki Rebane (Team 9 - HeRe)                        |   #
#   |   KIRJELDUS:   Eksami samm-sammuline töövoog. E-ITS audit,          |   #
#   |                reaktiivne forensika, intsidentide haldus Kali       |   #
#   |                masinast kaughalduse teel.                           |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```
# 🚀 EKSAMI TÖÖVOOG & SPIKKER — TEAM 10: HeRe

See töövoog on optimeeritud keskkonna **itskteam10** proaktiivseks auditeerimiseks
(E-ITS 2024), reaktiivseks forensikaks (MITRE ATT&CK) ja intsidentide
tsentraalseks lahendamiseks otse analüütiku Kali masinast.

---

## 📅 0. ETTEVALMISTUSKORD (Tee laboris esimese asjana)

Kui sihtmärk-masinad vSphere'is kloonivad, sisesta need käsud Kali terminali.
See võtab aega alla minuti – aga kui SSH server ei jookse, ei saa VALVUR
tulemusi tagasi saata.

```bash
# 1. Uuenda paketid ja paigalda tööriistad
sudo apt update && sudo apt install -y mc nmap zenmap-kbx net-tools iproute2 freerdp2-x11

# 2. Käivita SSH server (vajalik VALVUR-i failide vastuvõtmiseks)
sudo systemctl enable ssh && sudo systemctl start ssh

# 3. Kontrolli, et SSH kuulab
ss -tlnp | grep 22
```

---

## 🏁 SAMM-SAMMULINE TÖÖVOOG LABORIS

### SAMM 1: Virtuaaltaristu kaitse (kloonimine)

**Tegevus:** Enne kui teed ühegi masina terminali lahti, **tee vSphere
keskkonnas kõigist itskteam10 masinatest kloon või snapshot**.

**Miks?** Forensiline kuldreegel (ISO 27037). Kui tulemüür su kaughalduse
välja lukustab või süsteem rikneb, saad sekundiga algseisu tagasi.

---

### SAMM 2: Võrgu baasjoone kaardistamine (nmap)

**Tegevus:** Käivita Kali masinas võrgu skaneerimine:

```bash
# Kiire elusate tuvastus
sudo nmap -sn 192.168.10.0/24 -oG - | grep Up

# Põhjalik port + OS tuvastus (jäta taustale)
sudo nmap -sV -O 192.168.10.0/24 &
```

**Eesmärk:** Fikseerida ründaja poolt avatud pordid enne meie sekkumist.
Jäta skaneerimine taustale jooksma – hiljem saad võrrelda VALVUR-i enda
tekitatud liiklust ründaja omast.

**Näidisväljund:**
```
Nmap scan report for 192.168.10.10 (itsh-eksam-dc01)
Host is up (0.0012s latency).
PORT     STATE  SERVICE     VERSION
22/tcp   open   ssh         OpenSSH 9.2
RDP/tcp  open   ms-wbt-server Microsoft RDP
...

Nmap scan report for 192.168.10.20 (itsh-eksam-ruuter)
PORT     STATE  SERVICE
22/tcp   open   ssh
80/tcp   open   http
...
```

---

### SAMM 3: Kaughaldusühenduste loomine

| Masin | Protokoll | Käsk |
|-------|-----------|------|
| **Linux (ruuter, server, Kali)** | SSH | `ssh kasutaja@192.168.10.X` |
| **Windows (DC, file server)** | RDP | `xfreerdp /v:192.168.10.Y /u:Administrator /p:Parool123 /dynamic-resolution +clipboard` |

```bash
# SSH Linuxi
ssh heiki@192.168.10.10

# RDP Windowsi
xfreerdp /v:192.168.10.20 /u:Administrator /p:Parool123 /dynamic-resolution +clipboard
```

> ⚡ **Nipp:**  Kõik edasised tegevused teed juba kaughalduse kaudu.
> KUI RDP katkeb, on sul ikka nmap ja SSH olemas.

---

### SAMM 4: VALVUR-i käivitamine (ühe rea githubi käsklus)

Selleks, et mitte saastada uuritavate masinate kõvakettaid püsivate
jälgedega, käivitatakse VALVUR otse mälust GitHubi repositooriumist.
Kali IP tuvastatakse automaatselt `$SSH_CLIENT` põhjal – **pole vaja
käsitsi ette anda**.

#### 🐧 Linuxi sihtmärk (INTRAWEB1 / ruuter / TicketingServer)

```bash
# Lihtsalt kleebi – KALI_IP tuleb $SSH_CLIENT seest
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.py)"
```

> ⚡ **Eksami kuldvariant:**  SSH-d sisse → kleebi see rida → tulemused
> jõuavad ise SCP-ga Kali töölauale.

Kui `$SSH_CLIENT` millegipärast ei tööta (nt sudule lisati `sudo -E`):

```bash
sudo -E python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.py)"
```

#### 💻 Windowsi sihtmärk (DC1 / FileSRV1) – PowerShelli kaudu

```powershell
$env:KALI_IP="192.168.10.50"; iex (iwr -UseBasicParsing "https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.ps1")
```

#### 📋 VALVUR menüüvalikud

```
======================================================================
  1. FAAS 1+2 – Terviklus + Logifiltreering (KIIRANALÜÜS)
  2. FAAS 4   – E-ITS 2024 baasturvalisuse audit
  3. KÕIK MOODULID – Täielik analüüs (FAAS 1–5)
  4. Ekspordi tulemused käsitsi (ilma uue analüüsita)
  5. Seadista kaughalduse eksfiltreerimine
  6. Välju
======================================================================
```

| Valik | Millal kasutada | Mida ütled komisjonile |
|-------|-----------------|------------------------|
| **1** | Aega napib, ainult kiire turvafiltreering | "FAAS 1+2 – tervikluskontroll ja turvafiltreering. SHA-256 räsid ja MITRE märksõnad." |
| **2** | E-ITS baasturvalisuse hindamine | "FAAS 4 – E-ITS 2024 audit: tulemüür, paroolipoliitika, auditlogimine, võrk." |
| **3** | Täielik intsidendianalüüs | "Kõik 5 faasi, 14 moodulit – terviklusest lõppraportini NIST CSF 2.0 raamistikus." |

---

### SAMM 5: Intsidentide haldus (ticketid)

1. Vaata Kali töölauale laekunud VALVUR-i ZIP-paki sisu:
   ```bash
   ls -la /home/kali/Desktop/VALVUR_TULEMUSED/
   unzip -l /home/kali/Desktop/VALVUR_TULEMUSED/VALVUR_*.zip
   ```

2. Ava `34_tulemus_eits_vastavus.txt` ja `11_tulemus_turvafiltreering.csv`
   ```bash
   cat /home/kali/Desktop/VALVUR_TULEMUSED/34_tulemus_eits_vastavus.txt
   ```

3. Registreeri kõik leitud E-ITS hälbed ja võrguandmed koheselt
   piletisüsteemis (**TicketingServer-itskteam10**).
   Priority: **High** / **Critical**.

---

### SAMM 6: Linuxi süvaanalüüs (INTRAWEB1 / ruuter)

Kui VALVUR andis vihje aktiivsest ründajast, jahi teda SSH sessioonis:

```bash
# 6.1 – Reaalajas olemid
w && who -a

# 6.2 – Võrk reaalajas (ESTABLISHED ühendused)
sudo netstat -nputw | grep ESTABLISHED

# 6.3 – Kahtlase protsessi PID → pahavara asukoht
sudo ls -l /proc/[PID]/exe

# 6.4 – Püsivuspunktid (cron, systemd)
sudo crontab -e
ls -la /etc/cron.d/
ls -la /etc/systemd/system/multi-user.target.wants/

# 6.5 – SSH võtmed (backdoor)
ls -la ~/.ssh/authorized_keys
cat ~/.ssh/authorized_keys
```

#### Web Shelli otsing (veebiserver)

```bash
# Veebilogid vs rakenduse failid – kõrvuta mc-ga
sudo mc

# Vasak paneel: /var/log/nginx/access.log
# Parem paneel: /var/www/html/

# Otsi kahtlaseid faile veebikaustast
sudo find /var/www/html/ -name "*.php" -newer /var/www/html/index.php
sudo grep -rn "eval\|base64_decode\|shell_exec\|system(" /var/www/html/
```

#### Tulemüüri esmaabi (SSH elupäästja!)

```bash
# KRIITILINE: Luba alati SSH enne UFW aktiveerimist!
sudo ufw allow from 192.168.10.0/24 to any port 22 proto tcp
sudo ufw enable
sudo ufw status numbered
```

---

### SAMM 7: Windowsi süvaanalüüs (DC1 / FileSRV1)

**Kus:**  RDP sessioon (`xfreerdp`) → Windowsi töölaud → **Command Prompt (Admin)** või **PowerShell (Admin)**

Ava administraatori käsurida:
- Vajuta `Win + R`, kirjuta `cmd` või `powershell`
- Parem klõps → **Run as administrator**
- Või: `Win + X` → **Windows Terminal (Admin)**

#### 7.1 – Võrguühendused (kes ja kuhu?)

Selles masinas (DC või FileSRV) kontrolli, kas keegi on väljapoole ühenduses:

```cmd
REM Kõik aktiivsed TCP ühendused koos PID-ga
netstat -fano | findstr ESTABLISHED
```

**Tulemus:**  otsi võõraid välis-IP-sid ja porte (4444, 1337, 8080 jms).
Kui leiad midagi kahtlast, võta PID:

```cmd
REM PID → faili nimi
tasklist /FI "PID eq 1234"

REM PID → täpne faili asukoht
wmic process where "processid=1234" get name,executablepath
```

Näidis:
```
TCP    192.168.10.20:445     192.168.10.50:49152    ESTABLISHED  1234
                                                                    ^^^^
PID 1234 → tasklist → svchost.exe (normaalne)
PID 1234 → tasklist → powershell.exe (kahtlane – uuri edasi)
```

#### 7.2 – Jagamised ja failide liikumine

Kes parasjagu faile tõmbab?

```cmd
REM Käsurea variant (kiire)
net session

REM Graafiline variant (põhjalikum)
compmgmt.msc
```
`compmgmt.msc` aknas:  **System Tools → Shared Folders → Sessions**
- Vaata, kas keegi on ühenduses väljastpoolt domeeni
- Vaata **Open Files** – mida nad loevad/kirjutavad

Kõik jagamised ülevaates:

```cmd
REM Administratiivsed jagamised (ADMIN$, C$, IPC$) – need on normaalsed
REM Mitte-administratiivsed jagamised – need on kahtlased
net share
```

PowerShell-iga täpsemalt:

```powershell
# Näita ainult mitte-administratiivseid jagamisi
Get-SmbShare | Where-Object {$_.Special -eq $false} | Format-Table Name, Path, Description
```

#### 7.3 – Püsivus (automaatsed käivituskohad)

Ründaja tahab, et tema tagauks käivituks uuesti pärast taaskäivitust.
Leia need kohad:

##### 7.3.1 – Autoruns (Sysinternals) – kõige põhjalikum

**ABB:**  Kui Autoruns on juba masinas olemas, käivita see KOHE:

```
💻 RDP aknas:  File Explorer → C:\Tools\Autoruns\ → Autoruns64.exe
💻 Või:        Win + R → C:\Tools\Autoruns\Autoruns64.exe → Enter
```

**Kui Autorunsi pole:**  lae ise alla (RDP-s on internet tavaliselt olemas):

```
💻 RDP aknas:  Ava https://download.sysinternals.com/files/Autoruns.zip
💻 Või käsurealt:
   curl -L https://download.sysinternals.com/files/Autoruns.zip -o %TEMP%\Autoruns.zip
   tar -xf %TEMP%\Autoruns.zip -C %TEMP%
   %TEMP%\Autoruns64.exe
```

**Pärast Autorunsi käivitamist (7 sammu):**

| # | Tegevus | Mida otsid |
|---|---------|------------|
| 1 | **File → Hide Microsoft Entries** | Eemaldab kõik Microsofti omakirjad – jäävad ainult kolmandate osapoolte omad |
| 2 | Vaata sakki **Scheduled Tasks** | Ootamatud nimed, `UpdateCheck.vbs`, `BrowserHelper` |
| 3 | Vaata sakki **Logon** | Kahtlased `.exe`-d, mis käivituvad iga kasutaja sisselogimisel |
| 4 | Vaata sakki **Services** | Teenused, mida pole Microsofti poolt allkirjastatud |
| 5 | Vaata sakki **Run / RunOnce** | Registry võtmed – otsi `%TEMP%` või `%APPDATA%` teid |
| 6 | Vaata sakki **Winlogon** | Shell replacement – kui siin on midagi peale `explorer.exe`, on pahavara |
| 7 | Vaata sakki **AppInit** | Kõige sügavam püsivus – DLL-id, mis laaditakse igasse protsessi |

> ⚡ **Kriitiline leid:**  kui Autoruns näitab kirjet, mis viitab `C:\Users\Public\`
> või `C:\Windows\Temp\` – see on tugev indikaator pahavarast.

##### 7.3.2 – Kui Autorunsi pole üldse saadaval (käsurea variant)

Käivita need käsud **Command Prompt (Admin)** järjest:

```cmd
REM ===== 1. Plaanitud ülesanded =====
schtasks /query /fo LIST /v | findstr /i "TaskName Task To Run"

REM ===== 2. Registry Run võtmed =====
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce"
reg query "HKLM\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"

REM ===== 3. Startup kaustad =====
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
dir "%PROGRAMDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM ===== 4. WMI püsivus (kõige raskemini leitav) =====
wmic /NAMESPACE:"\\root\subscription" PATH __EventFilter GET *
wmic /NAMESPACE:"\\root\subscription" PATH CommandLineEventConsumer GET *
wmic /NAMESPACE:"\\root\subscription" PATH __FilterToConsumerBinding GET *
```

#### 7.4 – Administratorite rühm

Kes kõik saavad masinat administreerida?

```cmd
net localgroup Administrators
```

PowerShell-iga täpsemalt (kuvab ka allika – kas kohalik või domeenist):

```powershell
Get-LocalGroupMember -Group Administrators | Format-Table Name, PrincipalSource
```

**Otsi:**  Kas on kasutajaid, kes pole `Administrator` ega `Domain Admins`?
Kas on kontosid nimega `support_388945a0` või `backup_user`?

#### 7.5 – Logide analüüs (VALVUR)

Kui VALVUR on juba sihtmasinas kloonitud (kaughalduse kaudu):

```cmd
REM Käivita VALVUR moodulid otse kohalikust kloonist
cd C:\Users\%USERNAME%\Desktop\VALVUR\SKRIPTID

REM Turvafiltreering (kriitilised sündmused)
python 11_turvafiltreering.py

REM E-ITS audit
python 34_eits_vastavus.py
```

---

### SAMM 8: Raporti koostamine (esitluseks)

Iga leitud anomaalia vormista slaididele järgmiselt:

```markdown
## Leid #1: [Nimi]

| Väli | Väärtus |
|------|---------|
| **Tuvastatud tegevus** | Ründaja sessioon Linuxis cron töö ülesandena |
| **Kasutatud tööriist** | `crontab -e` / `netstat -nputw` |
| **Tõend** | `/var/log/auth.log` – sisselogimine kl 03:14 |
| **MITRE ATT&CK** | T1053.003 – Scheduled Task/Job: Cron |
| **E-ITS 2024** | SYS.1.3.M1 – Linuxi süsteemiturve |
| **NIST CSF** | DETECT (DE.CM-01) – Protsessi jälgimine |
| **Soovitus** | Keela root SSH, paigalda auditd ja Fail2ban |
```

#### Kokkuvõtlik tabel esitluse lõpus

| Masin | Leitud | E-ITS tase | MITRE |
|-------|--------|------------|-------|
| itsh-eksam-dc01 | 12 leidu | ⚠ KESK (M) | T1003, T1078 |
| itsh-eksam-ruuter | 8 leidu | ✓ KESK (M) | T1046 |
| itsh-eksam-fileserver | 15 leidu | ⚠ STANDARD (A) | T1490 |
| itsh-eksam-kali | 5 leidu | ✓ KÕRG (S) | – |
| client01 | 3 leidu | ✓ KESK (M) | T1059 |

---

## ⚡ KIIRVIITED (Eksami hetkel)

```bash
# ===== KALI ettevalmistus =====
sudo systemctl enable ssh --now
sudo nmap -sV -O 192.168.10.0/24 &

# ===== Linuxi sihtmärk (SSH) =====
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.py)"

# ===== Windowsi sihtmärk (RDP -> PowerShell) =====
$env:KALI_IP="192.168.10.50"; iex (iwr -UseBasicParsing "https://raw.githubusercontent.com/ocrHeiki/VALVUR/main/launch_VALVUR.ps1")

# ===== Tulemuste vaatamine Kali peal =====
unzip /home/kali/Desktop/VALVUR_TULEMUSED/VALVUR_*.zip -d /tmp/valvur_tulemused/
cat /tmp/valvur_tulemused/34_tulemus_eits_vastavus.txt
cat /tmp/valvur_tulemused/11_tulemus_turvafiltreering.csv

# ===== Windowsi püsivuse käsitsi kontroll (kui Autoruns pole) =====
schtasks /query /fo LIST /v | findstr /i "TaskName Task To Run"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
dir "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

# ===== REAKTIIVNE (kui VALVUR näitab ründajat) =====
sudo netstat -nputw | grep ESTABLISHED
sudo ls -l /proc/[PID]/exe
sudo crontab -e
```

---

## 📝 MITRE ATT&CK & E-ITS 2024 KIIRVIIT

| Tehnika | MITRE ID | E-ITS meede | Tase |
|---------|----------|-------------|------|
| Credential Dumping | T1003 | ORP.4.A2 | KÕRG |
| Scheduled Task/Job | T1053 | SYS.1.1.A6 | STANDARD |
| Command and Scripting Interpreter | T1059 | ORP.4.M22 | KESK |
| Remote Services: SSH | T1021 | CON.1.A1 | STANDARD |
| Data Encrypted for Impact | T1486 | INF.1.A1 | KESK |
| Inhibit System Recovery | T1490 | INF.1.A1 | KESK |
| Obfuscated Files or Information | T1027 | ORP.4.M22 | KESK |
| Account Manipulation | T1098 | ORP.4.A2 | KÕRG |
| Network Service Scanning | T1046 | CON.1.M1 | KESK |
| Boot or Logon Autostart Execution | T1547 | SYS.1.1.A6 | STANDARD |

---

## NIST CSF 2.0 & E-ITS 2024 VASTAVUS

```
IDENTIFY  ─┬─ CON.1   (võrgu kaardistus)
           ├─ SYS.1   (süsteemi inventar)
           └─ NET.1   (võrguseadmed)

PROTECT   ─┬─ CON.1.M2   (tulemüür)
           ├─ SYS.1.3.M3 (uuendused)
           ├─ ORP.4.A1   (paroolipoliitika)
           ├─ INF.1.A1   (varundus)
           └─ APP.1.M1   (TLS/SSL)

DETECT    ─┬─ ORP.4.M22  (logimine – auditd/auditpol)
           ├─ CON.1.A1   (Fail2ban)
           └─ SYS.1.3.A1 (AIDE/Tripwire)

RESPOND   ─┬─ SYS.1.3.A1 (tervikluse kontroll)
           └─ 34_eits_vastavus.py (soovitused)

RECOVER   ─── INF.1.A1   (varunduse staatus)
```

---

> **VALVUR motto:**  *"Analüüs teostatud süsteemi kloonil. Terviklus
> tagatud SHA-256 räsiga (NIST ID.SC-01). Tulemused kättesaadavad Kali
> töölaual."*
>
> **Team 10 – HeRe:** Heiki Rebane
