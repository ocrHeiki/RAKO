#!/usr/bin/env python3
"""
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
#   |   PROJEKT:     VALVUR - Remote Launcher                             |   #
#   |   FAILI NIMI:  launch_VALVUR.py                                     |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Süsteemi kiirkäivitus ja keskkonna ettevalmistus.    |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

"""
import os
import sys
import subprocess
import shutil
import tempfile

REPO_URL = "https://github.com/ocrHeiki/RAKO.git"
SUBDIR = "materjalid/infoturbeHALDAMINE/VALVUR"

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except:
        return False

def main():
    print("[*] VALVUR REMOTE LAUNCHER ALUSTAB...")

    # 1. Loome ajutise töökeskkonna
    tmp_dir = os.path.join(tempfile.gettempdir(), "VALVUR_EXAM")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    
    print(f"[*] Luuakse ajutine keskkond: {tmp_dir}")
    os.makedirs(tmp_dir)
    os.chdir(tmp_dir)

    # 2. Kloonime repositooriumi
    print(f"[*] Kloonitakse RAKO repositoorium ({REPO_URL})...")
    if not run_cmd(f"git clone {REPO_URL} ."):
        print("[!] VIGA: Giti kloonimine ebaõnnestus.")
        sys.exit(1)

    # Liigume VALVUR-i alamkataloogi
    if os.path.exists(SUBDIR):
        print(f"[*] Liigun projekti kausta: {SUBDIR}")
        os.chdir(SUBDIR)
    else:
        print(f"[!] VIGA: Alamkataloogi {SUBDIR} ei leitud!")
        sys.exit(1)

    # 3. Kontrollime ja installeerime sõltuvused
    print("[*] Kontrollin vajalikke Pythoni teeke...")
    run_cmd("pip install python-evtx python-docx python-pptx fpdf --user")

    # 4. Käivitame MASTER-skripti
    master_script = "SKRIPTID/valvurMASTER.py"
    if os.path.exists(master_script):
        print("
" + "="*60)
        print("   KÄIVITAN VALVUR MASTER CONTROL...")
        print("="*60 + "
")
        subprocess.run([sys.executable, master_script])
    else:
        print(f"[!] VIGA: Master skripti ({master_script}) ei leitud!")

if __name__ == "__main__":
    main()