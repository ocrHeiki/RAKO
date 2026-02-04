# Intsidendi analüüsi leiud (seisuga 2026-02-04)

## Intsidendi kirjeldus
Kasutaja Pille Porgand märkas 16.11 päeval, et arvutiga toimub midagi kahtlast. Töö tegemise ajal logiti ta järsku masinast välja. Hiljem uuesti sisse logides avanesid ekraanil korraks kahtlased aknad, mida ta varem polnud märganud.

## Analüüsitud süsteemid ja logid
- **TRL-DC01:** Domeenikontroller (Server 2019) - `Security.evtx`
- **TRL-WIN10-01:** Windows 10 tööjaam - `Security.evtx`, `Application.evtx`
- **TRL-INFRA01:** Rakendusserver (Server 2016) - `Security.evtx`, `Application.evtx`, `System.evtx`

## Peamised leiud (kronoloogilises järjekorras)

### 1. Pille Porgandi konto loomine (TRL-DC01 - Domeenikontroller)
-   **Kuupäev ja aeg:** 30. oktoober 2025, 08:17:10 UTC
-   **Sündmus:** Pille Porgandi kasutajakonto (`pille.porgand`) loomine `Administrator` poolt. (Sündmuse ID 4720).

### 2. Pille Porgandi lisamine turvagruppi (TRL-DC01 - Domeenikontroller)
-   **Kuupäev ja aeg:** 11. november 2025, 16:19:25 UTC
-   **Sündmus:** Pille Porgandi lisamine `Sec-HQ-Users` turvagruppi `Administrator` poolt. (Sündmuse ID 4728).

### 3. Varasem tegevus TRL-DC01 domeenikontrolleris (16. oktoober - 15. november 2025)
-   **Leidude puudumine:** Üldiselt puudub selge ja märkimisväärne kahtlane tegevus, mis viitaks ründaja varasemale kohalolekule süsteemis enne 16. novembril 2025.
-   **Pille Porgandi konto:** Tema konto loomise ja grupiliikmelisuse muudatuste sündmused on kooskõlas tavapäraste domeeniadministratsiooni tegevustega.
-   **Administraatori tegevus:** 15. novembril 2025 toimusid Administraatori sisselogimised, tööjaama lukustamised ja väljalogimised, mis näivad olevat tavalised haldustegevused.

### 4. Brute-force/sõnastikurünnak TRL-INFRA01 rakendusserverile ja TRL-DC01 domeenikontrollerile
-   **Kuupäev ja aeg:** 16. november 2025, 09:01:16 kuni 09:51:21 UTC (ja ka hiljem DC-l)
-   **Sündmus:** Mitmed ebaõnnestunud sisselogimiskatsed (Event ID 4625, Logon Type 3, NTLM autentimine) toimusid nii `TRL-INFRA01` serverile kui ka **`TRL-DC01` domeenikontrollerile**. See viitab koordineeritud või samaaegsele rünnakule mitme domeeniressursi vastu.
-   **Sihtmärgiks olnud kontod (mõlemas süsteemis):**
    -   **`Pille.Porgand`**
    -   `Administrator`
    -   `Peeter.Meeter`
    -   `Jaak.Tamm`
    -   `Admin`, `a`, `X`, `pcguest`, `root`, `guest`, `db2admin` ja mitmed genereeritud stringid (nt `15887923FCED06C2`, `1B9E3760`).
-   **Uus avastus TRL-DC01-l:** Kell 14:56 UTC toimus ebaõnnestunud sisselogimiskatse `WDAGUtllityAccount` kontoga `TRL-WIN11-02` masinast. See viitab ründaja võimalikule liikumisele või jalajälje laiendamisele pärast esialgse juurdepääsu saamist.
-   **Järeldus:** See on selge märk süstemaatilisest rünnakust, mis püüdis tuvastada kehtivaid mandaate kogu domeenis.

### 5. Edukad sisselogimised brute-force perioodil (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 09:01:16 kuni 09:51:21 UTC
-   **Sündmused:** Brute-force rünnaku perioodil toimusid ka mitmed edukad sisselogimised:
    -   `ANONYMOUS LOGON` (IP: `10.10.80.16`): mitmed sisselogimised alates `09:01:16 UTC`.
    -   `jaak-admin` (IP: `10.10.80.16`): sisselogimised kell `09:10:38 UTC` ja `09:13:28 UTC`.
    -   `Administrator` (IP: `127.0.0.1` - localhost): sisselogimine kell **`09:39:03 UTC`**. See on kriitiline, kuna toimus brute-force rünnaku ajal.
    -   `pille.porgand` (IP: `10.10.80.17`): sisselogimine kell **`09:39:38 UTC`**.
    -   `rpd7service` (IP: `10.10.80.8` või `-`): arvukad sisselogimised alates `09:48:57 UTC`.

### 6. Pille Porgandi ligipääs jagatud dokumentidele (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 09:41:17 UTC
-   **Sündmus:** `pille.porgand` pääses ligi võrgujagamisele `\\*.\Documents` (`\??\C:\Data\Documents`). See toimus lühikest aega pärast kahtlase tegevuse algust.

