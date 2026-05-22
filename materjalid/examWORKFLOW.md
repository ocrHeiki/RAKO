# Täielik Juhend: Windows 10 Logianalüüs (Hayabusa) ja Tulemuste Uurimine (VisiData) Läbi Kali Linuxi

See dokument on terviklik samm-sammuline juhend digitaalse ekspertiisi ja intsidentide lahendamise (DFIR) läbiviimiseks laborikeskkonnas.
## 1. SAMM: Windows 10 Ettevalmistus, SSH Lubamine ja IP Tuvastamine

Seda teed kooli Windowsi masinas PowerShellis (Run as Administrator).

Selleks, et saaksid Windowsi masinat hallata ja faile liigutada otse Kali Linuxi terminalist, tuleb Windowsis aktiveerida OpenSSH server ja kontrollida võrguseadeid.
PowerShell

- 1. Paigalda OpenSSH Serveri komponent
    Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0

- 2. Seadista OpenSSH teenus käivituma automaatselt ja käivita see kohe
    Set-Service -Name sshd -StartupType 'Automatic'
    Start-Service sshd

- 3. Kontrolli, kas SSH teenus reaalselt töötab (peab kuvama staatuseks "Running")
Get-Service sshd

- 4. Loo tulemüüri reegel, mis lubab sissetulevaid SSH ühendusi (port 22)
    New-NetFirewallRule -Name 'OpenSSH-In' -DisplayName 'OpenSSH Server (Inbound)' -Profile Any -Direction Inbound -Action Allow -Protocol TCP -LocalPort 22

- 5. TUVASTA WINDOWSI IP-AADRESS
# Otsi väljundist oma võrgukaardi nime alt rida "IPv4 Address" (nt. 192.168.1.232)
    ipconfig

## 2. SAMM: Tööriistade Allalaadimine ja Paigaldamine Kali Linuxis

Seda teed Kali Linuxi kohalikus terminalis (mitte SSH aknas).

Laadime vajalikud failid esmalt alla Kali masinasse, et vältida probleeme Windowsi virtuaalmasina võimalike võrgu- või DNS-tõrgetega.
Bash

- 1. Liigu kasutaja Downloads (Allalaadimised) kausta
    cd ~/Downloads

- 2. Laadi alla Hayabusa stabiilne Windowsi 64-bitine versioon (v3.9.0) otse GitHubist
    wget https://github.com/Yamato-Security/hayabusa/releases/download/v3.9.0/hayabusa-3.9.0-win-x64.zip

- 3. Uuenda Kali paketihaldurit ja paigalda Pythoni paketihaldur pip
    sudo apt update && sudo apt install -y python3-pip

- 4. Paigalda ülikiire terminalipõhine CSV-andmete vaataja VisiData
    pip install visidata --break-system-packages

## 3. SAMM: Failide saatmine Kalist Windowsisse (SCP)

Seda teed Kali Linuxi kohalikus terminalis.

Liigutame allalaaditud zip-arhiivi üle võrgu otse Windowsi masina C-kettale, kasutades turvalist SCP krüpteeringut.
Bash

# Saada Hayabusa zip-fail Windowsi masina C:\ juurkataloogi
# MÄRKUS: Asenda 'tempuser' ja '192.168.1.232' oma Windowsi tegeliku kasutajanime ja IP-ga!
    scp hayabusa-3.9.0-win-x64.zip tempuser@192.168.1.232:C:/

Küsimisel sisesta Windowsi kasutaja parool.
# 4. SAMM: Paigaldus ja Logianalüüs Läbi SSH Käsurea

Nüüd logid Kali terminalist SSH-ga Windowsisse sisse ja teed analüüsi distantsilt.
Bash

- 1. Loo SSH ühendus Windowsi masinaga (Asenda kasutaja ja IP!)
    ssh tempuser@192.168.1.232

- 2. Windowsi käsureale jõudes käivita kohe PowerShell keskkond
**powershell**

Järgmised käsud jooksevad juba Windowsi operatsioonisüsteemi sees (läbi SSH):
    PowerShell

- 3. Loo uus sihtkaust C:\hayabusa
    New-Item -ItemType Directory -Force -Path "C:\hayabusa"

- 4. Liiguta varem SCP-ga saadetud zip-fail uude kausta
    Move-Item "C:\hayabusa-3.9.0-win-x64.zip" "C:\hayabusa\"
    cd C:\hayabusa

- 5. Paki arhiiv lahti ja kustuta vana zip-fail
    Expand-Archive -Path "hayabusa-3.9.0-win-x64.zip" -DestinationPath "C:\hayabusa" -Force
    Remove-Item "hayabusa-3.9.0-win-x64.zip"

- 6. Mugavuse huvides nimeta pikk käivitatav fail ümber lühemaks
    Rename-Item "hayabusa-3.9.0-win-x64.exe" "hayabusa.exe"

- 7. Laadi alla kõige uuemad Sigma tuvastusreeglid GitHubist
    .\hayabusa.exe update-rules

- 8. Käivita reaalajas kohalike sündmuslogide (Event Logs) analüüs
    .\hayabusa.exe csv-timeline --live-analysis --output tulemus.csv

- 9. Pärast edukat analüüsi välju PowerShellist ja sulge SSH ühendus
    exit
    exit

## 5. SAMM: Raporti Tõmbamine Kalisse ja Analüüs VisiData-s

Oled tagasi Kali Linuxi kohalikus terminalis (~/Downloads kaustas).
Bash

- 1. Kopeeri valmis CSV fail Windowsist endale kohalikku Kali masinasse
- NB! Pane kindlasti tähele TÜHIKUT ja PUNKTI (.) käsu päris lõpus!
  scp tempuser@192.168.1.232:C:/hayabusa/tulemus.csv .

- 2. Ava raport sekundiga VisiData interaktiivse tabelina
    vd tulemus.csv

💡 VisiData Interaktiivsed Kiirkäsud (Spikker)
Klahv / Sümbol	Tegevus ja Selgitus
Nooleklahv / TAB	Liikumine tabeli ridade ja veergude vahel.
[ (Vasak sulg)	Sorteerib veeru kahanevalt. Liigu veeru Level peale ja vajuta seda, et tuua Critical ja High ohud kohe etteotsa.
] (Parem sulg)	Sorteerib valitud veeru kasvavalt.
/ (Kaldkriips)	Otsing. Sisesta ründe märk (nt. mimikatz, psexec, cmd.exe) ja vajuta Enter.
n	Hüppab järgmise samasuguse otsingutulemuse juurde.
| (Püstkriips)	Märgistamine. Trüki otsisõna (nt Critical), et märgistada kõik vastavad read kollaseks.
" (Jutumärk)	Filtreerimine. Tõstab kõik eelnevalt märgistatud read täiesti uuele puhtale vahelehele.
g ja siis q	Sulgeb praeguse aktiivse filtri-vahelehe.
q	Sulgeb VisiData ja viib tagasi tavalisele Linuxi käsureale.
