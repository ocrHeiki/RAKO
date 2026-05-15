#!/usr/bin/env python3
import os
import sys
import subprocess
import socket
from datetime import datetime

# Proovime importida rich, kui see on venv-is olemas
try:
    from rich.console import Console
    from rich.table import Table
    from rich.progress import Progress
    console = Console()
except ImportError:
    console = None

# Impordime oma uue utils mooduli
sys.path.append(os.path.join(os.path.dirname(__file__), "SKRIPTID"))
try:
    import utils
except ImportError:
    # Kui utils on mujal, kohandame teed
    sys.path.append("SKRIPTID")
    import utils

# DÜNAAMILINE ASUKOHT
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOSTNAME = socket.gethostname()
RESULT_DIR = os.path.join(BASE_DIR, "TULEMUSED", HOSTNAME)

logger = utils.setup_logging("MASTER")

def escalate_privileges():
    """Linuxis automaatne sudo taaskäivitus, kui õigusi napib (Punkt 3)."""
    if os.name != "nt" and os.getuid() != 0:
        logger.info("Privileegid puuduvad. Proovin sudo taaskäivitust...")
        args = ["sudo", sys.executable] + sys.argv
        os.execvp("sudo", args)

def run_step(script_name, critical=False, args=None):
    logger.info(f"Etapp: {script_name}")
    script_path = os.path.join(BASE_DIR, "SKRIPTID", script_name)
    
    cmd = [sys.executable, script_path]
    if args: cmd.extend(args)

    try:
        env = os.environ.copy()
        env["VALVUR_OUT"] = RESULT_DIR
        subprocess.run(cmd, check=True, cwd=BASE_DIR, env=env)
        return True
    except Exception as e:
        logger.error(f"Viga etapis {script_name}: {e}")
        if critical: sys.exit(1)
        return False

def main():
    escalate_privileges()
    utils.ensure_folders(BASE_DIR)
    
    if console:
        console.print("[bold cyan]VALVUR - PROFESSIONAALNE ANALÜÜSI PLATVORM[/bold cyan]", justify="center")
        console.print(f"Masin: [green]{HOSTNAME}[/green] | Kaust: {RESULT_DIR}")
        print("="*80)
    else:
        logger.info(f"VALVUR START - Masin: {HOSTNAME}")

    # KRIITILISED ETAPID
    run_step("00_terviklus_kontroll.py", critical=True)
    
    # 01_konverteering toetab nüüd --live argumenti
    run_step("01_konverteering_evtx_csv.py", critical=True, args=["--live"] if os.name == "nt" else [])

    # ANALÜÜSIMOODULID
    steps = [
        "03_turvafiltreering.py",
        "04_otsing_marksonade_jargi.py",
        "05_powershell_dekodeerimine.py",
        "06_kahtlased_failid.py",
        "07_turvaaudit.py",
        "08_genereeriRAPORT.py",
        "09_tehniline_raport_pdf.py",
        "10_threat_intel.py",
        "11_vorgu_skaneerimine.py",
        "12_kasutajate_nimekiri.py",
        "13_malu_analuus.py",
        "14_koond_ajajoon.py",
        "15_linux_syvaanaluus.py"
    ]

    if console:
        with Progress() as progress:
            task = progress.add_task("[cyan]Analüüsin...", total=len(steps))
            for step in steps:
                run_step(step)
                progress.update(task, advance=1)
    else:
        for step in steps: run_step(step)

    run_step("08_genereeriRAPORT.py")
    logger.info("ANALÜÜS LÕPETATUD.")

if __name__ == "__main__":
    main()
