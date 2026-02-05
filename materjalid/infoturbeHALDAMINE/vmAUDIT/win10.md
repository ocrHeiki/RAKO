# Pille Porgandi Juhtumi Lahendamise Töövoog (VMware & IR)

See juhend kirjeldab samm-sammult tegevusi VMware keskkonnas ja vajalikke PowerShelli skripte.

## IR KASUTAJA TUNNUSED
* **Kasutaja:** Kasutaja
* **Parool:** Parool123456@

---

## 1. SAMM: Masina isoleerimine ja Snapshot (VMware)
Enne analüüsi tuleb takistada ründe levikut.
* **Isolatsioon:** VMware seaded -> Network Adapter -> Uncheck "Connected".
* **Snapshot:** Paremklõps VM-il -> Snapshot -> Take Snapshot (Nimi: "Enne IR analüüsi").

---

## 2. SAMM: Virtuaalse ketta (VHDX) loomine tõendite jaoks
Loo eraldi konteiner skriptide ja kahtlaste failide hoidmiseks.
1. **Ava Disk Management:** Win + X -> Disk Management.
2. **Loo ketas:** Action -> Create VHD.
   - Location: `C:\evidence.vhdx`
   - Size: 2GB, Format: VHDX, Fixed Size.
3. **Aktiveeri:** Paremklõps uuel kettal -> Initialize Disk (GPT).
4. **Loo partitsioon:** Paremklõps tühjal alal -> New Simple Volume -> Drive **E:**.

---

## 3. SAMM: Sisselogimiste analüüs (PowerShell)
Otsime, kes ja millal sisse logis (asendab domeenikontrolleri puudumist).

```powershell
# Otsib edukaid sisselogimisi (ID 4624) viimase 24 tunni jooksul
Get-EventLog -LogName Security -InstanceId 4624 -After (Get-Date).AddDays(-1) | 
Select-Object TimeGenerated, @{N='User';E={$_.ReplacementStrings[5]}}, @{N='Source_IP';E={$_.ReplacementStrings[18]}} | 
Format-Table -AutoSize
```

4. SAMM: Kahtlaste protsesside tuvastamine

Uuri, mis põhjustas "kahtlased aknad" ekraanil.
PowerShell

# Otsib protsesse, mis jooksevad Temp või AppData kaustadest
Get-Process | Select-Object Name, Id, Path, Description | 
Where-Object {$_.Path -like "*\Temp\*" -or $_.Path -like "*\AppData\Local\*"} | 
Format-Table -AutoSize

5. SAMM: Failide kogumine ja puhastus

Kopeeri leitud failid E: kettale enne nende eemaldamist.

    Kopeeri: Copy-Item -Path "C:\kahtlane\asukoht\fail.exe" -Destination "E:\"

    Eemalda oht: Remove-Item -Path "C:\kahtlane\asukoht\fail.exe" -Force

    Väljutamine: Disk Management -> Paremklõps Disk (vasakul ääres) -> Detach VHD.

6. SAMM: Failide haldus võrguta keskkonnas

Kui kopeerid skripte VM-i tekstina, kasuta PowerShellis:
PowerShell

    Set-ExecutionPolicy Bypass -Scope Process
# Nüüd saad käivitada oma .ps1 failid
    .\skripti_nimi.ps1

MÄRKUS: Kuna ligipääs DC-le puudub, on see Win10 masin sinu ainus tõendusmaterjali allikas. Kõik tegevused ja leitud IP-aadressid logi üles!


---

**Väike nipp:** Kui sa hakkad neid "kahtlaseid aknaid" uurima, siis vaata ka **Task Manageris** (Ctrl+Shift+Esc) vahekaarti **Startup**. Tihti peidavad ründajad sinna skripte, mis peale väljalogimist ja uuesti sisselogimist uuesti käivituvad.
