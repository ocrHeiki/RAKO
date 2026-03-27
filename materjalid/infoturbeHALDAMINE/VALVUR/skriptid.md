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
#   |   FAILI NIMI:  skriptid.md                                          |   #
#   |   LOODUD:      27.03.2026                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Skriptide tehniline dokumentatsioon ja funktsioonid. |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# Skriptide Tehniline Ülevaade

See dokument selgitab VALVUR projekti Pythoni skriptide tööpõhimõtteid, kasutatud teeke ja funktsioone.

---

## 1. valvur_master.py (Keskne mootor)
See skript koordineerib teiste skriptide tööd.

* **`subprocess.run(cmd, check=True)`**: See meetod käivitab välise programmi (antud juhul teise Pythoni skripti). `check=True` tagab, et kui alam-skript ebaõnnestub, peatub ka peaskript.
* **`os.path.join("SKRIPTID", script_name)`**: Turvaline viis failiteede koostamiseks, mis töötab nii Windowsis kui Linuxis.
* **`sys.executable`**: Viitab praegu töötavale Pythoni interpretaatorile, tagades, et kõik etapid läbitakse sama Pythoni versiooniga.

---

## 2. 01_konverteering_evtx_csv.py
Eesmärk: Muuta binaarsed Windowsi logid loetavaks tabeliks.

* **`Evtx(evtx_path)`**: Avab `.evtx` faili voona (stream), mis võimaldab töödelda ka väga suuri logifaile ilma mälu üle koormamata.
* **`record.xml()`**: Muudab binaarse sündmuse XML-stringiks.
* **`ET.fromstring(xml_str)`**: Parsib XML-teksti objektiks, kus saab liikuda mööda "oksi" (nt `find('System')`).
* **`csv.DictWriter`**: Võimaldab kirjutada CSV ridade kaupa, kasutades Pythoni sõnastikku (Dictionary), kus võti on veeru nimi ja väärtus on logi sisu.

---

## 3. 02_turvafiltreering.py
Eesmärk: Müra vähendamine ja kriitiliste sündmuste koondamine.

* **`critical_ids` list**: Filter, mis hoiab mälus ainult küberkaitsja jaoks olulisi sündmusi (nt 4624 - sisselogimine).
* **`all_results.sort(key=lambda x: x['TimeCreated'])`**: Sorteerib kõikidest logifailidest kogutud sündmused üheks kronoloogiliseks jadaks (Timeline).
* **`int(row['Id'])`**: Muudab tekstina loetud ID numbriliseks, et seda saaks võrrelda kriitiliste ID-de nimekirjaga.

---

## 4. 03_otsing_marksonade_jargi.py
Eesmärk: Tuvastada ründaja "käekiri" ja tööriistad.

* **`message.lower()`**: Muudab logi sisu väiketähtedeks, et otsing ei oleks tõstutundlik (nt "Mimikatz" vs "mimikatz").
* **`if word in message`**: Pythoni lihtne ja kiire meetod stringi seest alamsõne leidmiseks.
* **`break`**: Kui sündmusest leiti juba üks kahtlane märksõna, liigutakse järgmise sündmuse juurde, et vältida dubleerimist tulemustes.

---

## 5. 04_powershell_dekodeerimine.py
Eesmärk: Peidetud ründekoodi lahtipakkimine (Deep Forensics).

* **`re.findall(r'[A-Za-z0-9+/]{40,}', text)`**: Regulaaravaldis (Regex), mis otsib tekstist pikki märgijadasid, mis sarnanevad Base64 kodeeringule.
* **`base64.b64decode(m)`**: Dekodeerib leitud jada tagasi baitideks.
* **`.decode('utf-16-le')`**: PowerShell kasutab spetsiifilist UTF-16 Little Endian kodeeringut. See meetod muudab baidid tagasi loetavaks tekstiks.
* **`re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', text)`**: Otsib tekstist IP-aadresse, mis viitavad ründaja serverile (C2).

---

## Kasutamine Pythoni õppimiseks
Kui soovid koodi muuta, pööra tähelepanu **`try...except`** plokkidele. Need on kriitilised, et sinu analüüs ei katkeks, kui mõni logirida on korrumpeerunud või puudulik.
