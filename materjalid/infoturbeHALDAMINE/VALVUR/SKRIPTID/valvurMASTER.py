#!/usr/bin/env python3
"""
valvurMASTER.py - VALVUR projekti keskne juhtskript.
See skript koordineerib kogu analüüsi ahelat (etapid 01 kuni 05).
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
#   |   KIRJELDUS:   Keskne mootor, mis käivitab analüüsi etapid 01-05.   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def run_step(script_name, args=None):
    """
    Abifunktsioon teiste Pythoni skriptide käivitamiseks.
    Kasutab subprocess moodulit, mis on Pythoni standardviis väliste protsesside juhtimiseks.
    """
    script_path = os.path.join("SKRIPTID", script_name)
    
    if not os.path.exists(script_path):
        print(f"\n[!] VIGA: Faili '{script_path}' ei leitud!")
        return False

    print(f"\n[>>>] KÄIVITAN: {script_name}...")
    
    # Moodustame käsu nimekirjana: [python3, skripti_tee, argumendid...]
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    try:
        # subprocess.run ootab, kuni skript lõpetab. check=True viskab vea, kui skript ebaõnnestub.
        subprocess.run(cmd, check=True)
        print(f"[+] ETAPP {script_name} edukalt läbitud.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] VIGA: Skript {script_name} lõpetas veakoodiga {e.returncode}.")
        return False
    except Exception as e:
        print(f"[!] OOTAMATU VIGA: {str(e)}")
        return False

def main():
    """Peamine töövoo loogika."""
    print(LOGO)

    # Kontrollime kaustade olemasolu (vajalik Pythoni algajale: alati veendu, et keskkond on valmis)
    folders = ["LOGID", "SKRIPTID", "TULEMUSED"]
    for folder in folders:
        if not os.path.exists(folder):
            print(f"[*] Loon puuduva kausta: {folder}")
            os.makedirs(folder)

    print("\n--- VALVUR ANALÜÜSI AHELA ALUSTAMINE ---")

    # 1. ETAPP: .evtx konverteerimine CSV-ks
    if not run_step("01_konverteering_evtx_csv.py", ["--path", "LOGID"]):
        print("\n[!] Analüüs seiskus etapis 01.")
        return

    # 2. ETAPP: Kriitiliste sündmuste filtreerimine
    if not run_step("02_turvafiltreering.py"):
        print("\n[!] Analüüs seiskus etapis 02.")
        return

    # 3. ETAPP: Kahtlaste märksõnade otsing
    if not run_step("03_otsing_marksonade_jargi.py"):
        print("\n[!] Analüüs seiskus etapis 03.")
        return

    # 4. ETAPP: PowerShell süvaanalüüs ja Base64 dekodeerimine
    if not run_step("04_powershell_dekodeerimine.py"):
        print("\n[!] Analüüs seiskus etapis 04.")
        return

    # 5. ETAPP: Lõpliku Wordi raporti genereerimine (Eesti ajavööndis)
    if not run_step("05_genereeri_raport.py"):
        print("\n[!] Analüüs seiskus etapis 05.")
        return

    print("\n" + "="*80)
    print(" KOGU ANALÜÜS ON EDUKALT LÕPETATUD! ")
    print(" Lõplik raport asub: TULEMUSED/VALVUR_LOPLIK_RAPORT.docx")
    print("="*80)

if __name__ == "__main__":
    # See rida tagab, et skript käivitub ainult otse jooksutades, mitte teise skripti poolt importides.
    main()
