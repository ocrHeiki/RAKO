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
#   |   FAILI NIMI:  03_skriptid.md                                       |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   VALVUR-i analüüsimoodulite detailne kirjeldus.       |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# VALVUR Skriptide Ülevaade

VALVUR koosneb etapiviisilistest skriptidest, mida juhib `valvurMASTER.py`.

### 00_terviklus_kontroll.py
Arvutab algallika logide (EVTX, syslog) SHA-256 räsid enne analüüsi alustamist.

### 01_konverteering_evtx_csv.py
Teisendab Windowsi .evtx logid CSV formaati. Toetab lukus failide kopeerimist.

### 02_linux_logid_csv.py
Teisendab Linuxi syslogid ühtsesse CSV formaati.

### 03_turvafiltreering.py
Eraldab logidest kriitilised turvasündmused (GPO, Logon jne).

### 04_otsing_marksonade_jargi.py
Otsib logidest ründetööriistade jälgi (MITRE ATT&CK / CVE).

### 05_powershell_dekodeerimine.py
Dekodeerib obfuskeeritud PowerShell koodi (Base64/XOR).

### 06_kahtlased_failid.py
Teostab süsteemi reaalajas kontrolli (Live Scan) ja otsib peidetud faile.

### 07_turvaaudit.py
Kontrollib vastavust E-ITS standardile ja koostab Roadmapi.

### 08_genereeriRAPORT.py
Koostab lõpliku koondraporti (Executive Summary + detailid).

### 09_tehniline_raport_pdf.py
Genereerib tehnilise PDF ülevaate.

### 10_threat_intel.py
Kontrollib IP-aadresside mainet välisandmebaasidest.

### 11_vorgu_skaneerimine.py
Kaardistab võrgu varad ja teenused (nmap).

### 12_kasutajate_nimekiri.py
Loetleb süsteemi kasutajad ja tuvastab UID 0 kontod.

### 13_malu_analuus.py
Liides Volatility 3 jaoks mäluanalüüsiks.

### 14_koond_ajajoon.py
Genereerib ühtse kronoloogilise ajajoone (Unified Timeline).

### 15_linux_syvaanaluus.py
Tuvastab logide manipuleerimist (Log Tampering) ja analüüsib SSH-d.

### valvurMASTER.py
Süsteemi peamootor, mis juhib kogu analüüsiahelat.
