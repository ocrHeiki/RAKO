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
#   |   PROJEKT:     VALVUR - Automaatne Intsidentide Analüüsi Ahel       |   #
#   |   VERSIOON:    3.1                                                  |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Windowsi logide süvaanalüüs ja raporti koostamine.   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```
# VALVUR - Windows Forensics Toolset

**VALVUR** on Pythoni-põhine tööriistakomplekt digitaalseks ekspertiisiks (*Digital Forensics*). 
See automatiseerib Windowsi sündmuslogide (.evtx) töötlemise, filtreerimise ja analüüsi, 
väljastades lõpptulemusena struktureeritud Wordi raporti.


## Projekti ülevaade: VALVUR

Nimi **VALVUR** tähistab kompromissitut järelevalvet ja analüütilist täpsust. 
See raamistik on loodud Windowsi logide automatiseeritud töötlemiseks, muutes toored binaarandmed professionaalseks raportiks.

ASCII-põhine visuaalne identiteet on kummardus klassikalisele küberkaitse- ja *forensics*-kultuurile, kus selgus ja funktsionaalsus on alati esikohal.

---

## 🚀 Keskne Funktsionaalsus

VALVUR läbib viis automaatset etappi, mida juhib **`valvurMASTER.py`**:

1.  **Konverteerimine**: Binaarsed logid teisendatakse CSV-vormingusse.
2.  **Filtreerimine**: Sõelutakse välja kriitilised sündmused (sisselogimised, teenused, kustutamised).
3.  **IOC Otsing**: Tuvastatakse tuntud ründevara ja häkkerite tööriistad (Mimikatz, PsExec jne).
4.  **Süvaanalüüs**: PowerShell skriptide dekodeerimine (Base64) ja ründaja IP-aadresside leidmine.
5.  **Raporteerimine**: Koostatakse kronoloogiline raport **Eesti ajavööndis** (.docx).

---

## 📂 Kaustastruktuur

Süsteem eeldab järgmist ülesehitust:

```text
VALVUR/
├── README.md               <-- See fail (ülevaade)
├── 00_analuusi_juhend.md   <-- Põhjalik metoodiline juhend
├── LOGID/                  <-- Sisendkaust (pane siia .evtx failid)
├── TULEMUSED/              <-- Väljundkaust (CSV-d ja Wordi raport)
└── SKRIPTID/               <-- Tööriistakaust (kõik .py skriptid)
```
## 🛠️ Paigaldamine ja Kasutamine

**Sõltuvused:** 
Veendu, et sul on Python 3 ja vajalikud teegid:
```
pip install python-evtx python-docx
```
**Käivitamine:**
Liigu SKRIPTID/ kausta ja käivita peaskript:
```
python3 valvurMASTER.py
```
## 🛡️ Miks VALVUR?

Erinevalt tavalisest logivaaturist keskendub VALVUR "ründaja loogikale". 
See ei näita lihtsalt andmeid, vaid proovib leida seoseid, dekodeerida peidetud käske 
ja esitada need uurijale loetaval kujul, hoides samal ajal kokku tunde rutiinset tööd.

Loodud õppe- ja uurimistöö eesmärgil. Hoia süsteemidel silm peal!
