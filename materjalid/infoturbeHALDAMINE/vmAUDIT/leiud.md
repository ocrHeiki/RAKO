```
###############################################################################
#                                                                             #
#   █████   █████           ████                                              #
#  ▒▒███   ▒▒███           ▒▒███                                              #
#   ▒███    ▒███   ██████   ▒███  █████ █████ █████ ████ ████████             #
#   ▒███    ▒███  ▒▒▒▒▒███  ▒███ ▒▒███ ▒▒███ ▒▒███ ▒███ ▒▒███▒▒███            #
#   ▒▒███   ███    ███████  ▒███  ▒███  ▒███  ▒███ ▒███  ▒███ ▒▒▒             #
#    ▒▒▒█████▒    ███▒▒███  ▒███  ▒▒███ ███   ▒███ ▒███  ▒███                 #
#      ▒▒███     ▒▒████████ █████  ▒▒█████    ▒▒████████ █████                #
#       ▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒      ▒▒▒▒▒▒▒▒ ▒▒▒▒▒                 #
#                                                                             #
###############################################################################
#                                                                             #
#                       INTSIDENDI UURIMISE LEIUD JA RAPORT                   #
#                                                                             #
###############################################################################
```


# Intsidendi analüüsi leiud (seisuga 2026-02-04)

## Intsidendi kirjeldus
Kasutaja Pille Porgand märkas 16.11 päeval, et arvutiga toimub midagi kahtlast. Töö tegemise ajal logiti ta järsku masinast välja. Hiljem uuesti sisse logides avanesid ekraanile korraks kahtlased aknad, mida ta varem polnud märganud.

## Analüüsitud süsteemid ja logid
- **TRL-DC01:** Domeenikontroller (Server 2019) - `Security.evtx`
- **TRL-WIN10-01:** Windows 10 tööjaam - `Security.evtx`, `Application.evtx`
- **TRL-INFRA01:** Rakendusserver (Server 2016) - `Security.evtx`, `Application.evtx`, `System.evtx`

## Analüüsi käigus kasutatud meetodid ja tööriistad

Intsidendi süvaanalüüsi läbiviimiseks kasutati mitmeid spetsialiseeritud meetodeid ja automatiseeritud tööriistu. Need võimaldasid tõhusalt töödelda suuri logimahtusid ja tuvastada kahtlast tegevust erinevates süsteemides.

### 1. Logifailide eeltöötlus ja analüüs
*   **Logide teisendamine:** Binaarsete Windowsi sündmuselogide (`.evtx`) tekstivormingusse teisendamiseks kasutati skripti `extract_evtx_to_text.py`. See on oluline samm enne mistahes tekstipõhise analüüsi läbiviimist.
*   **Eelnevate DC logide analüüs:** Skripti `analyze_earlier_dc_logs.py` kasutati domeenikontrolleri varasema tegevuse analüüsimiseks, et tuvastada potentsiaalseid ründeindikaatoreid enne intsidendi algust.
*   **TRL-INFRA01 logide analüüs:** Rakendusserveri `TRL-INFRA01` turva-, süsteemi- ja rakenduslogide analüüsimiseks intsidendi kuupäeval kasutati vastavalt skripte `analyze_infra01_security_logs.py`, `analyze_infra01_system_logs.py` ja `analyze_infra01_application_logs.py`.
*   **TRL-WIN10-01 allalaadimiste otsimine:** Skripti `search_win10_downloads.py` kasutati Windows 10 tööjaama logidest konkreetse failinimega allalaadimiste otsimiseks määratud ajaperioodil.

