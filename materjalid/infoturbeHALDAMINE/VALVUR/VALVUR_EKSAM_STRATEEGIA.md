# VALVUR - Intsidendi Analüüsi ja Reageerimise Strateegia (Eksam 2026)

See juhend kirjeldab VALVUR-i (HeRe) moodulite rakendamist spetsiifilistel infrastruktuuri masinatel, et tuvastada kompromiteerimist ja rekonstrueerida ründaja tegevust.

---

## 1. itsh-eksam-dc01 (Domain Controller)
**Roll:** Infrastruktuuri süda. Ründaja peamine eesmärk (Domain Admin õigused).

### Tegevuskava (Actionable Steps):
1.  **Samm 1 (Identify):** Käivita `00_terviklus_kontroll.py`, et räsida süsteemilogid (`Security.evtx`).
2.  **Samm 2 (Detect):** Käivita `01_konverteering_evtx_csv.py --live`, et saada kätte reaalajas logid.
3.  **Samm 3 (Detect):** Käivita `02_turvafiltreering.py`. DC puhul otsime eriti GPO muudatusi ja uute kasutajate loomist.
4.  **Samm 4 (Audit):** Käivita `11_kasutajate_nimekiri.py`, et tuvastada ootamatuid kontosid privilegeeritud gruppides.

### Kriitilised Event ID-d DC analüüsis:
-   **4720:** Kasutajakonto loomine (Võimalik ründaja püsivus).
-   **4732 / 4728:** Kasutaja lisamine "Administrators" või "Domain Admins" gruppi.
-   **4624 (Logon Type 3/10):** Võrgu kaudu sisselogimine või RDP (Lateral Movement).
-   **4704:** Kasutajaõiguste muudatused (nt "Log on as a service").

**NIST Kategooria:** *Detect (DE.AE-02)* - Logide analüüs AD kompromiteerimise tuvastamiseks.

---

## 2. itsh-eksam-ruuter (Gateway)
**Roll:** Liikluse sõlmpunkt. Siit liigub ründaja sisevõrku või saadab andmeid välja (Exfiltration).

### Tegevuskava (Actionable Steps):
1.  **Samm 1 (Detect):** Käivita `10_vorgu_skaneerimine.py`. Kasuta Nmap-i, et tuvastada ruuteris avatud porte, mida seal olema ei peaks (nt 4444, 31337).
2.  **Samm 2 (Respond):** Kasuta `09_threat_intel.py` (või vaata logisid manuaalselt), et kontrollida ruuterit läbinud kahtlasi välis-IP-sid.
3.  **Samm 3 (Detect):** Kui ruuter on Linuxi-põhine, käivita `14_linux_syvaanaluus.py`, et kontrollida SSH sisselogimisi välisvõrgust.

**NIST Kategooria:** *Identify (ID.AM-01)* - Võrgu varade ja avatud teenuste kaardistamine.

---

## 3. itsh-eksam-fileserver (Data Assets)
**Roll:** Andmete asukoht. Peamine sihtmärk lunavarale (Ransomware) või andmevargusele.

### Tegevuskava (Actionable Steps):
1.  **Samm 1 (Detect):** Käivita `06_kahtlased_failid.py`. Otsime massiliselt loodud ebaharilikke laiendeid (.crypt, .locky) või skripte ajutistes kaustades.
2.  **Samm 2 (Protect):** Käivita `07_turvaaudit.py`. Kontrolli kriitiliselt **Volume Shadow Copies (vssadmin)** olekut. Kui need on kustutatud, on tegu lunavaraga.
3.  **Samm 3 (Recover):** Kasuta `13_koond_ajajoon.py`, et näha, millal algas massiline failide muutmine.

**NIST Kategooria:** *Protect (PR.PT-01)* - Andmete tervikluse ja varukoopiate kaitse audit.

---

## 4. itsh-eksam-kali (Attacker machine)
**Roll:** Ründaja tööriist. Kui saame siia ligipääsu (nt uurimise käigus), peame leidma ründe alguspunkti.

### Tegevuskava (Actionable Steps):
1.  **Samm 1 (Detect):** Käivita `06_kahtlased_failid.py`. Linuxis otsime peidetud faile (`/dev/shm`) ja `.bash_history` sisu.
2.  **Samm 2 (Detect):** Käivita `14_linux_syvaanaluus.py`. Kontrolli `auth.log` auke (Log Tampering) – kui ründaja on oma jälgi kustutanud, jääb logisse ajaline pragu.
3.  **Samm 3 (Identify):** Käivita `11_kasutajate_nimekiri.py`, et leida UID 0 kasutajaid, kes pole "root".

**NIST Kategooria:** *Respond (RS.AN-01)* - Ründaja tegevuse rekonstrueerimine ja analüüs.

---

## 5. Kliendid (client01-03)
**Roll:** Ohvrid. Siit algab rünne (Phishing/Exploit) ja siit liigutakse edasi DC poole.

### Tegevuskava (Actionable Steps):
1.  **Samm 1 (Detect):** Käivita `04_powershell_dekodeerimine.py`. Kliendi masinates on tihti esimeseks sümptomiks obfuskeeritud PowerShell skriptid (Base64/XOR).
2.  **Samm 2 (Detect):** Käivita `13_koond_ajajoon.py` (Unified Timeline).
    -   Võrdle kellaaegu: Kas klient01 sisselogimine ebaõnnestus ja 2 minutit hiljem logiti sisse klient02-te samalt IP-lt? See on **Lateral Movement**.
3.  **Samm 3 (Identify):** Kasuta `12_malu_analuus.py`, et tuvastada mälus peituvat pahavara, mis ei salvestu kettale.

**NIST Kategooria:** *Detect (DE.CM-01)* - Pidev seire ja ebatavalise liikumise tuvastamine sisevõrgus.

---

### Eksami MOTO: 
*"Analüüs teostatud süsteemi kloonil. Terviklus tagatud SHA-256 räsiga (NIST ID.SC-01). VALVUR tuvastab, HeRe analüüsib."*
