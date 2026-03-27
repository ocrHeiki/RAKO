#!/usr/bin/env python3
"""
valvur_master.py - VALVUR projekti keskne juhtskript.
See skript koordineerib kogu analüüsi ahelat, käivitades alam-skripte õiges järjekorras.
"""

import subprocess
import os
import sys

# ASCII Logo ja metainfo definitsioon (VALVUR standard)
LOGO = r"""
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
#   |   FAILI NIMI:  valvurMASTER.py                                     |   #
#   |   LOODUD:      27.03.2026                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Keskne mootor, mis käivitab analüüsi etapid 01-04.   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def run_step(script_name, args=None):
    """Abifunktsioon Pythoni alam-skriptide käivitamiseks."""
    script_path = os.path.join("SKRIPTID", script_name)
    
    if not os.path.exists(script_path):
        print(f"\n[!] VIGA: Skripti {script_path} ei leitud!")
        return False

    print(f"\n[>>>] ETAPP: {script_name} käivitamine...")
    
    # sys.executable tagab, et kasutatakse sama Pythoni interpretaatorit
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    try:
        # Käivitame skripti ja ootame, kuni see lõpetab
        subprocess.run(cmd, check=True)
        print(f"[+] ETAPP {script_name} lõpetatud edukalt.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] VIGA: Skript {script_name} ebaõnnestus koodiga {e.returncode}")
        return False
    except Exception as e:
        print(f"[!] OOTAMATU VIGA: {e}")
        return False

def main():
    """Peamine töövoog."""
    print(LOGO)
    
    # Kontrollime vajalike kaustade olemasolu
    for folder in ["LOGID", "SKRIPTID", "TULEMUSED"]:
        if not os.path.exists(folder):
            print(f"[*] Loon puuduva kausta: {folder}")
            os.makedirs(folder)

    print("\n--- ANALÜÜSI AHELA KÄIVITAMINE ---")

    # 1. SAMM: Konverteerimine (.evtx -> .csv)
    if not run_step("01_konverteering_evtx_csv.py", ["--path", "LOGID"]):
        print("\n[!] Analüüs katkestati esimeses etapis.")
        return

    # 2. SAMM: Turvafiltreering (Kriitilised sündmused)
    if not run_step("02_turvafiltreering.py"):
        print("\n[!] Analüüs katkestati teises etapis.")
        return

    # 3. SAMM: Märksõnaotsing (Tööriistad ja käsud)
    if not run_step("03_otsing_marksonade_jargi.py"):
        print("\n[!] Analüüs katkestati kolmandas etapis.")
        return

    # 4. SAMM: Süvaanalüüs ja Dekodeerimine (Base64 / PowerShell)
    if not run_step("04_powershell_dekodeerimine.py"):
        print("\n[!] Analüüs katkestati neljandas etapis.")
        return

    print("\n" + "="*80)
    print(" KOGU VALVUR ANALÜÜS ON EDUKALT LÕPETATUD! ")
    print(" Kõik raportid ja koondfailid asuvad kaustas: TULEMUSED/")
    print("="*80)

if __name__ == "__main__":
    main()
