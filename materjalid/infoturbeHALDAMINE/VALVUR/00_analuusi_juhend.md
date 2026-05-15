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
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Windowsi ja Linuxi intsidentide analüüsi koondjuhend.|   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```
# Projekti ülevaade

### Miks "VALVUR"?

Nimi **VALVUR** valiti tähistama kompromissitut järelevalvet ja analüütilist täpsust. Infosüsteemi uurimisel ei piisa vaid pealiskaudsest vaatlusest – vaja on "valvurit", kes märkab ka kõige väiksemaid kõrvalekaldeveid tavapärasest käitumisest, kaardistab sündmuste kronoloogia ja tuvastab ründaja poolt jäetud varjatud jäljed.

---

# Windowsi ja Linuxi intsidentide analüüsi juhend (v4.0)

See on professionaalne ja struktureeritud tööraamistik Windowsi ja Linuxi operatsioonisüsteemi logide analüüsimiseks ning turvaauditiks.

## 1. Kuldreeglid ja ettevalmistus

### **TÄHTIS: Õigused ja Keskkond**
- **Administraatori õigused:** Skriptid, mis teostavad reaalajas süsteemi kontrolli (06) ja turvaauditit (07), vajavad **Administrator** (Windows) või **sudo** (Linux) õigusi.
- **VMware / Virtuaalkeskkonna erisus:** Enne analüüsi alustamist loo masinast alati **Full Clone** või **Snapshot**. See tagab asitõendi säilimise eksamiolukorras.
- **Analüüsi välisel andmekandjal!** Ära kunagi teosta analüüsi uuritava masina kõvakettal, kui see pole kloon.
- **Terviklus (Hashing):** Alusta alati logide räsimisest, et tõestada andmete puutumatust.

### Vajalikud teegid ja tööriistad
```bash
pip install python-evtx python-docx fpdf
sudo apt install nmap  # Võrgu skaneerimiseks
```

## 2. Täielik töövoog (Ahel 00-10)

VALVUR töötab etapiviisiliselt:

1.  **00_terviklus_kontroll.py** - SHA-256 räsid algmaterjalile.
2.  **01_konverteering / 01_linux_logid** - Teisendamine CSV formaati.
3.  **02_turvafiltreering.py** - Kriitiliste sündmuste (sh GPO muudatused) eraldamine.
4.  **03_otsing_marksonade_jargi.py** - MITRE ATT&CK ja CVE põhine analüüs.
5.  **04_powershell_dekodeerimine.py** - Peidetud koodi paljastamine.
6.  **09_threat_intel.py** - IP-aadresside maine kontroll.
7.  **06_kahtlased_failid.py** - Live-süsteemi kontroll (Temp, Public jne).
8.  **07_turvaaudit.py** - E-ITS vastavuskontroll.
9.  **10_vorgu_skaneerimine.py** - Hostide tuvastamine võrgujoonise jaoks.
10. **05_genereeriRAPORT.py** & **08_pdf_raport** - Lõplik dokumentatsioon.

---
*Edu Pythoni õppimisel ja turbeintsidentide lahendamisel!*
