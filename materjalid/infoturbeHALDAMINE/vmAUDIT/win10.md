Pille Porgandi Juhtumi Lahendamise Töövoog (VMware & IR)

See juhend kirjeldab samm-sammult tegevusi VMware keskkonnas ja vajalikke PowerShelli skripte.
IR Kasutaja Tunnused

    Kasutaja: Kasutaja

    Parool: Parool123456@

1. SAMM: Masina isoleerimine ja Snapshot (VMware)

Enne analüüsi tuleb takistada ründe levikut.

    Isolatsioon: Vali VMware'is TRL-Win10-01 -> Settings -> Network Adapter -> Võta märge ära "Connected" ja "Connect at power on" juurest.

    Snapshot: Paremklõps VM-il -> Snapshot -> Take Snapshot (Nimi: "Enne IR analüüsi").

2. SAMM: Sisselogimiste analüüs (Logide kontroll)

Logi sisse IR-kasutajaga ja ava PowerShell administraatori õigustes.
PowerShell

# Otsib edukaid sisselogimisi (ID 4624) viimase 24 tunni jooksul
Get-EventLog -LogName Security -InstanceId 4624 -After (Get-Date).AddDays(-1) | 
Select-Object TimeGenerated, @{N='User';E={$_.ReplacementStrings[5]}}, @{N='Source_IP';E={$_.ReplacementStrings[18]}} | 
Format-Table -AutoSize

3. SAMM: Kahtlaste protsesside tuvastamine

Uuri, mis põhjustas "kahtlased aknad" ekraanil.
PowerShell

# Otsib protsesse, mis jooksevad kahtlastest asukohtadest (nt Temp kaust)
Get-Process | Select-Object Name, Id, Path, Description | 
Where-Object {$_.Path -like "*\Temp\*" -or $_.Path -like "*\AppData\Local\*"} | 
Format-Table -AutoSize

4. SAMM: Võrguühenduste kontroll

Kontrolli, kas masinal oli aktiivseid ühendusi (see on kasulik, kui teed analüüsi vahetult peale isolatsiooni).
PowerShell

# Kuvab aktiivsed ühendused ja nendega seotud protsessi ID
Get-NetTCPConnection -State Established | 
Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess | 
Sort-Object RemoteAddress

5. SAMM: Failide ja skriptide haldus (Võrguta keskkond)

Kuna võrk on maas, kasuta kopeerimiseks VMware Tools "Drag and Drop" funktsiooni või teksti kopeerimist (Copy-Paste). Kui käivitad faile, kasuta:
PowerShell

Set-ExecutionPolicy Bypass -Scope Process
.\skripti_nimi.ps1

6. SAMM: Puhastus ja paroolipoliitika

    Kustuta fail: Kui leidsid pahaloomulise faili: Remove-Item -Path "C:\asukoht\fail.exe" -Force

    Parool: Vaheta Pille ja IR-kasutaja paroolid tugevamate vastu.
