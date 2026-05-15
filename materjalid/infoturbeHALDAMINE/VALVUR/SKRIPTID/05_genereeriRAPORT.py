#!/usr/bin/env python3

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
#   |   FAILI NIMI:  05_genereeriRAPORT.py                                |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Lõpliku koondraporti genereerimine.                  |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

LOGO = r
import os
import csv
from datetime import datetime

def generate_summary():
    """Loob raporti algusesse Executive Summary koos NIST CSF maatriksiga."""
    summary = (
        "VALVUR - ANALÜÜSI KOKKUVÕTE (EXECUTIVE SUMMARY)\n"
        "==============================================\n"
        "MIS JUHTUS: Teostati Windowsi ja Linuxi süsteemilogide süvaanalüüs.\n\n"
        "NIST CSF RAAMISTIKU VASTAVUS (NIST Mapping):\n"
        "-------------------------------------------\n"
        "1. IDENTIFY (Tuvasta):  Süsteemi varade, kasutajate ja võrgu kaardistus (Skriptid 07, 10, 11).\n"
        "2. PROTECT (Kaitse):   E-ITS turvaaudit ja paroolipoliitika kontroll (Skript 07).\n"
        "3. DETECT (Tuvasta):    Logianalüüs ja kahtlaste failide/protsesside leidmine (Skriptid 02, 03, 06).\n"
        "4. RESPOND (Reageeri): Kiire intsidendi analüüs ja normaliseeritud raporteerimine.\n"
        "5. RECOVER (Taasta):   Süsteemi muudatuste (Timeline) tuvastamine taasteplaaniks.\n\n"
        "METOODIKA: Analüüs on teostatud süsteemi kloonil. Kõik algallikad on räsitud (SHA-256).\n"
        "------------------------------------------------------------------------------\n"
    )
    return summary

def get_severity(row):
    """Määra sündmusele kriitilisuse tase."""
    msg = row.get('Message', '').lower()
    if any(x in msg for x in ['mimikatz', 'psexec', 'nopasswd', 'malfind']):
        return "CRITICAL"
    if any(x in msg for x in ['failed', 'unauthorized', 'suspicious']):
        return "HIGH"
    return "MEDIUM"

def run_report_gen():
    # Kasutame keskkonnamuutujat, mille MASTER-skript määras
    out_dir = os.environ.get("VALVUR_OUT", "TULEMUSED")
    out_file = os.path.join(out_dir, "VALVUR_LOPLIK_RAPORT.txt")
    findings_file = os.path.join(out_dir, "03_tulemus_kahtlased_marksonad.csv")
    
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(generate_summary())
        
        if os.path.exists(findings_file):
            f.write("PEAMISED TURVALEIDUD (Detection Findings):\n")
            f.write(f"{'TASE':<10} | {'MITRE':<8} | {'SÜNDMUS':<50}\n")
            f.write("-" * 75 + "\n")
            
            with open(findings_file, mode='r', encoding='utf-8') as cf:
                reader = csv.DictReader(cf)
                for row in reader:
                    severity = get_severity(row)
                    mitre = row.get('MITRE_ID', 'N/A')
                    desc = row.get('Attack_Type', row.get('Message', ''))[:50]
                    f.write(f"{severity:<10} | {mitre:<8} | {desc:<50}\n")
        
        f.write("\n\nTEHNILINE DETAILRAPORT (Timeline)\n")
        f.write("=================================\n")
        # Siia saab lisada detailse ajajoone
    
    print(f"[+] Lõplik raport genereeritud: {out_file}")

if __name__ == "__main__":
    run_report_gen()
