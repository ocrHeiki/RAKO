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
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  valvurMASTER.py                               |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   VALVUR-i peamootor ja kontrollmoodul.         |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

LOGO = r
import os
import sys
import platform
import ctypes
import subprocess
import socket
from datetime import datetime

# DÜNAAMILINE ASUKOHT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "valvur_protsess.log")
HOSTNAME = socket.gethostname()
RESULT_DIR = os.path.join(BASE_DIR, "TULEMUSED", HOSTNAME)

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    print(formatted_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted_msg + "\n")

def is_admin():
    if platform.system() == "Windows":
        try: return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except: return False
    return os.getuid() == 0

def run_step(script_name, critical=False, args=None):
    log_event(f"KÄIVITAN: {script_name} (Kriitiline: {critical})")
    script_path = os.path.join(BASE_DIR, "SKRIPTID", script_name)
    
    if not os.path.exists(script_path):
        log_event(f"[!] VIGA: Skripti {script_name} ei leitud.")
        if critical: sys.exit(1)
        return False

    cmd = [sys.executable, script_path]
    if args: cmd.extend(args)

    try:
        env = os.environ.copy()
        env["VALVUR_OUT"] = RESULT_DIR
        subprocess.run(cmd, check=True, cwd=BASE_DIR, env=env)
        log_event(f"[OK] {script_name} lõpetas edukalt.")
        return True
    except subprocess.CalledProcessError as e:
        log_event(f"[!] VIGA: {script_name} ebaõnnestus (Kood: {e.returncode}).")
        if critical: sys.exit(1)
        return False

if __name__ == "__main__":
    os.makedirs(RESULT_DIR, exist_ok=True)
    
    log_event("="*60)
    log_event(f"VALVUR - ANALÜÜS KÄIVITATUD MASINAL: {HOSTNAME}")
    log_event(f"Tulemused: {RESULT_DIR}")
    log_event("Analüüs teostatud süsteemi kloonil. Algne tõendusmaterjal on puutumatu.")
    log_event("="*60)

    if not is_admin():
        log_event("[HOIATUS] Käivitatud ilma ADMIN/ROOT õigusteta. Raport tuleb puudulik.")

    # 1. ACQUISITION (Andmete hankimine)
    # Kui LOGID on tühi, proovime live-kopeerimist
    live_args = ["--live"] if platform.system() == "Windows" and not os.listdir(os.path.join(BASE_DIR, "LOGID")) else []
    
    # 2. KRIITILISED ETAPID (Järjekord: Konverteerimine/Kopeerimine -> Räsimine)
    if platform.system() == "Windows":
        run_step("01_konverteering_evtx_csv.py", critical=True, args=live_args)
    else:
        run_step("01_linux_logid_csv.py", critical=True)

    # Nüüd kui andmed on olemas (kopeeritud), arvutame räsid
    run_step("00_terviklus_kontroll.py", critical=True)

    # 3. ANALÜÜSI ETAPID
    steps = [
        "02_turvafiltreering.py", "03_otsing_marksonade_jargi.py", 
        "04_powershell_dekodeerimine.py", "06_kahtlased_failid.py", 
        "07_turvaaudit.py", "11_kasutajate_nimekiri.py", 
        "13_koond_ajajoon.py", "14_linux_syvaanaluus.py"
    ]

    for step in steps:
        run_step(step, critical=False)

    # 4. LÕPPVIIMISTLUS
    run_step("05_genereeriRAPORT.py", critical=False)

    log_event("ANALÜÜS LÕPETATUD.")
    log_event("="*60)