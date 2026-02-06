# FORENSIC REPORT: TRL-Win11-02 (Offline Activity Detected)
**Uurimise kuupäev:** 06.02.2026
**Uurija:** [Sinu Nimi]
**Intsidendi tüüp:** Andmete eksfiltratsioon ja autonoomne püsivus (Persistence)

---

## 1. Sündmuse anatoomia
Kasutaja märkas "vilkuvaid aknaid". Uurimise käigus tuvastati, et ründaja on loonud autonoomse süsteemi, mis kogub andmeid ka võrguühenduse puudumisel. Masin suleb end perioodiliselt, mis viitab "Watchdog" skriptile.

---

## 2. Kriitilised leiud (PowerShell Transkriptid)
Tuvastatud on 24+ transkripti faili. Failinime formaat: `PowerShell_transcript.TRL-WIN11-02.[ID].[Timestamp].txt`.
* **Viimane aktiivne tihend:** 2026-02-06 12:09:41
* **Tähendus:** Süsteem logib automaatselt kogu PowerShelli tegevust. Ründaja näeb ka uurija sisestatud käskusid.

---

## 3. Uurimise tööriistakast (Käsklused järgmiseks korraks)

Kui saad masina uuesti käima, tegutse selles järjekorras:

### SAMM 1: Tuvasta ründaja "Koju helistamise" aadress (C2)
Otsi transkriptidest ründaja serveri URL-i.
```powershell
Select-String -Path "$env:USERPROFILE\Documents\20251118\*.txt" -Pattern "aC2URL", "http"
```
SAMM 2: Leia "Pesa" (E: ketta algne asukoht)

Kuna andmeid kopeeriti E: kettale, peame leidma selle võrgutee.
```PowerShell

Select-String -Path "$env:USERPROFILE\Documents\20251118\*.txt" -Pattern "RemotePath", "net use"
```
SAMM 3: Tuvasta, mis skript masinat suleb (Persistence)

Otsi protsessi, mis käivitus failide tekkimise ajal (12:09:41).
```PowerShell

Get-Process | Where-Object { $_.StartTime -gt "2026-02-06 12:09:00" -and $_.StartTime -lt "2026-02-06 12:10:00" } | Select-Object Name, Id, StartTime, Path
```
SAMM 4: Kontrolli ajastatud ülesandeid (Scheduled Tasks)

See on tõenäoline koht, kus asub "Watchdog", mis masinat suleb.
```PowerShell

Get-ScheduledTask | Where-Object {$_.State -ne "Disabled"} | Get-ScheduledTaskInfo | Sort-Object LastRunTime -Descending | Select-Object TaskName, LastRunTime -First 10
```
SAMM 5: Päästa BitLockeri taastevõti

Otsi 48-kohalist numbrijada, enne kui ketas lukustub.
```PowerShell

Select-String -Path "$env:USERPROFILE\Documents\20251118\*.txt" -Pattern "\d{6}-\d{6}-\d{6}-\d{6}"
```
4. Tuvastatud ründeahel (Kill Chain)

    Reconnaissance: Süsteemiinfo kogumine KAPE ja Autoruns abil.

    Staging: Andmete kogumine E:\Capture\KAPE\.

    Exfiltration: Side C2 serveriga läbi MSXML2.XMLHTTP (VBScript).

    Persistence: PowerShell Transcriptioni ja Scheduled Taskide kasutamine kontrolli säilitamiseks.

    Anti-Forensics: Masina sunnitud sulgemine uurimise takistamiseks.

5. Järgmised sammud (Prioriteetne)

    Käivitada masin ja sisestada kohe käsk protsesside loetlemiseks (Samm 3).

    Tuvastada ründaja IP-aadress (Samm 1).

    Eemaldada kahtlased Scheduled Taskid.




### Minu nõuanne sulle:
Kuna masin suleb end, siis järgmine kord, kui sisse saad, **ära hakka faile lugema**, vaid pane esimese asjana käima **Samm 3** ja **Samm 4**. Meil on vaja teada, mis *protsess* on see "peremees", kes masinat käsutab.

Kui sa näed `Get-ScheduledTask` väljundis midagi, mille nimi on "Update", "SysCheck" või mõni suvaline tähtede jada, siis see ongi see, mis tuleb peatada käsklusega:
`Stop-Process -Id [ID]` või `Disable-ScheduledTask -TaskName "[Nimi]"`.
