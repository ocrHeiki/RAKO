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
#   |   LOODUD:      27.03.2026 (UUENDATUD v3.1)                          |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Windowsi intsidentide analüüsi koondjuhend.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# Projekti ülevaade: VALVUR

Nimi **VALVUR** tähistab kompromissitut järelevalvet ja analüütilist täpsust. See raamistik on loodud Windowsi logide automatiseeritud töötlemiseks, muutes toored binaarandmed professionaalseks raportiks.

ASCII-põhine visuaalne identiteet on kummardus klassikalisele küberkaitse- ja *forensics*-kultuurile, kus selgus ja funktsionaalsus on alati esikohal.

---

# Windowsi intsidentide analüüsi juhend (v3.1)

## 1. Ettevalmistus ja nõuded

### **TÄHTIS: Tõendite puutumatus!**
* **Analüüsi välisel andmekandjal!** Ära kunagi teosta analüüsi uuritava masina kõvakettal.
* **Andmete terviklikkus:** Iga uus fail uuritavas masinas võib üle kirjutada ründaja poolt kustutatud andmed.

### Vajalikud Pythoni teegid
Enne süsteemi käivitamist paigalda vajalikud raamatukogud:
```bash
pip install python-evtx python-docx
2. Kaustastruktuur ja failid
Kõik skriptid asuvad üheskoos ühes kaustas (nt SKRIPTID/ või projekti juurkaust):
• valvurMASTER.py - Keskne juhtpult (Mootor).
• 01_konverteering_evtx_csv.py - Logide dešifreerimine.
• 02_turvafiltreering.py - Kriitiliste ID-de Timeline.
• 03_otsing_marksonade_jargi.py - Tööriistade ja IOC-de tuvastus.
• 04_powershell_dekodeerimine.py - Base64 lahkamine.
• 05_genereeriRAPORT.py - Wordi raporti koostamine.
Andmete jaoks kasutatakse (vastavalt seadistusele) naaberkaustu:
• ../LOGID/ - Toored .evtx failid.
• ../TULEMUSED/ - Valmis raportid ja CSV-tabelid.
3. Analüüsi ahel (Pipeline)
VALVUR läbib viis automaatset etappi, mida juhib valvurMASTER.py. See mootor kutsub skripte järjestikku, kontrollides iga etapi edukust.
Märkus: 5. etapis teisendatakse ajatemplid automaatselt Eesti ajavööndisse (Europe/Tallinn), et tagada sünkroniseeritus kohaliku kellaajaga.
4. Prioriteetsed logifailid
| Logifail | Tähtsus | Mida sealt otsime? |
| :--- | :--- | :--- |
| **Security.evtx** | **KRIITILINE** | Sisselogimised (4624), protsesside loomine (4688). |
| **System.evtx** | **OLULINE** | Teenuste paigaldamine (7045), logide kustutamine (1102). |
| **PowerShell Operational**| **KÕRGEM** | Ründajate skriptide sisu (4104). |
5. Kasutamine
1. Pane .evtx failid kausta LOGID.
2. Mine terminalis skriptide kausta.
3. Käivita peaskript:
python3 valvurMASTER.py
4. Leia lõplik raport kaustast TULEMUSED.
