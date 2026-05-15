#!/usr/bin/env python3
"""
###############################################################################
#   VALVUR MASTER CONTROL - Sünkroniseeritud Töövoog                          #
###############################################################################
"""
import os
import sys
import subprocess
import socket
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import utils

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTNAME = socket.gethostname()
RESULT_DIR = os.path.join(BASE_DIR, "TULEMUSED", HOSTNAME)

logger = utils.setup_logging("MASTER")

def run_step(script_name, critical=False, args=None):
    logger.info(f"===> KÄIVITAN: {script_name}")
    script_path = os.path.join(BASE_DIR, "SKRIPTID", script_name)
    if not os.path.exists(script_path):
        logger.error(f"FAILI EI LEITUD: {script_path}")
        if critical: sys.exit(1)
        return False

    env = os.environ.copy()
    env["VALVUR_OUT"] = RESULT_DIR
    try:
        subprocess.run([sys.executable, script_path] + (args or []), check=True, env=env)
        return True
    except Exception as e:
        logger.error(f"VIGA ETAPIS {script_name}: {e}")
        if critical: sys.exit(1)
        return False

if __name__ == "__main__":
    utils.ensure_folders(BASE_DIR)
    os.makedirs(RESULT_DIR, exist_ok=True)
    
    # 1. ETAPP: ANDMETE HANKIMINE (KRIITILINE)
    run_step("00_terviklus_kontroll.py", critical=True)
    if os.name == "nt":
        run_step("01_konverteering_evtx_csv.py", critical=True, args=["--live"])
    else:
        run_step("02_linux_logid_csv.py", critical=True)

    # 2. ETAPP: ANALÜÜS (JÄRJEKORD ON KRIITILINE)
    steps = [
        "03_turvafiltreering.py",      # Tekitab: filtered_events.csv
        "04_otsing_marksonade_jargi.py", # Tekitab: threat_findings.csv
        "05_powershell_dekodeerimine.py", # Tekitab: decoded_payloads.txt
        "06_kahtlased_failid.py",
        "07_vorgu_skaneerimine.py",
        "08_kasutajate_nimekiri.py",
        "09_turvaaudit.py",
        "10_threat_intel.py",
        "11_malu_analuus.py",
        "12_linux_syvaanaluus.py",
        "13_koond_ajajoon.py"          # Timeline koondab kõik CSV-d
    ]

    for step in steps:
        run_step(step)

    # 3. ETAPP: RAPORTEERIMINE
    run_step("14_genereeriRAPORT.py")
    run_step("15_tehniline_raport_pdf.py")

    logger.info(f"KÕIK VALMIS. Tulemused: {RESULT_DIR}")
