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
#   |   FAILI NIMI:  skriptid.md (UUENDATUD)                              |   #
#   |   LOODUD:      27.03.2026                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Skriptide tehniline dokumentatsioon (Etapid 01-05).  |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
```
# Skriptide Tehniline Ülevaade (v2.0)

See dokument selgitab VALVUR projekti Pythoni töövoogu, funktsioone ja andmete liikumist.

---

## 1. valvurMASTER.py (Keskne mootor)
See skript on "orkestraator", mis hoiab analüüsi ahelat koos.

* **`subprocess.run()`**: Käivitab järgmise etapi Pythoni faili. See ootab eelneva etapi lõpetamist (sünkroonne töövoog).
* **`check=True`**: Kriitiline parameeter - kui näiteks etapp 01 ebaõnnestub, ei hakka peaskript tühjade andmetega edasi töötama, vaid peatub veateatega.
* **`sys.executable`**: Tagab, et kõik alam-skriptid kasutavad täpselt sama Pythoni interpretaatorit, millega alustati.

---

## 2. 01_konverteering_evtx_csv.py
Eesmärk: Binaarsete `.evtx` failide dešifreerimine ja XML-i parsimine.

* **`Evtx.records()`**: Generaator, mis loeb kirjeid ükshaaval, säästes operatiivmälu.
* **`ET.fromstring()`**: Muudab toore XML-teksti Pythoni objektiks, võimaldades otsida välju nagu `EventID` ja `TimeCreated`.
* **`csv.DictWriter`**: Kirjutab andmed CSV-sse, sidudes XML-i väljad konkreetsete veergudega.

---

## 3. 02_turvafiltreering.py
Eesmärk: Müra eemaldamine ja "Timeline" loomine.

* **`critical_ids`**: List, mis defineerib intsidendi uurija fookuse (sisselogimised, teenused, kustutamised).
* **`list.sort(key=...)`**: Kuna logisid loetakse erinevatest failidest, siis see meetod paneb kõik kirjed õigesse ajalisse järjestusse.

---

## 4. 03_otsing_marksonade_jargi.py
Eesmärk: Tuvastada ründaja tegevusmustrid (Threat Hunting).

* **`message.lower()`**: Muudab otsingu lollikindlaks (leiab nii "Mimikatz" kui "mimikatz").
* **`MatchedKeyword`**: Uus veerg CSV-s, mis ütleb uurijale kohe ära, miks konkreetne logirida kahtlasena märgiti.

---

## 5. 04_powershell_dekodeerimine.py
Eesmärk: Obfuskatsiooni (peitmise) eemaldamine.

* **`re.findall()`**: Regulaaravaldised, mis skaneerivad logisid ja leiavad sealt automaatselt IP-aadresse ja Base64 koodi.
* **`base64.b64decode()`**: Võtab ründaja peidetud käsu ja muudab selle baitideks.
* **`.decode('utf-16-le')`**: PowerShelli spetsiifiline kooditabel, mis muudab baidid loetavaks skriptiks.

---

## 6. 05_genereeriRAPORT.py
Eesmärk: Tõendite vormistamine ja ajavööndite korrigeerimine.

* **`ZoneInfo("Europe/Tallinn")`**: Windowsi logid on UTC-s. See funktsioon arvutab automaatselt juurde Eesti suve- või talveaja nihke, et uurija näeks kellaaegu, mis vastavad Eesti ajavööndile.
* **`Document()`**: Loob mälus uue Wordi faili objekti.
* **`doc.add_table()`**: Genereerib dünaamilise tabeli, kus on näha kronoloogiline ülevaade sündmustest.
* **`Pt(8)` ja `Courier New`**: Kasutatakse koodi eristamiseks tavatekstist, et raport oleks loetav ja professionaalne.

---

### Pythoni õppimise punkt: Moodulite importimine
Selles projektis näed sa, kuidas kasutada nii Pythoni **standardteeke** (`os`, `csv`, `datetime`, `re`) kui ka **väliseid teeke** (`python-docx`, `python-evtx`). Välised teegid peab alati enne `pip install` käsuga paigaldama.
