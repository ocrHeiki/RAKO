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
#   |   FAILI NIMI:  DEMO_SPIKK.md                                 |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Eksami esitlusspikker ja tehniline tugi.      |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################


# VALVUR - Eksami Esitlusspikker (Demo Cheat Sheet)

Kasuta seda spikrit, kui käivitad skripti komisjoni ees. See aitab täita "vaikust" ja näidata oma asjatundlikkust.

## 1. Algus (MASTER käivitamine)
- **Mida öelda:** "Käivitan VALVUR-i peamootori. See kontrollib esmalt minu õigusi ja tuvastab, et töö toimub kloonitud masinas, et tagada originaalandmete puutumatus vastavalt ISO standardile."

## 2. Terviklus (00) ja Import (01)
- **Mida öelda:** "Nüüd arvutab süsteem logifailidele SHA-256 räsid. See on forensika kuldstandard – kui ma hiljem andmeid muudan, siis räsid ei klapi ja ma jään vahele. Järgmisena kopeerib süsteem lukustatud Windowsi logid turvalisse kohta ja konverteerib need analüüsiks sobivasse CSV-formaati."

## 3. Filtreerimine (02) ja Märksõnad (03)
- **Mida öelda:** "Selles etapis puhastab VALVUR logid mürast. Me ei otsi lihtsalt 'midagi', vaid kasutame MITRE ATT&CK maatriksit, et leida ründajate spetsiifilisi tehnikaid nagu Credential Dumping või Lateral Movement."

## 4. Süvaanalüüs (04) ja Kahtlased failid (06)
- **Mida öelda:** "Siin toimub maagia. VALVUR proovib automaatselt dekodeerida obfuskeeritud PowerShell koodi (Base64 ja XOR). Samuti kontrollib süsteem 'Live Scan' meetodil ajutisi kaustu ja Linuxi püsivuse märke nagu uued SSH võtmed või Cron-tööd."

## 5. Audit (07) ja Kasutajad (11)
- **Mida öelda:** "Nüüd liigume NIST raamistiku 'Protect' faasi. Kontrollime süsteemi vastavust E-ITS paroolipoliitikale ja otsime peidetud root-õigustega kasutajaid. Tulemuseks on samm-sammuline Roadmap süsteemi parandamiseks."

## 6. Kokkuvõte (05 ja Timeline 13)
- **Mida öelda:** "Lõpuks koondab VALVUR kõik killud ühtseks kronoloogiliseks ajajooneks. See võimaldab meil sekundilise täpsusega näha, kuidas ründaja masinasse sisenes ja mis ta siin tegi. Genereeritud Executive Summary on suunatud juhtkonnale, andes kiire vastuse: mis juhtus ja kui hull see on."

---
**NIPP:** Kui mõni skript viskab vea, ütle rahulikult: "Tegemist on mitte-kriitilise hoiatusega. MASTER-skript on ehitatud robustseks ja jätkab teiste andmeallikate analüüsi."
