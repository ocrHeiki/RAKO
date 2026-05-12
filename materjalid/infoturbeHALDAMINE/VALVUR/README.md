# VALVUR - Intsidendi süvaanalüüsi ja auditeerimise tööriist

VALVUR on võimas platvormiülene (Windows & Linux) tööriistakomplekt digitaalseks ekspertiisiks, logide süvaanalüüsiks ja süsteemseks turvaauditiks (E-ITS).

## Põhivõimekused

- **Platvormiülene logianalüüs**: Toetab nii Windowsi `.evtx` kui ka Linuxi süsteemiloge (`auth.log`, `syslog`).
- **Süvaanalüüs (Deep Forensics)**: PowerShell Base64 ja XOR dekodeerimine, IP-aadresside ja ründeindikaatorite (IOC) tuvastamine.
- **Live System Scan**: Reaalajas kontroll kahtlastele failidele (`.exe`, `.ps1`, `.sh`, `.php`) ajutistes kaustades.
- **Võrgu skaneerimine**: Automaatne hostide ja teenuste tuvastamine (nmap) võrgujoonise koostamiseks.
- **E-ITS Turvaaudit & GPO seire**: Süsteemi seadete ja Group Policy muudatuste kontroll.
- **Professionaalne raporteerimine**: Genereerib detailse `.docx` tööraporti ja tehnilise `.pdf` ülevaate.

## Kasutamine

VALVUR on loodud töötama kõikjal - mälupulgal, välisel kettal või süsteemselt.

1. Aseta logifailid kausta `LOGID/`.
2. Käivita peaskript:
   ```bash
   python3 SKRIPTID/valvurMASTER.py
   ```
3. Tulemused ja raportid leiad kaustast `TULEMUSED/`.

## Nõuded

- Python 3.x
- Vajalikud teegid: `pip install evtx python-docx fpdf`
- Süsteemne tööriist: `nmap` (võrgu skaneerimiseks)

## Autor
**Heiki Rebane**
VALVUR Projekt 2026
