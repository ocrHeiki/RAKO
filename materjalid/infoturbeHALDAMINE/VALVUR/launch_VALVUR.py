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
#   |   KIRJELDUS:   Süsteemi kiirkäivitus virtuaalkeskkonnas (venv).     |   #
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

def main():
    print("[*] VALVUR BOOTSTRAP ALUSTAB...")
    
    # 1. Ajutise kausta loomine
    work_dir = os.path.join(tempfile.gettempdir(), "VALVUR_LIVE")
    if os.path.exists(work_dir): shutil.rmtree(work_dir)
    os.makedirs(work_dir)
    os.chdir(work_dir)

    # 2. Kloonimine
    print(f"[*] Kloonitakse repositoorium: {REPO_URL}")
    subprocess.run(["git", "clone", REPO_URL, "."], check=True)
    os.chdir(SUBDIR)

    # 3. Virtuaalkeskkonna loomine (Punkt 3)
    print("[*] Luuakse isoleeritud virtuaalkeskkond (venv)...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Määrame venv interpretaatori tee
    if os.name == "nt":
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join("venv", "bin", "python")

    # 4. Sõltuvuste paigaldamine
    print("[*] Paigaldatakse sõltuvused ja Rich UI...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([python_exe, "-m", "pip", "install", "python-evtx", "python-docx", "rich", "psutil"], check=True)

    # 5. Käivitamine
    print("\n" + "="*60)
    print("   VALVUR KÄIVITUB VIRTUAALKESKKONNAS")
    print("="*60 + "\n")
    subprocess.run([python_exe, "SKRIPTID/valvurMASTER.py"])

if __name__ == "__main__":
    main()
