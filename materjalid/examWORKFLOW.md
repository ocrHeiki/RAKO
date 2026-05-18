# 🚀 EKSAMI TÖÖVOOG & SPRIKKER — TEAM 10 (Taktikaline versioon)

See töövoog on optimeeritud nii, et esmalt jäädvustatakse puhta võrgu seisund ning seejärel rakendatakse automatiseeritud ja käsitsi forensikat, kahjustamata olemasolevaid ründetõendeid.

---

## 📅 ETTEVALMISTUSKORD (Tee täna oma Kali masinas)

Käivita oma Kali terminalis järgmised käsud, et tööriistad oleksid laboris kohe valmis:
```bash
sudo apt update
sudo apt install -y mc nmap zenmap-kbx net-tools iproute2

```
## 🏁 SAMM-SAMMULINE TÖÖVOOG LABORIS
### SAMM 1: Virtuaaltaristu Kaitse (Kloonimine)
 * **Tegevus:** Enne kui puutud ühtegi masinat või käivitad ühtegi skripti, tee vSphere keskkonnas kõigist itskteam10 masinatest **Kloon või Snapshot**.
 * **Miks?** See on forensiline esmaabi. Kui süsteem jookseb kokku või tulemüür lukustab SSH/RDP välja, saame sekundiga taastada algse seisukorra.
### SAMM 2: Võrgu Baasjoone Kaardistamine (Zenmap)
 * **Tegevus:** Käivita kohe oma Kali masinas Zenmap või käsurida ja pane võrk skaneerima:
   ```bash
   sudo nmap -sV -O 192.168.10.0/24
   
   ```
 * **Eesmärk:** Tuvastada ründaja poolt avatud pordid ja aktiivsed ühendused hetkel, kui te pole ise veel süsteemides muudatusi teinud. Jäta Zenmap/liiklusanalüüs taustale jooksma, et hiljem eraldada meeskonna enda tekitatud VALVUR-i liiklus ründaja omast.
### SAMM 3: VALVUR Masterskripti Rakendamine (E-ITS Audit)
Nüüd, mil võrgupilt on salvestatud, käivita automatiseeritud kontroll, et tuvastada E-ITS hälbed (meede CON.1.M2, SYS.1.3.M1 jne).
 * **Windows (DC1 / FileSRV1):**
   ```powershell
   python .\VALVUR_master.py --mode eits
   
   ```
 * **Linux (INTRAWEB1 / TicketingServer):**
   ```bash
   sudo python3 valvur_master.py --check-all
   
   ```
 * **Tulemus:** VALVUR genereerib raporti valede failiõiguste, maas olevate tulemüüride ja kahtlaste teenuste kohta, andes käsitööks täpsed vihjed.
### SAMM 4: Intsidentide Haldus (Ticketid)
 1. Registreeri VALVUR-i ja Zenmapi leitud hälbed koheselt piletisüsteemis (TicketingServer-itskteam10).
 2. Määratle intsidentide prioriteedid (nt aktiivne Reverse Shell = Kriitiline).
### SAMM 5: Linuxi Serveri Süvaanalüüs (INTRAWEB1)
Kasuta käsitööks õpetaja soovitatud käske, et ründaja isoleerida:
 1. **Kasutajad:** w ja who -a (Kes teeb reaalajas terminalis kahju?).
 2. **Võrk reaalajas:** sudo netstat -nputw (Leia ründaja ühenduse PID).
 3. **Pahavara asukoht:** sudo ls -l /proc/[PID]/exe (Kust fail jookseb?).
 4. **Püsivus:** sudo crontab -e ja ls -la /etc/cron.d/.
 5. **Logide lappamine:** sudo mc (Võrdle /var/log/nginx/ süsteemseid logisid ja /var/www/html/ rakenduse siseseid logisid, kuhu ründaja võis jälgi jätta).
 6. **Tulemüüri esmaabi (SSH elupäästja!):**
   ```bash
   sudo ufw allow from [Sinu_Kali_IP] to any port 22 proto tcp
   sudo ufw enable
   
   ```
### SAMM 6: Windowsi Masina Süvaanalüüs (DC1)
 1. **Võrk:** netstat -fano -> Tuvasta C2 ühendused ja nende PID-d.
 2. **Sessioonid:** compmgmt.msc -> Shared Folders -> Sessions.
 3. **Püsivus:** Autoruns64.exe (Kontrolli ajastatud toiminguid ja registrit).
 4. **Logi-analüüs:** Käivita VALVUR-i 11_turvafiltreering.py, et filtreerida välja rünnaku kellaaja kriitilised sündmused.
```

---

### 🗣️ Kuidas sa seda esitlusel komisjonile serveerid:

See loogika paneb komisjoni teid kuulama täieliku austusega. Kui jõuad **Slaid 3 (Võrguplaan)** ja **Slaid 5/6 (Masinate analüüs)** juurde, selgita seda täpselt nii:

> *"Meie meeskonna metodoloogia laboris oli rangelt forensiline. **Esimene samm oli keskkonna kloonimine vSphere'is**, et tagada andmete terviklikkus ja turvaline taganemistee. 
> 
> **Teise sammuna käivitasime koheselt Zenmapi**, et fikseerida võrgu baasjoon reaalajas, enne kui me ise süsteeme muudame. See oli kriitiline, sest kui me **kolmanda sammuna rakendasime oma VALVUR masterskripti**, tekitas see paratamatult uut võrguliiklust. Tänu varasemale skaneerimisele ja taustal jooksvale seirele suutsime me VALVUR-i enda legitiimse liikluse ründaja pahatahtlikust C2 liiklusest täielikult eraldada ja filtreerida."*

See on tipptasemel küberkaitse analüütiku töövoog. Te olete homseks laboriks ideaalselt planeeritud ja valmis!

```
