#!/usr/bin/env python3
"""
valvurMASTER.py - VALVUR projekti keskne juhtskript.
Versioon 2.0 - Platvormiülene (Windows/Linux) & E-ITS Audit.
"""

import subprocess
import os
import sys
import platform
import socket

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
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   FUNKTSIOON:  Windows & Linux analüüs + E-ITS Audit                |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

# Dünaamiline tee leidmine - VALVUR leiab end üles igalt kettalt
# __file__ on skriptide kaustas, seega base_dir on üks tase kõrgemal
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKRIPTID_DIR = os.path.join(BASE_DIR, "SKRIPTID")
TULEMUSED_DIR = os.path.join(BASE_DIR, "TULEMUSED")

def run_step(script_name, args=None):
    """Käivitab skripti ja tagab, et see leiaks oma asukoha."""
    script_path = os.path.join(SKRIPTID_DIR, script_name)
    
    if not os.path.exists(script_path):
        print(f"\n[!] VIGA: Faili '{script_path}' ei leitud!")
        return False

    print(f"\n[>>>] KÄIVITAN: {script_name}...")
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    try:
        # Käivitame skripti BASE_DIR töökaustas
        subprocess.run(cmd, check=True, cwd=BASE_DIR)
        print(f"[+] ETAPP {script_name} edukalt läbitud.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] VIGA: Skript {script_name} ebaõnnestus.")
        return False

def main():
    print(LOGO)
    os_type = platform.system()
    hostname = socket.gethostname()
    print(f"SÜSTEEM: {os_type} | MASIN: {hostname} | ASUKOHT: {BASE_DIR}")

    if not os.path.exists(TULEMUSED_DIR):
        os.makedirs(TULEMUSED_DIR, exist_ok=True)

    print("\n--- VALVUR ANALÜÜSI AHELA KÄIVITAMINE ---")

    # 0. ETAPP: Terviklus (Hashing)
    if not run_step("00_terviklus_kontroll.py"): return

    # 1. ETAPP: Logide kogumine/konverteerimine
    if os_type == "Windows":
        if not run_step("01_konverteering_evtx_csv.py", ["--path", "LOGID"]): return
    else:
        if not run_step("01_linux_logid_csv.py"): return

    # 2. ETAPP: Analüüs
    run_step("02_turvafiltreering.py")
    run_step("03_otsing_marksonade_jargi.py")
    run_step("04_powershell_dekodeerimine.py")
    run_step("09_threat_intel.py")
    
    # 3. ETAPP: Süsteemi Live-kontroll (kahtlased failid)
    run_step("06_kahtlased_failid.py")
    
    # 4. ETAPP: E-ITS Turvaaudit
    run_step("07_turvaaudit.py")

    # 5. ETAPP: Võrgu skaneerimine (Võrgujoonise ja hostide jaoks)
    run_step("10_vorgu_skaneerimine.py")
    run_step("11_kasutajate_nimekiri.py")

    # 6. ETAPP: Raporteerimine
    run_step("05_genereeriRAPORT.py")
    run_step("08_tehniline_raport_pdf.py")

    print("\n" + "="*80)
    print(" KOGU ANALÜÜS ON EDUKALT LÕPETATUD! ")
    print(f" Raportid asuvad kaustas: {TULEMUSED_DIR}")
    print("="*80)

if __name__ == "__main__":
    main()
