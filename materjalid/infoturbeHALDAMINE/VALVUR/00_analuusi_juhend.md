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
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Windowsi intsidentide analüüsi koondjuhend.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# Projekti ülevaade

### Miks "VALVUR"?

Nimi **VALVUR** valiti tähistama kompromissitut järelevalvet ja analüütilist täpsust. Infosüsteemi uurimisel ei piisa vaid pealiskaudsest vaatlusest – vaja on "valvurit", kes märkab ka kõige väiksemaid kõrvalekaldeveid tavapärasest käitumisest, kaardistab sündmuste kronoloogia ja tuvastab ründaja poolt jäetud varjatud jäljed.

ASCII-põhine visuaalne identiteet on kummardus klassikalisele küberkaitse ja *forensics* kultuurile, kus selgus ja funktsionaalsus on alati esikohal.

---

# Windowsi intsidentide analüüsi juhend (v2.0)

See on professionaalne ja struktureeritud tööraamistik Windowsi operatsioonisüsteemi logide analüüsimiseks rünnete korral.

## 1. Kuldreeglid ja ettevalmistus

### **TÄHTIS: Analüüsi välisel andmekandjal!**
Ära kunagi teosta analüüsi ega salvesta tulemusi otse uuritava masina kõvakettale. Iga uus fail, mille masinasse lood, võib üle kirjutada ründaja poolt kustutatud andmed või muuta olulisi metaandmeid (*TimeStamps*). 
*   Kopeeri logid välisele mälupulgale või kettale.
*   Käivita skriptid ja salvesta `TULEMUSED` välisele andmekandjale.

### Vajalikud teegid (Libraries)
Enne alustamist paigalda vajalik raamatukogu:
```bash
pip install python-evtx
```

## 2. Kaustastruktuur ja töövoog

Hoiame andmeid ja skripte eraldi kaustades:
*   **VALVUR/LOGID/** - Siia kopeeri uuritavad `.evtx` failid.
*   **VALVUR/SKRIPTID/** - Siin asuvad Pythoni skriptid.
*   **VALVUR/TULEMUSED/** - Siia salvestuvad kõik skriptide loodud CSV-failid.

Käivita skriptid järjekorras **01**, **02**, **03**.

## 3. Analüüsi tööriistad

Lisaks Excelile on tungivalt soovitatav kasutada professionaalset tööriista:
*   **Timeline Explorer (Eric Zimmerman)** - See on parim vahend suurte CSV-failide analüüsiks. See võimaldab välkkiiret sorteerimist, grupeerimist ja filtreerimist. 
    *   *Märkus:* Timeline Explorer on Windowsi tööriist, kuid töötab Linuxis suurepäraselt läbi **Wine** keskkonna.

## 4. Milliseid logifaile uurida? (Prioriteedid)

| Logifail | Tähtsus | Mida sealt otsida? |
| :--- | :--- | :--- |
| **Security.evtx** | **KRIITILINE** | Sisselogimised (4624), ebaõnnestunud katsed (4625), protsesside loomine (4688). |
| **System.evtx** | **OLULINE** | Uute teenuste paigaldamine (4697, 7045), logide kustutamine (1102). |
| **PowerShell Operational** | **KÕRGEM** | Ründajate poolt käivitatud skriptide sisu (4104). |

---
*Edu Pythoni õppimisel ja turbeintsidentide lahendamisel!*
