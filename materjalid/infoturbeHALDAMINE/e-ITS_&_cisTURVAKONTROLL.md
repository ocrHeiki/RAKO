# Infovarade turvameetmete hindamine ja rakendamine (E-ITS + CIS Benchmarks)

## Eesmärk

Analüüsida ja hinnata virtuaalkeskkonnas olevate infovarade (operatsioonisüsteemid ja teenused) infoturbe taset vastavalt:

1.  E-ITS (Eesti infoturbestandardi) nõuetele.
2.  CIS Benchmarks soovitustele.

Lisaks traditsioonilistele serverioperatsioonisüsteemidele lisatakse hindamisel ka **Kali Linux** ja **Parrot OS**, mida soovitavad kasutamiseks mitmed infoturbe õpikeskkonnad (Kali: Offensive Security; Parrot: HackTheBox). Kuna need süsteemid sisaldavad ründetööriistu, on nende **kõvendamine (hardening)** kriitiline – vastasel juhul võib turvatööriistadest endast saada ründevektor.

## CIS Benchmarks: Lühikirjeldus

CIS Benchmarks on rahvusvahelised turvastandardid, mis sisaldavad samm-sammulisi turvaseadistusi konkreetsetele süsteemidele (nt Ubuntu Server, Windows Server, MySQL, Docker jms).