### 2. Tööjaama süvaanalüüs (virtuaalkeskkonnas)
Võrguühenduseta virtuaalkeskkonnas läbi viidud süvaanalüüsi käigus rakendati järgmisi meetodeid ja tööriistu:
*   **Süsteemi triaaži skript `audit.py`:** See skript kogus automaatselt kriitilist süsteemiinformatsiooni, nagu jooksvad protsessid, võrguühendused, teenused, startup programmid ja kasutajakontode audit (sh BitLockeri staatus).
*   **Failisüsteemi süvaskaneerimine `deep_scan.py`:** Skripti kasutati failisüsteemi muudatuste, loomisaegade ja SHA256 kontrollsummade tuvastamiseks, keskendudes kahtlastele faililaienditele.
*   **Visuaalne vaatlus ja dokumentatsioon:** Intsidentide süvaanalüüsi ajal tehti süsteemi visuaalset vaatlust, fikseerides kõik olulised leiud (nt veateated, kahtlased aknad) ekraanipiltide ja fotodena.
*   **Mälu dump'i ja disk forensilised koopiad:** Mälu dump'ide ja forensiliste diskikoopiate loomiseks kasutati vastavaid tööriistu (nt `DumpIt`, `FTK Imager Lite`, `dd`). Need koopiad võimaldavad hiljem sügavamat offline analüüsi.

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
-   **Sündmus:** Mitmed ebaõnnestunud sisselogimiskatsed (Event ID 4625, Logon Type 3, NTLM autentimine) toimusid nii `TRL-INFRA01` serverile kui ka **`TRL-DC01` domeenikontrollerile**.
-   **Sihtmärgiks olnud kontod (mõlemas süsteemis):**
    -   **`Pille.Porgand`**
    -   `Administrator`
    -   `Peeter.Meeter`
    -   `Jaak.Tamm`
    -   `Admin`, `a`, `X`, `pcguest`, `root`, `guest`, `db2admin` ja mitmed genereeritud stringid (nt `15887923FCED06C2`, `1B9E3760`).
-   **Uus avastus TRL-DC01-l:** Kell 14:56 UTC toimus ebaõnnestunud sisselogimiskatse `WDAGUtllityAccount` kontoga `TRL-WIN11-02` masinast.
-   **Järeldus:** See on selge märk süstemaatilisest rünnakust, mis püüdis tuvastada kehtivaid mandaate kogu domeenis.

### 5. Edukad sisselogimised brute-force perioodil (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 09:01:16 kuni 09:51:21 UTC
-   **Sündmused:** Brute-force rünnaku perioodil toimusid ka mitmed edukad sisselogimised:
    -   `ANONYMOUS LOGON` (IP: `10.10.80.16`): mitmed sisselogimised alates `09:01:16 UTC`.
    -   `jaak-admin` (IP: `10.10.80.16`): sisselogimised kell `09:10:38 UTC` ja `09:13:28 UTC`.
    -   `Administrator` (IP: `127.0.0.1` - localhost): sisselogimine kell **`09:39:03 UTC`**.
    -   `pille.porgand` (IP: `10.10.80.17`): sisselogimine kell **`09:39:38 UTC`**.
    -   `rpd7service` (IP: `10.10.80.8` või `-`): arvukad sisselogimised alates `09:48:57 UTC`.

### 6. Pille Porgandi ligipääs jagatud dokumentidele (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 09:41:17 UTC
-   **Sündmus:** `pille.porgand` pääses ligi võrgujagamisele `\*.Documents` (`???`C:\Data\Documents`). See toimus lühikest aega pärast kahtlase tegevuse algust.

### 7. Kahtlane tegevus `Administrator` konto poolt (TRL-INFRA01 rakendusserver)
-   **Chrome'i käivitamine:** Umbes **09:43:40 UTC** käivitas `Administrator` Google Chrome'i (`chrome.exe`) parameetritega, mis võivad viidata failide lahtipakkimisele (`--type=utility --utility-sub-type=unzip.mojom.Unzipper`).
-   **Nmap käivitamine:** Umbes **09:44:26 UTC** käivitati `TRL-INFRA01` serveris `nmap.exe` (`C:\Program Files\rapid7\nexpose\nse\nmap\nmap.exe`).

### 8. Ootamatu süsteemi väljalülitamine (TRL-INFRA01 rakendusserver)
-   **Kuupäev ja aeg:** 16. november 2025, 14:21:26 UTC
-   **Sündmus:** Server kukkus kokku või lülitati jõuga välja (Event ID 6008). See seletab Pille Porgandi 
