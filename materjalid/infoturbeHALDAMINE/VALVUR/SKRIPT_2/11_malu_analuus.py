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
#   |   FAILI NIMI:  11_malu_analuus.py                                   |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Volatility 3 mäluanalüüsi liides.                    |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import utils

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
###############################################################################
"""

logger = utils.setup_logging("MALU_ANALUUS")

def find_memory_dumps():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dump_dir = os.path.join(base_dir, "MALUDUMPID")
    if not os.path.exists(dump_dir):
        return []
    dumps = []
    for f in os.listdir(dump_dir):
        if f.endswith(('.raw', '.mem', '.dmp', '.vmem')):
            dumps.append(os.path.join(dump_dir, f))
    return dumps

def run_volatility(memory_file, plugin="windows.pslist"):
    try:
        result = subprocess.check_output(
            ["vol", "-f", memory_file, plugin],
            stderr=subprocess.STDOUT, timeout=60
        ).decode(errors='ignore')
        return result
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        return "[!] Aegunud - mäluanalüüs katkestati (60s piir)"
    except subprocess.CalledProcessError as e:
        return f"[!] Viga: {e.output.decode(errors='ignore')}"

def main():
    print(LOGO)
    out_dir = utils.get_output_dir()
    out_file = os.path.join(out_dir, '11_tulemus_malu_analuus.txt')
    dumps = find_memory_dumps()

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("VALVUR - MÄLUANALÜÜSI RAPORT\n" + "="*60 + "\n\n")

        if not dumps:
            f.write("Mälutõmmiseid ei leitud.\n")
            f.write("Aseta .raw/.mem/.dmp failid kausta: MALUDUMPID/\n")
            logger.warning("Mälutõmmiseid ei leitud")
            print(f"  [!] Mälutõmmiseid ei leitud. Loo kaust MALUDUMPID/ ja lisa failid sinna.")
            print(f"  [+] Tulemus: {out_file}")
            return

        for dump in dumps:
            f.write(f"\n--- Analüüsin: {os.path.basename(dump)} ---\n")
            logger.info(f"Analüüsin mälutõmmist: {dump}")
            f.write("\n[Protsessid]\n")
            output = run_volatility(dump, "windows.pslist")
            if output is None:
                f.write("Volatility 3 pole paigaldatud. Paigaldamiseks: pip install volatility3\n")
                break
            f.write(output)
    logger.info(f"Mäluanalüüs valmis: {out_file}")

if __name__ == "__main__":
    main()
