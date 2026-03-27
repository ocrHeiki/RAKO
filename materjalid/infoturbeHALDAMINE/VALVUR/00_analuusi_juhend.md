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
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  00_analuusi_juhend.md                                |   #
#   |   LOODUD:      27:03:2027                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Windowsi intsidentide analüüsi koondjuhend.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```
# Projekti ülevaade

### Miks "VALVUR"?

Nimi **VALVUR** valiti tähistama kompromissitut järelevalvet ja analüütilist täpsust. Infosüsteemi uurimisel ei piisa vaid pealiskaudsest vaatlusest – vaja on "valvurit", kes märkab ka kõige väiksemaid kõrvalekaldeid tavapärasest käitumisest, kaardistab sündmuste kronoloogia ja tuvastab ründaja poolt jäetud varjatud jäljed.

ASCII-põhine visuaalne identiteet on kummardus klassikalisele küberkaitse ja *forensics* kultuurile, kus selgus ja funktsionaalsus on alati esikohal.

---

# Windowsi intsidentide analüüsi juhend (v1.9)

See on professionaalne ja struktureeritud tööraamistik Windowsi operatsioonisüsteemi logide analüüsimiseks rünnete korral.

## 1. Kaustastruktuur ja Ettevalmistus

Hoiame andmeid ja skripte eraldi kaustades, et vältida segadust:
*   **VALVUR/LOGID/** - Siia pane oma uuritavad `.evtx` failid.
*   **VALVUR/SKRIPTID/** - Siin asuvad Pythoni skriptid.
*   **VALVUR/TULEMUSED/** - Siia salvestuvad kõik skriptide loodud CSV-failid.

### Vajalikud teegid (Libraries)
Enne alustamist paigalda vajalik raamatukogu:
```bash
pip install python-evtx
```

## 2. Analüüsi töövoog (Workflow)

Käivita skriptid **VALVUR** peakaustas olles:

1.  **01_konverteering_evtx_csv.py** - Loeb `.evtx` failid `LOGID` kaustast ja teeb neist loetavad CSV-d `TULEMUSED` kausta.
2.  **02_turvafiltreering.py** - Filtreerib `TULEMUSED` kaustas olevaid CSV-sid ja otsib kriitilisi Event ID-sid.
3.  **03_otsing_marksonade_jargi.py** - Otsib `TULEMUSED` kaustas olevatest CSV-dest kahtlaseid märksõnu.

## 3. Milliseid logifaile uurida? (Prioriteedid)

| Logifail | Tähtsus | Mida sealt otsida? |
| :--- | :--- | :--- |
| **Security.evtx** | **KRIITILINE** | Sisselogimised (4624), ebaõnnestunud katsed (4625), protsesside loomine (4688). |
| **System.evtx** | **OLULINE** | Uute teenuste paigaldamine (4697, 7045), logide kustutamine (1102). |
| **PowerShell Operational** | **KÕRGEM** | Ründajate poolt käivitatud skriptide sisu (4104). |

---
*Edu Pythoni õppimisel ja turbeintsidentide lahendamisel!*
