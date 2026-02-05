# Windows Event ID Spikker: Intsidendihaldus (IR)

See dokument koondab kriitilised logide ID-d, mida jälgida Pille Porgandi ja sarnaste intsidentide uurimisel.

---

## 1. SECURITY LOG (Sisselogimised ja süsteem)
*Asukoht: Windows Logs -> Security*

### Sisselogimised (Logon Events)
| Event ID | Tegevus | Selgitus |
| :--- | :--- | :--- |
| **4624** | **Edukalt sisse logitud** | Kontrolli **Logon Type**. Tüüp 2 = kohalik, Tüüp 3 = võrk, Tüüp 10 = RDP. |
| **4625** | **Ebaõnnestunud sisselogimine** | Vale parool või kasutajanimi. Viitab brute-force ründele. |
| **4648** | **Explicit Credentials** | Kasutati `runas` käsku teise kasutaja õigustega. |
| **4634 / 4647** | **Väljalogimine** | Märgib sessiooni lõppu. |

### Protsessid ja Manipuleerimine
| Event ID | Tegevus | Selgitus |
| :--- | :--- | :--- |
| **4688** | **Uus protsess loodi** | Näitab, mis programm käivitus. Kontrolli "Process Command Line"! |
| **4698** | **Scheduled Task loodi** | Ründaja seadistas pahavara automaatse käivituse (persistence). |
| **1102** | **Audit Log puhastati** | **KRIITILINE!** Keegi üritas oma jälgi peita ja kustutas logid. |
| **4720** | **Kasutaja loodi** | Süsteemi tekitati uus, ründajale kuuluv konto. |
| **4732** | **Lisati gruppi** | Kasutajale anti nt Administraatori õigused. |

---

## 2. POWERSHELL LOG (Operational)
*Asukoht: Applications and Services -> Microsoft -> Windows -> PowerShell -> Operational*

| Event ID | Tegevus | Miks see on oluline? |
| :--- | :--- | :--- |
| **4104** | **Script Block Logging** | **Kõige olulisem!** Salvestab skripti sisu (isegi kui see on peidetud/krüpteeritud). |
| **4103** | **Module Logging** | Näitab kasutatud PowerShelli mooduleid ja parameetreid. |
| **400 / 403** | **Engine Start/Stop** | Näitab PowerShelli sessiooni algust ja lõppu. |

### Kahtlased märksõnad PowerShelli logides (ID 4104):
* `EncodedCommand` või `-enc` (Peidetud kood)
* `IEX` / `Invoke-Expression` (Teksti käivitamine koodina)
* `DownloadString` / `WebClient` (Asjade allalaadimine internetist)
* `WindowStyle Hidden` (Kasutaja eest akna peitmine)
* `Bypass` (Turvapoliitika eiramine)

---

## 3. KUIDAS FILTREERIDA (PowerShell skript)
Kui soovid Win10 masinas kiiresti olulised ID-d kätte saada ilma hiirega klõpsimata:

```powershell
# Filtreeri Security logist olulisemad ID-d
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624, 4625, 4688, 1102} -MaxEvents 50 | Select-Object TimeCreated, ID, Message | Out-GridView

# Otsi PowerShelli logist kahtlast Script Block sisu
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-PowerShell/Operational'; ID=4104} | Select-Object TimeCreated, Message | Format-List
