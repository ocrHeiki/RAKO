# Pille Porgandi Juhtumi Lahendamise Töövoog (VMware & IR)

See juhend kirjeldab samm-sammult tegevusi VMware keskkonnas, kasutades eraldi virtuaalseid kettaid tööriistade ja tõendite jaoks.

## IR KASUTAJA TUNNUSED
* **Kasutaja:** Kasutaja
* **Parool:** Parool123456@
* **Roll:** Local Administrator / Incident Responder

---

## 1. SAMM: Ettevalmistus (Päris arvutis, ENNE VM-i käivitamist)
Lood oma päris arvutis "mälupulga" laadse ketta, et viia skriptid isoleeritud masinasse.
1. **Päris arvutis:** Win + X -> Disk Management -> Action -> Create VHD.
2. **Seaded:** `C:\IR_Tools.vhdx`, suurus 500MB, VHDX, Fixed Size.
3. **Sisu:** Initialize (GPT) -> New Simple Volume -> Kopeeri siia kõik vajalikud skriptid ja `eventID.md`.
4. **Väljutamine:** Paremklõps Disk Managementis sellel kettal -> **Detach VHD**.
5. **VMware seaded:** VM Settings -> Add -> Hard Disk -> Use an existing virtual disk -> Vali loodud `IR_Tools.vhdx`.

---

## 2. SAMM: Masina käivitamine ja isolatsioon
1. **VMware seaded:** Võta võrgukaardilt märge "Connected" ja "Connect at power on" ära.
2. **Käivita VM:** Logi sisse IR-kasutajaga.
3. **Snapshot:** Tee kohe Snapshot (Nimi: "Algseis enne analüüsi").

---

## 3. SAMM: Tõendite ketta loomine (VM-i sees)
Loo masina sees teine puhas konteiner, kuhu kogud uurimise käigus leitud failid.
1. **VM-i sees:** Disk Management -> Action -> Create VHD.
2. **Seaded:** `C:\evidence.vhdx`, suurus 2GB, VHDX.
3. **Kasutuselevõtt:** Initialize -> New Simple Volume (Drive **E:**).

---

## 4. SAMM: Analüüs ja skriptid
Sinu tööriistad on nüüd nähtavad uue kettana (nt **D:**). Ava PowerShell administraatorina ja kasuta neid:


# Sisselogimiste kontroll (Otsime ID 4624 sündmusi)
```powershell
Get-EventLog -LogName Security -InstanceId 4624 -After (Get-Date).AddDays(-1) | 
Select-Object TimeGenerated, @{N='User';E={$_.ReplacementStrings[5]}}, @{N='Source_IP';E={$_.ReplacementStrings[18]}} | 
Format-Table -AutoSize
```
# Kahtlaste protsesside otsimine Temp kaustadest
```powershell
Get-Process | Select-Object Name, Id, Path | 
Where-Object {$_.Path -like "*\Temp\*" -or $_.Path -like "*\AppData\Local\*"}
```
5. SAMM: Failide kogumine ja väljutamine

    Kopeeri leitud pahavara E-kettale: Copy-Item -Path "C:\kahtlane\asukoht\fail.exe" -Destination "E:\"

    Eemalda oht süsteemist: Remove-Item -Path "C:\kahtlane\asukoht\fail.exe" -Force

    Väljuta tõendite ketas: Disk Management -> Paremklõps Disk (vasakul paneelis) -> Detach VHD.

    Kättesaamine: Kopeeri evidence.vhdx fail VM-ist välja (nt VMware Drag & Drop abil), et seda turvalises masinas edasi uurida.

6. SAMM: Turvapoliitika lubamine skriptideks

Kui skriptid ei käivitu, kasuta seda käsku:
```PowerShell
Set-ExecutionPolicy Bypass -Scope Process
```
MÄRKUS: Kuna võrk on maas ja ligipääs DC-le puudub, on see Win10 masin sinu ainus infoallikas. Logi üles kõik leitud IP-aadressid ja protsesside nimed!