**Viide näidistele:**
[https://github.com/jonathanbglass/cis-benchmarks](https://github.com/jonathanbglass/cis-benchmarks)

---

## Praktiline osa

### Ülesanne 1: E-ITS põhine infovarade turvakontroll

**Sammud**
1. Vali 3–5 operatsioonisüsteemi (Windows Server, Ubuntu, Debian, pfSense, Kali Linux, Parrot OS).
2. Vali 3 teenust (nt DNS, DHCP, failiserver, veebiserver, Active Directory).
3. Vali sobivad meetmed E-ITS etalonturbe kataloogist.
4. Täida tabel.

#### Täidetud E-ITS Meetmete Tabel (OS-id + teenused, sh Kali & Parrot)

| Infovara nimi | Rakendatav E-ITS põhimeede | Kas meede on rakendatud | Kuidas meedet kontrolliti | Kuidas meedet seadistatakse |
| :--- | :--- | :--- | :--- | :--- |
| **Windows Server 2022 (OS)** | SYS.1.1 – Kaitsmine pahavara eest | ✅ | Kontrolliti Windows Defender Antivirus olekut ja definitsioonide kuupäeva. | Windows Defender seadistamine Security Centeri kaudu; automaatuuendused GPO abil. |
| **Windows Server 2022 (OS)** | SYS.1.4 – Paroolide kasutamine | ✅ | Kontrolliti GPO poliitikaid: minimaalse pikkuse, keerukuse ja aegumise nõuded. | Seadistamine Active Directory või Local Security Policy kaudu. |
| **Ubuntu Server 22.04 (OS)** | OPS.1.2 – Konfiguratsioonihaldus | ❌ | Kontrolliti SSH konfiguratsiooni (kas paroolisisselogimine on keelatud). | Ansible vm konfiguratsioonihaldus; `PasswordAuthentication no` seadistus. |
| **Failiserver (Samba, Ubuntu)** | AVA.3.2 – Juurdepääsuõiguste haldus | ✅ | Kontrolliti ACL-e ja gruppide õiguseid jagatud kaustadele. | Õigused Samba `smb.conf` failis ja failisüsteemi tasemel (`setfacl`). |
| **Veebiserver (Apache/Nginx)** | SYS.2.3 – Logide käitlemine | ❌ | Kontrolliti logide detailset taset ja edasi saatmist logiserverisse. | Logimise seadistamine Apache/Nginx configis, `rsyslog` kaudu edastamine. |
| **DNS Server (Bind9)** | SYS.2.1 – Rakenduste turvalisus | ✅ | Kontrolliti kasutajaõiguseid ja rekursiooni piiramist siseklientidele. | `named.conf.options` – `allow-recursion` seadistus. |
| **Kali Linux (OS)** | SYS.1.2 – Süsteemi kõvendamine | ❌ | Kontrolliti, kas mittevajalikud teenused ja tööriistad on keelatud või eemaldatud. | Tulemüüri aktiveerimine (`ufw`), mittevajalike pakettide eemaldamine, SSH piiramine. |
| **Parrot OS Security Edition (OS)** | SYS.1.2 – Süsteemi kõvendamine | ❌ | Kontrolliti süsteemi kõvendamise seadeid ja vaikimisi aktiivseid turvateenuseid. | Parrot Security Hardening Tools, tulemüüri seadistamine, mittevajalike moodulite eemaldamine. |

---

### Ülesanne 2: CIS Benchmarks põhine süsteemi kontroll

#### Täidetud CIS Benchmark Tabel (Ubuntu Linux 22.04 LTS — 10 meedet)

| # | CIS Benchmark meede | Rakendatud | Kuidas kontrolliti | Kuidas seadistatakse |
| :--- | :--- | :--- | :--- | :--- |
| **1** | 2.2.1.2 — SSH mitteaktiivsuse ajalõpp | ❌ | Kontrolliti `/etc/ssh/sshd_config`. | Lisa `ClientAliveInterval 300` ja `ClientAliveCountMax 0`; **taaskäivita SSH**: `systemctl restart sshd`. |
| **2** | 5.3.3 — Parooli räsimise algoritm SHA-512 | ❌ | Kontrolliti `ENCRYPT_METHOD` väärtust. | Muuda `ENCRYPT_METHOD SHA512`; **kehtib uutele paroolidele**. |
| **3** | 3.5.1.1 — ufw lubatud | ✅ | Kontrolliti `ufw status`. | `sudo ufw enable`. |
| **4** | 4.1.2.1 — Auditireeglid kriitiliste failide jaoks | ✅ | Vaadati `auditctl -l` väljundit. | Lisa reegel; `augenrules --load`. |
| **5** | 6.1.12 — UMASK rangemaks | ❌ | Kontrolliti `/etc/profile`. | Sea `UMASK` väärtuseks `027` või `077`. |
| **6** | 1.1.1.1 — Partitsioonide eraldamine | ✅ | Kontrolliti `df -h`. | Teostatakse paigalduse käigus (nt `/var` ja `/tmp` eraldi partitsioonidel). |
| **7** | 5.4.4 — Parooli maksimaalne kehtivusaeg | ✅ | Kontrolliti `/etc/login.defs`. | Seadista `PASS_MAX_DAYS`; vajadusel `chage`. |
| **8** | 1.5.1 — Mittevajalike failisüsteemide keelamine | ✅ | Kontrolliti `lsmod` ja blacklisti. | Lisa moodulid `blacklist.conf` faili. |
| **9** | 6.1.13 — Kõigil kasutajatel kodukataloog olemas | ✅ | Kontrolliti skriptiga. | Loo puuduvad kataloogid ja õigused. |
| **10** | 4.2.1.2 — rsyslog tsentraliseerimine | ❌ | Kontrolliti `/etc/rsyslog.conf`. | Lisa logiserver; **taaskäivita rsyslog**: `systemctl restart rsyslog`. |

---

## Kokkuvõte

Analüüs E-ITS ja CIS Benchmarks standardite alusel tuvastas mitmeid olulisi puudusi nii organisatsioonilisel kui tehnilisel tasandil, näidates kahe standardi sünergiat turvaolukorra hindamisel.

**E-ITS tulemused**
Tõid esile organisatsioonipõhised riskid, sealhulgas:
*   logide käitlemise puudulikkus (SYS.2.3),
*   konfiguratsioonihalduse puudumine (OPS.1.2),
*   juurdepääsuõiguste ebapiisav haldus (AVA.3.2).
*   Kali Linux ja Parrot OS puhul ilmnes vajadus tugeva süsteemi kõvendamise järele, et vältida võimalust, et turvatööriistad ise muutuvad ründevahenditeks.

**CIS Benchmarks tulemused**
Tuvastasid tehnilised juurprobleemid, mis vastavad E-ITS organisatsioonilistele puudustele, näiteks:
*   SSH seansside kontrolli puudumine (2.2.1.2).
*   nõrk parooliräsi algoritm (5.3.3).
*   UMASK liiga leebe (6.1.12).
*   logide tsentraliseerimata olek (4.2.1.2).

Kuigi E-ITS ja CIS lähtuvad erinevast fookusest (organisatsiooniline vs tehniline), jõudsid mõlemad sama järelduseni: süsteemide turvaseisund nõuab tugevdamist.
