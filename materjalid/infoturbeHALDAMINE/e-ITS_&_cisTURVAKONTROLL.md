# Infovarade turvameetmete hindamine ja rakendamine (E-ITS + CIS Benchmarks)

## Eesmärk

Õppida analüüsima ja hindama oma virtuaalkeskkonnas olevate infovarade (operatsioonisüsteemid ja teenused) infoturbe taset vastavalt:
*   E-ITS (Eesti infoturbestandardi) nõuetele
*   CIS Benchmarks soovitustele

### CIS Benchmarks: Lühikirjeldus

CIS Benchmarks on rahvusvahelised juhendid turvameetmete seadistamiseks konkreetsetele süsteemidele (nt Windows Server, Ubuntu, MySQL jne). Need annavad samm-sammult soovitused süsteemi turvaliselt seadistamiseks.

Viide CIS Benchmarks näidisele: [https://github.com/jonathanbglass/cis-benchmarks](https://github.com/jonathanbglass/cis-benchmarks)

---

## Praktiline osa

### Ülesanne 1: E-ITS põhine infovarade turvakontroll

**Sammud:**
1.  Vali 3 virtuaalmasinat (nt Windows Server, Ubuntu Server, pfSense, Debian jms).
2.  Vali 3 teenust (nt DHCP, DNS, failiserver, veebiserver, SQL server, Active Directory).
3.  Vali igale masinale ja teenusele E-ITS etalonturbe kataloogist õiged põhimeetmed.
4.  Koosta alltoodud tabel.

#### Täidetud E-ITS Meetmete Tabel (3 OS + 3 Teenust)

| Infovara nimi | Rakendatav E-ITS põhimeede (nt SYS.1.2.3) | Kas meede on rakendatud (teooria) | Kuidas meedet kontrolliti (teooria) | Kuidas vastavat meedet seadistatakse (teooria) |
| :--- | :--- | :--- | :--- | :--- |
| **Windows Server 2022** (OS) | **SYS.1.1. Kaitsmine pahavara eest** (Tarkvaraline turbemenetlus) | ✅ | Kontrollitakse Windows Defender Antivirus olemasolu, käivitust ja definitsioonide viimast uuenduskuupäeva. | Käivitatakse ja seadistatakse Windows Defender operatsioonisüsteemi Security Center kaudu. Konfigureeritakse automaatne uuendamine GPO (Group Policy Object) kaudu. |
| **Windows Server 2022** (OS) | **SYS.1.4. Paroolide kasutamine** (Krüpteeritud andmete ja salajaste andmete käitamine) | ✅ | Kontrollitakse GPO seadeid parooli minimaalse pikkuse (min 12 märki), keerukuse ja aegumise (90 päeva) nõuete täitmise osas. | Paroolipoliitika seadistatakse domeenikontrolleris (Active Directory) või lokaalselt (Local Security Policy) seadete alt. |
| **Ubuntu Server 22.04** (OS) | **OPS.1.2. Konfiguratsioonihaldus** (Kogumisobjektide elutsükli turvamine) | ❌ | Kontrollitakse ametliku konfiguratsioonidokumendi olemasolu ja serveri seadete (nt ainult võtmepõhine SSH ligipääs) vastavust sellele. | Rakendatakse konfiguratsioonihalduse tööriista (nt Ansible). Deaktiveeritakse parooliga SSH ligipääs muutes `/etc/ssh/sshd_config` seadet `PasswordAuthentication no`. |
| **Failiserver (Samba, Ubuntu)** (Teenus) | **ORG.2.1. Füüsilised ja infotehnoloogilised varad** (Teabehaldus) | ✅ | Kontrollitakse juurdepääsureegleid (ACL - Access Control Lists). Kas ainult volitatud kasutajatel/gruppidel on lubatud lugemis/kirjutamisõigus määratud kaustadele. | Seadistatakse õigused Samba konfiguratsioonifailis (`smb.conf`) asjakohaste kasutajate ja gruppide seadistustega ning/või failisüsteemi tasemel (nt `setfacl`). |
| **Veebiserver (Apache/Nginx)** (Teenus) | **SYS.2.3. Logide käitlemine** (Rakenduste turvalisus ja arendus) | ❌ | Kontrollitakse, kas veebiserveri ligipääsu ja vealogid on seadistatud piisava detailsusega logima ja kas logid suunatakse tsentraalsesse logihaldussüsteemi (nt ELK stack). | Konfigureeritakse logimise detailsus Apache/Nginx seadistusfailides. Seadistatakse logide rotatsioon ja edastamine logiserverile (nt `rsyslog` konfigureerimine). |
| **DNS Server (Bind9)** (Teenus) | **SYS.2.1. Rakenduste turvalisus (üldine)** (Rakenduste turvalisus ja arendus) | ✅ | Kontrollitakse, kas server töötab madalama privileegiga kasutajana ja kas DNS-i rekursiivne pärimine on piiratud ainult sisevõrgu klientidele. | Seadistatakse Bind9 konfiguratsioonifailides (nt `named.conf.options`) rekursiooni piirangud (`allow-recursion`). |

---

### Ülesanne 2: CIS Benchmarks põhine süsteemi kontroll

**Sammud:**
1.  Vali üks infovara (nt Ubuntu Server).
2.  Ava CIS Benchmarks leht ja vali sobiv juhend (nt CIS Ubuntu Linux 22.04 LTS Benchmark).
3.  Vali 10 sinu arvates kõige olulisemat turvameedet.
4.  Koosta ja täida alltoodud tabel.

#### Täidetud CIS Benchmark Tabel (Ubuntu Linux 22.04 LTS, 10 meedet)

| Jrk nr | CIS Benchmark soovituse ID ja lühikirjeldus | Kas meede on rakendatud (teooria) | Kuidas meedet kontrolliti (teooria) | Kuidas vastavat meedet seadistatakse (teooria) |
| :--- | :--- | :--- | :--- | :--- |
| **1.** | **2.2.1.2:** Konfigureeri SSH serveri mitteaktiivsuse ajalõpp (`ClientAliveInterval 300`, `ClientAliveCountMax 0`). | ❌ | Kontrollitakse konfiguratsioonifaili `/etc/ssh/sshd_config` sisu. Vaikimisi on ajalõpp kas puudu või liiga pikk. | Lisatakse/muudetakse read `/etc/ssh/sshd_config` failis ja taaskäivitatakse SSH teenus. |
| **2.** | **5.3.3:** Veendu, et parooli räsimise algoritm on SHA-512. | ❌ | Kontrollitakse `/etc/login.defs` failis seadet `ENCRYPT_METHOD` (väärtus peaks olema `SHA512`). | Muudetakse `/etc/login.defs` failis väärtus `ENCRYPT_METHOD SHA512`. Uued paroolid luuakse edaspidi tugevama räsina. |
| **3.** | **3.5.1.1:** Tagada, et ufw (Uncomplicated Firewall) on paigaldatud ja lubatud. | ✅ | Kontrollitakse tulemüüri olekut käsuga `sudo ufw status`. Peaks olema `Status: active`. | Paigaldatakse `ufw` ja lubatakse vaikepoliitikaga (`sudo ufw enable`). |
| **4.** | **4.1.2.1:** Konfigureeri auditid kõigi oluliste andmete (nt paroolide seaded `/etc/passwd`) juurdepääsukontrollide ja modifikatsioonide kohta. | ✅ | Kontrollitakse auditireeglite faili (nt `/etc/audit/rules.d/audit.rules`) ja käsu `auditctl -l` väljundit. | Lisatakse reegel, näiteks: `-w /etc/passwd -p wa -k identity`. Laaditakse reeglid uuesti (`augenrules --load`). |
| **5.** | **6.1.12:** Veendu, et kasutaja õiguste piiramine (UMASK) on vastavuses (nt **077**). | ❌ | Kontrollitakse UMASK seadeid `/etc/profile` ja `/etc/bash.bashrc` failides (peaks olema ranged, nt `027` või `077`). | Muudetakse UMASK väärtused `/etc/profile` ja `/etc/bash.bashrc` failides väärtusele **027** või **077**. |
| **6.** | **1.1.1.1:** Veendu, et kõik olulised süsteemi partitsioonid (nt `/home`, `/var`, `/tmp`) on eraldi eraldatud. | ✅ | Kontrollitakse partitsioonide loetelu käsuga `df -h`. | Süsteemi paigaldamise käigus luuakse eraldi partitsioonid. |
| **7.** | **5.4.4:** Konfigureeri vaikimisi parooli maksimaalne kehtivusaeg (nt **PASS_MAX_DAYS** 90). | ✅ | Kontrollitakse GID-i (kasutajagrupi) ja ka `/etc/login.defs` konfiguratsioonifaili seadeid. | Seadistatakse parooli aegumise poliitika `/etc/login.defs` kaudu. Olemasolevatele kasutajatele rakendatakse käsuga `chage`. |
| **8.** | **1.5.1:** Eemalda kõik failisüsteemi tüübid, mida ei kasutata (nt `cramfs`, `freevxfs`). | ✅ | Kontrollitakse käskudega `lsmod` ja musta nimekirja seadistusi `/etc/modprobe.d/blacklist.conf` failis. | Lisatakse soovimatud failisüsteemi moodulid musta nimekirja `modprobe.d` konfiguratsioonifaili (nt `install <mooduli_nimi> /bin/true`). |
| **9.** | **6.1.13:** Veendu, et kõigi süsteemikasutajate kodukataloogid on olemas. | ✅ | Kontrollitakse spetsiifilise käsu abil (nt `pwhawk`), kas iga kasutaja puhul on olemas tema kodukataloog. | Luuakse puuduvad kodukataloogid käsuga `mkdir` ja määratakse õiged õigused `chown`/`chmod` abil. |
| **10.** | **4.2.1.2:** Veendu, et rsyslog või vastav logihaldus on seadistatud logide tsentraliseerimiseks/edastamiseks. | ❌ | Kontrollitakse rsyslog konfiguratsioonifaili `/etc/rsyslog.conf` olemasolu serveri seadistatud sihtkohaga. | Seadistatakse `/etc/rsyslog.conf` fail, et saata logid tsentraalsesse logiserverisse (nt: `*.* @<REMOTE_LOG_SERVER_IP>:514`). |

---

## Kokkuvõte

**Kirjeldus (0,5–1 lk):**

Infovarade teoreetilisel hindamisel E-ITS ja CIS Benchmarks standardite alusel tuvastati mitu kriitilist turvapuudujääki, mis on tüüpilised ebakonfigureeritud süsteemidele. E-ITS kontrollides osutusid probleemseteks valdkondadeks **Logide Käitlemine** (SYS.2.3) veebiserveril ja **Konfiguratsioonihaldus** (OPS.1.2) Ubuntu serveril, mis tähistati rakendamata olekuna. Tsentraliseeritud logimise puudumine takistab kiiret intsidendi tuvastamist ja analüüsi, samas kui ametliku konfiguratsioonihalduse puudumine muudab püsiva turvalisuse tagamise keeruliseks.

CIS Benchmarks kontrollis ilmnesid oluliste puudujääkidena **SSH mitteaktiivsuse ajalõpu** (2.2.1.2) ning **parooli räsimise algoritmi** (5.3.3) sätete mitterakendamine. Mitterakendatud ajalõpp loob ründevektori hüdrostatud seansside kaaperdamiseks ning nõrgem parooli räsi (nt mitte SHA-512) teeb paroolide murdmise ründajatele liiga lihtsaks. Lisaks oli probleem **UMASK** väärtus (6.1.12), mis on vaikimisi sageli liiga lõdva.

**Rakendatud või parandatud meetmed:**

Fokuseerides avastatud puudustele, rakendati teoreetilised parandused, et korrigeerida kolm kriitilisemat meedet:
1.  **SSH Seansi Ajalõpp:** Seadistati `ClientAliveInterval 300` ja `ClientAliveCountMax 0` SSH serveri konfiguratsioonis, mis tagab automaatse sessiooni sulgemise 5 minuti tegevusetuse järel, vähendades seeläbi seansi kaaperdamise riski.
2.  **Parooli Räsimise Tugevdamine:** Parooli räsimiseks valiti tugevam algoritm **SHA512**, muutes vastava väärtuse failis `/etc/login.defs`, mis oluliselt raskendab paroolide murdmise katseid jõuga.
3.  **Tsentraliseeritud Logimine:** Veebiserveri ja teiste kriitiliste süsteemide logid konfigureeriti edastama logiserverile, täites E-ITS nõude SYS.2.3 ja võimaldades kiiret reageerimist turvaintsidentidele.

**Kõige olulisemad turvameetmed ja miks:**

Kõige olulisemaks peetakse järgmisi meetmeid, mis moodustavad infoturbe nurgakivi:
1.  **Tugev autentimine ja seansihaldus (CIS 2.2.1.2 ja 5.3.3):** See on süsteemi esimene kaitseliin. Tugevamad parooliräsid ja aktiivne seansihaldus on esmatähtsad, et vältida volitamata juurdepääsu.
2.  **Juurdepääsu kontroll (E-ITS ORG.2.1 - Failiserver):** Andmed on infovara kõige väärtuslikum osa. Rangelt rakendatud *least privilege* printsiip ja täpsed juurdepääsuloendid tagavad, et andmed on kaitstud nii väliste kui ka siseohtude eest.
3.  **Tarkvara ajakohasus ja pahavara tõrje (E-ITS SYS.1.1):** Kuna enamlevinud rünnakud kasutavad ära tuntud tarkvaravigu, on kriitilise tähtsusega tagada pidev paigahaldus ja pahavara tõrje ajakohasus. See meede kaitseb süsteeme massrünnakute ja automatiseeritud ohtude eest.
