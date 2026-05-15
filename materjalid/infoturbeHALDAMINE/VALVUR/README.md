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
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  README.md                                     |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Projekti koondülevaade ja kiirkäivitusjuhend. |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################


# VALVUR - Intsidendi süvaanalüüsi ja turvaauditi platvorm

**VALVUR** on professionaalne ja automatiseeritud tööriistakomplekt Windowsi ja Linuxi operatsioonisüsteemide turvaauditiks ja küberintsidentide lahendamiseks. Projekt on loodud eksamitööna (2026), kuid järgib tööstusstandardeid nagu **NIST CSF 2.0** ja **MITRE ATT&CK**.

## 🚀 Kiirkäivitus (Remote Launch)
VALVUR-i saab käivitada otse GitHubist ilma käsitsi installita:
```bash
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/RAKO/main/materjalid/infoturbeHALDAMINE/VALVUR/launch_VALVUR.py)"
```

## 🛡️ Strateegiline raamistik: NIST CSF 2.0
VALVUR on ehitatud NIST põhisammastele:
- **IDENTIFY**: Süsteemi varade ja kasutajate kaardistus (Skriptid 07, 10, 11).
- **PROTECT**: E-ITS audit ja turvapoliitika kontroll (Skript 07).
- **DETECT**: MITRE ATT&CK põhine logi- ja failianalüüs (Skriptid 02, 03, 06).
- **RESPOND**: Automatiseeritud normaliseeritud raporteerimine.
- **RECOVER**: Kronoloogiline ajajoon (Timeline) süsteemi taastamiseks.

## 🧠 HeRe kontseptsioon: Väe ja Tarkuse Liit
Esitlusmaterjalides kannab projekt nime **HeRe** (Heiki Rebane & Helena Reinhold):
- **HE (Might)**: Tehniline kaitsevõimekus (krüptograafia, tulemüürid).
- **RE (Mind)**: Strateegiline analüüs ja ründaja kavaluse mõistmine.
- **Moto**: *"Vägi ilma tarkuseta on pime, tarkus ilma väeta on võimetu."*

## 🛠️ Töövoog (Workflow)
Analüüs toimub järgmises järjekorras (MASTER Control):
1.  **Terviklus (00)**: SHA-256 räside arvutamine (Forensiliselt korrektne).
2.  **Import (01)**: Logide konverteerimine CSV-ks (sisaldab lukustatud failide kopeerimist).
3.  **Filtreerimine (02)**: Müra eemaldamine ja kriitiliste sündmuste eraldamine.
4.  **Analüüs (03-04)**: MITRE märksõnade otsing, Fuzzy Matching ja XOR dekodeerimine.
5.  **Live Scan (06)**: Peidetud failid, Cron-tööd ja brauseri indikaatorid.
6.  **Audit (07)**: E-ITS vastavuskontroll ja **Roadmap** genereerimine.
7.  **Visualiseerimine (13)**: Ühtne kronoloogiline ajajoon (Unified Timeline).
8.  **Raporteerimine (05, 08)**: Executive Summary ja tehniline raport.

## ⚖️ Metoodiline märkus
Analüüs on teostatud süsteemi kloonil. Algne tõendusmaterjal on säilitatud puutumatuna vastavalt **ISO 27037** standardile.
