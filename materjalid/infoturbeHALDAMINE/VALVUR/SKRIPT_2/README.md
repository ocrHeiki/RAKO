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
#   |   FAILI NIMI:  README.md                                            |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Projekti koondülevaade ja kiirkäivitusjuhend.        |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# VALVUR - Intsidendi süvaanalüüsi ja turvaauditi platvorm

**VALVUR** on professionaalne ja automatiseeritud tööriistakomplekt Windowsi ja
Linuxi operatsioonisüsteemide turvaauditiks ja küberintsidentide lahendamiseks.
Projekt järgib tööstusstandardeid nagu **NIST CSF 2.0** ja **MITRE ATT&CK**.

## Kiirkäivitus (Remote Launch)

```bash
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/ocrHeiki/RAKO/main/materjalid/infoturbeHALDAMINE/VALVUR/launch_VALVUR.py)"
```

## Strateegiline raamistik: NIST CSF 2.0

- **IDENTIFY**: Varade ja kasutajate kaardistus (Skriptid 06, 07, 08)
- **PROTECT**: E-ITS audit ja turvapoliitika kontroll (Skript 09)
- **DETECT**: MITRE ATT&CK põhine logi- ja failianalüüs (Skriptid 01-05)
- **RESPOND**: Automatiseeritud raporteerimine (Skriptid 10, 14, 15)
- **RECOVER**: Kronoloogiline ajajoon süsteemi taastamiseks (Skript 13)

## Töövoog (MASTER Control)

1. **Terviklus (00)**: SHA-256 räside arvutamine
2. **Import (01/02)**: Logide konverteerimine CSV-ks (Win/Linux)
3. **Filtreerimine (03)**: Müra eemaldamine ja kriitiliste sündmuste eraldamine
4. **Analüüs (04/05)**: MITRE märksõnade otsing, Fuzzy Matching ja XOR dekodeerimine
5. **Live Scan (06)**: Peidetud failid, Cron-tööd ja brauseri indikaatorid
6. **Võrguskaneerimine (07)**: Võrguvarade ja teenuste kaardistamine
7. **Kasutajate audit (08)**: Kasutajakontode tuvastamine
8. **Turvaaudit (09)**: E-ITS vastavuskontroll ja Roadmap
9. **Threat Intel (10)**: IP-aadresside maine kontroll
10. **Mäluanalüüs (11)**: Volatility 3 liides mälutõmmiste analüüsiks
11. **Linuxi süvaanalüüs (12)**: SSH logide ja logide tervikluse kontroll
12. **Ajajoon (13)**: Ühtne kronoloogiline ajajoon (Unified Timeline)
13. **Raportid (14/15)**: Executive Summary ja tehniline PDF-raport

## Metoodiline märkus

Analüüs teostatakse süsteemi kloonil vastavalt **ISO 27037** standardile.
