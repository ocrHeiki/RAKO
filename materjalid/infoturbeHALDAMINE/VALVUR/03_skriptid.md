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
#   |   FAILI NIMI:  03_skriptid.md                                |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   VALVUR-i analüüsimoodulite detailne kirjeldus. |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################


# VALVUR Skriptide Ülevaade

VALVUR koosneb mitmest etapilisest skriptist, mida juhib `valvurMASTER.py`.

### 00_terviklus_kontroll.py
Arvutab algallika logide (EVTX, syslog) SHA-256 räsid enne analüüsi alustamist. Tagab andmete puutumatuse tõendamise.

### 01_konverteering_evtx_csv.py / 01_linux_logid_csv.py
Teisendavad algallika logid ühtsesse CSV formaati. Linuxi puhul tuvastab sisselogimised ja omistab neile vastavad ID-d (4624, 4625).

### 02_turvafiltreering.py
Eraldab kriitilised sündmused, sealhulgas GPO muudatused ja SOC standardile vastavad ID-d.

### 09_threat_intel.py
Võtab süvaanalüüsist leitud IP-aadressid ja kontrollib nende mainet (AbuseIPDB valmidus).

### 03_otsing_marksonade_jargi.py
Otsib logidest ründetööriistade jälgi ja seostab need **MITRE ATT&CK** taktikate ning **CVE** koodidega.

### 04_powershell_dekodeerimine.py
Teostab süvaanalüüsi, dekodeerides peidetud PowerShell skripte ja eraldades ründajate IP-aadressid.

### 06_kahtlased_failid.py
Teostab süsteemi reaalajas kontrolli (Live Scan) ajutistes kaustades ja otsib viiteid logidest.

### 07_turvaaudit.py
Kontrollib süsteemi vastavust E-ITS standardile ja pakub parandusmeetmeid.

### 10_vorgu_skaneerimine.py
Kaardistab võrgus olevad hostid ja teenused (nmap), et aidata koostada infovarade võrgujoonist.

### 05_genereeriRAPORT.py
Koostab kronoloogilise ja struktureeritud Wordi (.docx) raporti, koondades kõik analüüsi tulemused.

### 08_tehniline_raport_pdf.py
Genereerib juhtkonnale suunatud tehnilise ülevaate VALVURI süvaanalüüsi võimekusest.

### 11_kasutajate_nimekiri.py
Loetleb kõik unikaalsed kasutajad nii logidest kui ka süsteemist (/etc/passwd), tuvastades peidetud root-õigustega kontod (UID 0).

### 12_malu_analuus.py
Liides Volatility 3 jaoks. Analüüsib mälutõmmiseid (.raw, .mem), tuvastades mälus peituvat pahavara (malfind, pslist).

### 13_koond_ajajoon.py
Genereerib ühtse kronoloogilise ajajoone (Unified Timeline) kõikidest logiallikatest, visualiseerides ründaja teekonda.

### 14_linux_syvaanaluus.py
Linuxi spetsiifiline süvakontroll: logide tervikluse kontroll (Log Tampering) ja SSH sisselogimiste normaliseeritud analüüs.

### valvurMASTER.py
Süsteemi peamootor, mis juhib kogu analüüsiahelat. Sisaldab admin-õiguste kontrolli, metoodilist "klooni" märget ja robustset veatöötlust.
