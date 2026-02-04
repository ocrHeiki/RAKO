# Intsidendi logianalüüsi skriptid

See dokument kirjeldab Pythoni skripte, mis on loodud Windowsi sündmuselogide (`.evtx`) analüüsimiseks küberintsidentide lahendamisel. Skriptid aitavad automatiseerida logifailide teisendamist loetavaks tekstivorminguks ja oluliste kahtlaste tegevuste tuvastamist logidest.

**Märkus kronoloogia kohta:** Välja võetud logikirjed sisaldavad täpseid kuupäevi ja kellaaegu (kuni millisekunditeni). See võimaldab sündmusi kronoloogiliselt järjestada, mis on kohtuekspertiisi analüüsi ja auditeerimise jaoks ülioluline.

## Ülesande kirjeldus ja algne teave

**Ülesanne:**
*   Kasutaja Pille Porgand märkas 16.11 päeval, et arvutiga toimub midagi kahtlast. Töö tegemise ajal logiti ta järsku masinast välja. Hiljem uuesti sisse logides avanesid ekraanil korraks kahtlased aknad, mida ta varem polnud märganud.
*   IR kasutaja: Kasutaja / parool: Parool123456@

**Algselt teadaolev info:**
*   Logid:
    *   `TRL-DC01` - Server 2019 domeenikontroller
    *   `TRL-INFRA01` - Server 2016 rakendusserver
    *   `TRL-WIN10-01` - Windows 10 tööjaam

## Edasine strateegia

Enne virtuaalmasinatele otseselt juurdepääsu loomist on meie esmane samm kaardistada olemasolev teave logifailidest. See aitab tuvastada potentsiaalseid ohuvektoreid ja sündmuste kronoloogiat, et suunata edasist uurimistööd ja vähendada riske otse süsteemides tegutsedes.

## Paigaldus

Enne skriptide kasutamist peate paigaldama vajalikud Pythoni moodulid ja tagama `evtxexport` tööriista olemasolu.

### Pythoni moodulid
Kõigi skriptide käivitamiseks on vaja `re` ja `os` mooduleid, mis on Pythoni standardraamatukogu osad ja ei vaja eraldi paigaldust. Lisaks on vaja `subprocess` moodulit `evtxexport` tööriista käivitamiseks.

### `evtxexport` tööriist
Skript `extract_evtx_to_text.py` kasutab `.evtx` failide teisendamiseks `evtxexport` tööriista. Veenduge, et see tööriist on teie süsteemi paigaldatud ja kättesaadav (PATH-is).

**Debian/Ubuntu-põhistes süsteemides:**
```bash
sudo apt install libevtx-utils
```

## Skriptide kirjeldus ja kasutus

Analüüsi protsess koosneb mitmest etapist, mida iga skript toetab.

### 1. `extract_evtx_to_text.py`
- **Kirjeldus:** See skript teisendab binaarsed Windowsi sündmuselogide `.evtx` failid loetavaks tekstivorminguks, kasutades `evtxexport` tööriista. See on esimene samm enne logifailide analüüsimist.
- **Kasutus:**
    ```bash
    python extract_evtx_to_text.py <sisend_evtx_fail> <väljund_teksti_fail>
    ```
    - `<sisend_evtx_fail>`: Tee `.evtx` failini, mida soovite teisendada (nt `TRL-INFRA01/winevt/logs/Security.evtx`).
    - `<väljund_teksti_fail>`: Tee ja failinimi, kuhu teisendatud tekstivormingus logi salvestatakse (nt `infra01_security.txt`).