### 7. Kahtlane tegevus `Administrator` konto poolt (TRL-INFRA01 rakendusserver)
-   **Chrome'i käivitamine:** Umbes **09:43:40 UTC** käivitas `Administrator` Google Chrome'i (`chrome.exe`) parameetritega, mis võivad viidata failide lahtipakkimisele (`--type=utility --utility-sub-type=unzip.mojom.Unzipper`). See võib olla seotud pahatahtlike tööriistade allalaadimise ja lahtipakkimisega.
-   **Nmap käivitamine:** Umbes **09:44:26 UTC** käivitati `TRL-INFRA01` serveris `nmap.exe` (`C:\Program Files\rapid7\nexpose\nse\nmap\nmap.exe`). Nmap on võrguskanner ja selle käivitamine rakendusserveris on tugev märk pahatahtlikust tegevusest (siseuuringud).

### 8. Ootamatu süsteemi väljalülitamine (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 14:21:26 UTC
-   **Sündmus:** Server kukkus kokku või lülitati jõuga välja (Event ID 6008). See seletab Pille Porgandi "järsku väljalogimise" tema võrguseansilt `TRL-INFRA01` serveris.

### 9. Rakendusvead ja teenuse väljalülitamine (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 19:44:56 UTC
-   **Sündmus:** Kriitilised PostgreSQL andmebaasivead ja ühenduste katkestamine "administraatori käsu" tõttu, millele järgnes PostgreSQL teenuse väljalülitamine.

### 10. Kasutaja algatatud süsteemi väljalülitamine (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 19:44:55 UTC
-   **Sündmus:** `EPP-TRIAL\Administrator` kasutaja lülitas serveri välja (Event ID 1074). See võis olla taastekatse või ründaja tegevus. Sündmuselogi teenus peatati (Event ID 6006) kell 19:44:57 UTC, mis kinnitab korralikku süsteemi väljalülitamist.

### 11. Tegevus TRL-WIN10-01 tööjaamas
-   `TRL-WIN10-01` (`Workstation`) `Security.evtx` ja `Application.evtx` logides ei leitud 16. novembril 2025 Pille Porgandi tegevust (sisselogimisi, väljalogimisi) ega üldist tegevust. Tundub, et selle tööjaama logid ei sisalda intsidendi kuupäeval andmeid.

### 12. Pille Porgandi tegevus TRL-DC01 domeenikontrolleris
-   Pille Porgandi domeenikonto (`pille.porgand`) on olemas.
-   Kogu `TRL-DC01` turvalogis ei leitud Pille Porgandi väljalogimissündmusi (Event ID 4634). See on kahtlane, arvestades "järsku väljalogimist". Võimalikud põhjused hõlmavad auditeerimispoliitika puudusi või ebanormaalset seansi lõppemist.
-   `TRL-DC01` logides ei leitud `Administrator` konto edukaid sisselogimisi `TRL-INFRA01` serverisse 16. novembril 2025, mis viitab, et administraator ei loginud domeeni kaudu sisse või konto oli kompromiteeritud.

## Järeldused ja hüpotees
1.  **Ajas kokkulangevus:** Brute-force/sõnastikurünnak `TRL-INFRA01` serverile ja `TRL-DC01` domeenikontrollerile leidis aset samal päeval, 16. novembril 2025, ja ajaliselt enne Pille Porgandi edukaid sisselogimisi samale serverile. Pille Porgandi konto oli rünnaku sihtmärgiks.
2.  **Seansi ebanormaalne lõppemine:** Ootamatu väljalülitamine kell `14:21 UTC` seletab Pille Porgandi "järsku väljalogimise" tema võrguseansilt `TRL-INFRA01` serveris.
3.  **Hüpotees:**
    -   Ründaja algatas brute-force rünnaku `TRL-INFRA01` ja `TRL-DC01` vastu ajavahemikus 09:01 UTC kuni 09:51 UTC ning kompromiteeris edukalt `Administrator` konto umbes `09:39 UTC`. Tõenäoliselt kompromiteeriti ka `jaak-admin` konto.
    -   Ründaja kasutas kompromiteeritud `Administrator` kontot siseuuringute läbiviimiseks (Nmap käivitamine) ja pahatahtlike tööriistade potentsiaalseks allalaadimiseks/lahtipakkimiseks (Chrome'i käivitamine).
    -   Need tegevused (või mõni muu ründaja põhjustatud sündmus) viisid `TRL-INFRA01` serveri krahhini kell `14:21 UTC`, mis põhjustas Pille Porgandi seansi ebanormaalse lõppemise.
    -   Pille Porgandi sisselogimisel pärast serveri krahhi võis ründaja (kes oli ikka veel aktiivne või oli jätnud püsivuse) käivitada tema tööjaamas "kahtlased aknad".
    -   Lõpuks lülitas `Administrator` (tõenäoliselt kompromiteeritud konto või ründaja poolt kasutatud) serveri välja kell `19:44 UTC`, pärssides samal ajal PostgreSQL teenust.

## Edasised sammud
Käesolev hetk näitab, et audit on lõpule viidud esimeste leidudeni ja hüpotees on koherentne ning toetatud logiandmetega.
Lõplikud leiud on failis `leiud.md`.
