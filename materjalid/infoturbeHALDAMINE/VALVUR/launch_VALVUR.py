#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import tempfile

REPO_URL = "https://github.com/ocrHeiki/VALVUR.git"

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except:
        return False

def main():
    print("""
    #################################################################
    #                                                               #
    #   VALVUR REMOTE LAUNCHER - Kiirkäivitus GitHubist             #
    #                                                               #
    #################################################################
    """)

    # 1. Loome ajutise töökeskkonna
    tmp_dir = os.path.join(tempfile.gettempdir(), "VALVUR_EXAM")
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)
    
    print(f"[*] Luuakse ajutine keskkond: {tmp_dir}")
    os.makedirs(tmp_dir)
    os.chdir(tmp_dir)

    # 2. Kloonime repositooriumi
    print(f"[*] Kloonitakse VALVUR GitHubist ({REPO_URL})...")
    if not run_cmd(f"git clone {REPO_URL} ."):
        print("[!] VIGA: Giti kloonimine ebaõnnestus. Kontrolli internetiühendust.")
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