### 2. `analyze_infra01_security_logs.py`
- **Kirjeldus:** Analüüsib rakendusserveri `TRL-INFRA01` turvalogi (tekstivormingus) intsidendi kuupäeval (16. november 2025). Skript otsib ebaõnnestunud sisselogimiskatseid (Event ID 4625), edukaid sisselogimisi (Event ID 4624) ja kahtlasi protsesse (Nmap, Chrome'i käivitamine), mis olid seotud brute-force rünnaku perioodiga.
- **Kasutus:**
    ```bash
    python analyze_infra01_security_logs.py <sisend_teksti_fail> <väljund_leidude_fail> [intsidendi_kuupäev]
    ```
    - `<sisend_teksti_fail>`: Teisendatud turvalogi tekstifail (nt `infra01_security.txt`).
    - `<väljund_leidude_fail>`: Failinimi, kuhu analüüsi leiud salvestatakse (nt `infra01_security_findings.txt`).
    - `[intsidendi_kuupäev]`: Valikuline. Intsidendi kuupäev formaadis "Nov 16, 2025". Vaikimisi "Nov 16, 2025".

### 3. `analyze_earlier_dc_logs.py`
- **Kirjeldus:** Analüüsib DC turvalogi varasema perioodi kohta (nt 16. oktoober 2025 kuni 15. november 2025), otsides kahtlast tegevust, mis on seotud teatud kasutajate või sündmuse ID-dega.
- **Kasutus:**
    ```bash
    python analyze_earlier_dc_logs.py <sisend_teksti_fail> <väljund_leidude_fail> <alguskuupäev_format_MMM_DD_YYYY> <lõppkuupäev_format_MMM_DD_YYYY>
    ```
    - `<sisend_teksti_fail>`: Teisendatud DC turvalogi tekstifail (nt `dc01_security.txt`).
    - `<väljund_leidude_fail>`: Failinimi, kuhu analüüsi leiud salvestatakse (nt `dc01_earlier_findings.txt`).
    - `<alguskuupäev_format_MMM_DD_YYYY>`: Analüüsi alguskuupäev formaadis "Okt 16, 2025".
    - `<lõppkuupäev_format_MMM_DD_YYYY>`: Analüüsi lõppkuupäev formaadis "Nov 15, 2025".

### 4. `analyze_infra01_system_logs.py`
- **Kirjeldus:** Analüüsib rakendusserveri `TRL-INFRA01` süsteemilogi (tekstivormingus) intsidendi kuupäeval (16. november 2025). Skript otsib süsteemi väljalülitamisi (Event ID 1074, 6006, 6008) ja kriitilisi vigu/hoiatusi.
- **Kasutus:**
    ```bash
    python analyze_infra01_system_logs.py <sisend_teksti_fail> <väljund_leidude_fail> [intsidendi_kuupäev]
    ```
    - `<sisend_teksti_fail>`: Teisendatud süsteemilogi tekstifail (nt `infra01_system.txt`).
    - `<väljund_leidude_fail>`: Failinimi, kuhu analüüsi leiud salvestatakse (nt `infra01_system_findings.txt`).
    - `[intsidendi_kuupäev]`: Valikuline. Intsidendi kuupäev formaadis "Nov 16, 2025". Vaikimisi "Nov 16, 2025".

### 5. `analyze_infra01_application_logs.py`
- **Kirjeldus:** Analüüsib rakendusserveri `TRL-INFRA01` rakenduslogi (tekstivormingus) intsidendi kuupäeval (16. november 2025). Skript otsib PostgreSQL-i vigu ja väljalülitamisi ning muid kriitilisi rakendusvigu.
- **Kasutus:**
    ```bash
    python analyze_infra01_application_logs.py <sisend_teksti_fail> <väljund_leidude_fail> [intsidendi_kuupäev]
    ```
    - `<sisend_teksti_fail>`: Teisendatud rakenduslogi tekstifail (nt `infra01_application.txt`).
    - `<väljund_leidude_fail>`: Failinimi, kuhu analüüsi leiud salvestatakse (nt `infra01_application_findings.txt`).
    - `[intsidendi_kuupäev]`: Valikuline. Intsidendi kuupäev formaadis "Nov 16, 2025". Vaikimisi "Nov 16, 2025".

## Soovitatav kasutusjärjekord

1.  **Teisenda logifailid:**
    Käivita `extract_evtx_to_text.py` iga `.evtx` faili jaoks, mida soovid analüüsida (nt Security.evtx, System.evtx, Application.evtx kõigilt masinatelt).
    ```bash
    python extract_evtx_to_text.py TRL-DC01/winevt/logs/Security.evtx dc01_security.txt
    python extract_evtx_to_text.py TRL-WIN10-01/winevt/logs/Security.evtx win10_security.txt
    python extract_evtx_to_text.py TRL-INFRA01/winevt/logs/Security.evtx infra01_security.txt
    python extract_evtx_to_text.py TRL-INFRA01/winevt/logs/System.evtx infra01_system.txt
    python extract_evtx_to_text.py TRL-INFRA01/winevt/logs/Application.evtx infra01_application.txt
    ```

2.  **Analüüsi DC turvalogi varasemat perioodi:**
    ```bash
    python analyze_earlier_dc_logs.py dc01_security.txt dc01_earlier_findings.txt "Oct 16, 2025" "Nov 15, 2025"
    ```

3.  **Analüüsi turvalogisid (intsidendi kuupäev):**
    Käivita `analyze_infra01_security_logs.py` rakendusserveri turvalogi jaoks.
    ```bash
    python analyze_infra01_security_logs.py infra01_security.txt infra01_security_findings.txt
    ```

4.  **Analüüsi süsteemilogisid (intsidendi kuupäev):**
    Käivita `analyze_infra01_system_logs.py` rakendusserveri süsteemilogi jaoks.
    ```bash
    python analyze_infra01_system_logs.py infra01_system.txt infra01_system_findings.txt
    ```

5.  **Analüüsi rakenduslogisid (intsidendi kuupäev):**
    Käivita `analyze_infra01_application_logs.py` rakendusserveri rakenduslogi jaoks.
    ```bash
    python analyze_infra01_application_logs.py infra01_application.txt infra01_application_findings.txt
    ```

Need sammud annavad põhjaliku ülevaate intsidendi kuupäeval toimunud sündmustest, keskendudes avastatud kahtlastele tegevustele.
