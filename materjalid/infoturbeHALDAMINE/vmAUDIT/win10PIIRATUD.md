# IR Töövoog: Piiratud õigustega keskkond (Win10)

Seda juhendit kasuta siis, kui Disk Management on blokeeritud ja sa ei saa uusi virtuaalkettaid süsteemi haakida. Fookus on "elamisel maast" (Living off the Land).

## 0. IR KASUTAJA TUNNUSED
* **Kasutaja:** Kasutaja
* **Parool:** Parool123456@

---

## 1. SAMM: Ettevalmistus ja isoleerimine
Kuna uusi kettaid luua ei saa, pead skriptid masinasse saama läbi VMware lõikelaua (Copy-Paste) või mälupulga passthrough.

1. **Võrk välja:** VMware seaded -> Network Adapter -> Võta märge "Connected" pealt ära.
2. **Snapshot:** Tee VM-ist Snapshot ("Enne uuringut").
3. **Tööala loomine:** Kuna sa ei saa uut ketast, loo kaust uurimiseks:
   `New-Item -Path "C:\Users\Public\Documents\Uurimine" -ItemType Directory`

---

## 2. SAMM: Skriptide kopeerimine
Kui VMware Tools lubab, kopeeri skriptide tekst ja kleebi need Notepadiga failidesse:
* `C:\Users\Public\Documents\Uurimine\analuus.ps1`
* `C:\Users\Public\Documents\Uurimine\logid.ps1`

---

## 3. SAMM: Aktiivse ründe tuvastamine (Reaalajas)
Kuna ründaja võib olla veel sees, kontrolli kohe aktiivseid ühendusi ja sessioone.

```powershell
# 1. Vaata, kes on sisse logitud (kas peale sinu ja Pille on veel keegi?)
query user

# 2. Vaata võrguühendusi (otsi võõraid väliseid IP-sid)
netstat -ano | findstr "ESTABLISHED"

# 3. DNS vahemälu (kuhu masin on proovinud ühenduda?)
ipconfig /displaydns | Select-String "Record Name"
```
4. SAMM: Kahtlaste "akende" ja startup-toimingute leidmine

Pille nägi "kahtlaseid aknaid". Need käivituvad tavaliselt automaatselt.
```PowerShell
# 1. Kontrolli kasutaja startup kausta
Get-ChildItem "C:\Users\Pille\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

# 2. Kontrolli Registry Run võtmeid (mida Windows käivitab sisselogimisel)
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Run

# 3. Otsi .exe ja .ps1 faile Temp kaustadest
dir $env:TEMP -Filter *.exe, *.ps1 -Recurse -ErrorAction SilentlyContinue
```
5. SAMM: Logide analüüs ilma domeenikontrollerita

Kuna sul on ainult Win10, pead lootma kohalikule Security logile.
```PowerShell
# Otsi sisselogimisi (ID 4624). Pööra tähelepanu Logon Type 3 (Network) ja 10 (RDP)
Get-EventLog -LogName Security -InstanceId 4624 -After (Get-Date).AddDays(-1) | 
Select-Object TimeGenerated, @{N='User';E={$_.ReplacementStrings[5]}}, @{N='Source_IP';E={$_.ReplacementStrings[18]}}

# Otsi PowerShelli skriptide sisu (ID 4104)
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; ID=4104} -ErrorAction SilentlyContinue | 
Select-Object TimeCreated, Message | Format-List
```
6. SAMM: Tõendite kogumine (Exfiltration)

Kuna sa ei saa ketast väljutada, pead tõendid käsitsi VM-ist välja tõstma.

    Paki leiud kokku: Compress-Archive -Path "C:\Users\Public\Documents\Uurimine\*" -DestinationPath "C:\Users\Public\Documents\Tõendid.zip"

    Kopeeri välja: Proovi Tõendid.zip kopeerida (Drag & Drop) oma päris arvuti töölauale.

NIPP: Kui sa ei tea, milline aken on kahtlane, kasuta Task Manageri (Ctrl+Shift+Esc). Vali vahekaart Details, paremklõps tulpade päisel -> Select Columns -> vali Command Line. See näitab täpselt, millise käsuga aken avati.
