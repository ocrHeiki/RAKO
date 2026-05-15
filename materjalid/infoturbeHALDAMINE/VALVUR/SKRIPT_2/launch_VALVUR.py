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

def check_command(cmd):
    return shutil.which(cmd) is not None

def main():
    print("[*] VALVUR BOOTSTRAP ALUSTAB...")

    # 1. Kontrolli git
    if not check_command("git"):
        print("[!] VIGA: Git pole paigaldatud.")
        print("    Paigaldamiseks: sudo apt install git")
        sys.exit(1)

    # 2. Ajutise kausta loomine
    work_dir = os.path.join(tempfile.gettempdir(), "VALVUR_LIVE")
    if os.path.exists(work_dir): shutil.rmtree(work_dir)
    os.makedirs(work_dir)
    os.chdir(work_dir)

    # 3. Kloonimine
    print(f"[*] Kloonitakse repositoorium: {REPO_URL}")
    subprocess.run(["git", "clone", REPO_URL, "."], check=True)
    os.chdir(SUBDIR)

    # 4. Virtuaalkeskkonna loomine
    print("[*] Luuakse isoleeritud virtuaalkeskkond (venv)...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    if os.name == "nt":
        python_exe = os.path.join("venv", "Scripts", "python.exe")
    else:
        python_exe = os.path.join("venv", "bin", "python")

    # 5. Sõltuvuste paigaldamine
    print("[*] Paigaldatakse sõltuvused...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([python_exe, "-m", "pip", "install", "python-evtx", "python-docx", "rich", "psutil", "fpdf2"], check=True)

    # 6. Käivitamine (kasutab SKRIPT_2 versiooni)
    print("\n" + "="*60)
    print("   VALVUR KÄIVITUB VIRTUAALKESKKONNAS")
    print("="*60 + "\n")
    subprocess.run([python_exe, "SKRIPT_2/valvurMASTER.py"])

if __name__ == "__main__":
    main()
