#!/usr/bin/env python3
"""
valvurMASTER.py - VALVUR projekti keskne juhtskript.
Kõik skriptid asuvad samas kaustas.
"""

import subprocess
import os
import sys

# ASCII Logo (VALVUR standard)
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
#   |   FAILI NIMI:  valvurMASTER.py                                      |   #
#   |   LOODUD:      27.03.2026                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Keskne mootor, mis käivitab etapid 01-05.            |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def run_step(script_name, args=None):
    """Käivitab samas kaustas asuva skripti."""
    # Kuna kõik on ühes kaustas, siis tee on lihtsalt faili nimi
    script_path = script_name
    
    if not os.path.exists(script_path):
        print(f"\n[!] VIGA: Faili '{script_path}' ei leitud!")
        return False

    print(f"\n[>>>] KÄIVITAN: {script_name}...")
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    try:
        subprocess.run(cmd, check=True)
        print(f"[+] ETAPP {script_name} edukalt läbitud.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] VIGA: Skript {script_name} ebaõnnestus.")
        return False

def main():
    print(LOGO)

    # Kontrollime, et andmete kaustad oleksid olemas (eeldame, et need on taseme võrra kõrgemal)
    # Kui sul on kõik ühes suures kaustas, siis võid need punktid eemaldada
    for folder in ["../LOGID", "../TULEMUSED"]:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    print("\n--- VALVUR ANALÜÜSI AHELA KÄIVITAMINE ---")

    # 1. ETAPP: Konverteerimine
    # Märkus: Kasutame "../LOGID", et skript leiaks failid väljastpoolt skriptide kausta
    if not run_step("01_konverteering_evtx_csv.py", ["--path", "../LOGID"]): return

    # 2. ETAPP: Filtreerimine
    if not run_step("02_turvafiltreering.py"): return

    # 3. ETAPP: Märksõnad
    if not run_step("03_otsing_marksonade_jargi.py"): return

    # 4. ETAPP: PowerShell dekodeerimine
    if not run_step("04_powershell_dekodeerimine.py"): return

    # 5. ETAPP: Raport (Nimi täpselt nagu pildil!)
    if not run_step("05_genereeriRAPORT.py"): return

    print("\n" + "="*80)
    print(" KOGU ANALÜÜS ON EDUKALT LÕPETATUD! ")
    print(" Raport: ../TULEMUSED/VALVUR_LOPLIK_RAPORT.docx")
    print("="*80)

if __name__ == "__main__":
    main()
