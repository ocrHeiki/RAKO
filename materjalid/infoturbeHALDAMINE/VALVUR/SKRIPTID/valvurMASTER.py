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
#   |   FAILI NIMI:  valvurMASTER.py                                      |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   VALVUR-i peamootor ja kontrollmoodul.                |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import subprocess
import socket
from datetime import datetime

# Impordime utils
sys.path.append(os.path.join(os.path.dirname(__file__), "SKRIPTID"))
try:
    import utils
except ImportError:
    sys.path.append("SKRIPTID")
    import utils

# DÜNAAMILINE ASUKOHT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTNAME = socket.gethostname()
RESULT_DIR = os.path.join(BASE_DIR, "TULEMUSED", HOSTNAME)

logger = utils.setup_logging("MASTER")

def escalate_privileges():
    if os.name != "nt" and os.getuid() != 0:
        logger.info("Privileegid puuduvad. Proovin sudo taaskäivitust...")
        args = ["sudo", sys.executable] + sys.argv
        os.execvp("sudo", args)

def run_step(script_name, critical=False, args=None):
    logger.info(f"KÄIVITAN: {script_name}")
    script_path = os.path.join(BASE_DIR, "SKRIPTID", script_name)
    
    if not os.path.exists(script_path):
        logger.error(f"Skripti {script_name} ei leitud!")
        if critical: sys.exit(1)
        return False

    cmd = [sys.executable, script_path]
    if args: cmd.extend(args)

    try:
        env = os.environ.copy()
        env["VALVUR_OUT"] = RESULT_DIR
        subprocess.run(cmd, check=True, cwd=BASE_DIR, env=env)
        return True
    except Exception as e:
        logger.error(f"Viga: {e}")
        if critical: sys.exit(1)
        return False

def main():
    escalate_privileges()
    utils.ensure_folders(BASE_DIR)
    os.makedirs(RESULT_DIR, exist_ok=True)
    
    logger.info(f"VALVUR START - Masin: {HOSTNAME}")

    # 1. KRIITILISED ETAPID
    run_step("00_terviklus_kontroll.py", critical=True)
    
    if os.name == "nt":
        run_step("01_konverteering_evtx_csv.py", critical=True, args=["--live"])
    else:
        run_step("02_linux_logid_csv.py", critical=True)

    # 2. ANALÜÜSIMOODULID (Järjekord on oluline!)
    steps = [
        "03_turvafiltreering.py",
        "04_otsing_marksonade_jargi.py",
        "05_powershell_dekodeerimine.py",
        "06_kahtlased_failid.py",
        "07_vorgu_skaneerimine.py",
        "08_kasutajate_nimekiri.py",
        "09_turvaaudit.py",
        "10_threat_intel.py",
        "11_malu_analuus.py",
        "12_linux_syvaanaluus.py",
        "13_koond_ajajoon.py"
    ]

    for step in steps:
        run_step(step)

    # 3. LÕPPVIIMISTLUS
    run_step("14_genereeriRAPORT.py")
    run_step("15_tehniline_raport_pdf.py")

    # Lõpukontroll
    if not os.listdir(RESULT_DIR):
        logger.error("HOIATUS: Ühtegi tulemust ei loodud! Kontrolli sisendlogisid.")
    else:
        logger.info(f"ANALÜÜS LÕPETATUD. Tulemused: {RESULT_DIR}")

if __name__ == "__main__":
    main()
