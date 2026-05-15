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
#   |   FAILI NIMI:  00_terviklus_kontroll.py                             |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Logifailide SHA-256 räside arvutamine.               |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import hashlib

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

logger = utils.setup_logging("TERVIKLUS")

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_all_logs():
    print(LOGO)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    log_dir = os.path.join(base_dir, "LOGID")
    out_dir = utils.get_output_dir()
    out_report = os.path.join(out_dir, '00_terviklus_raport.txt')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        logger.warning(f"Kausta {log_dir} ei leitud, see loodi.")
        return

    results = []
    logger.info(f"Arvutan räsid logidele asukohas: {log_dir}")

    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if file.lower().endswith(('.evtx', '.log', '.syslog')):
                full_path = os.path.join(root, file)
                try:
                    file_hash = calculate_sha256(full_path)
                    results.append(f"{file}: {file_hash}")
                    print(f"  [OK] {file}")
                except Exception as e:
                    logger.error(f"Räsi arvutamine ebaõnnestus {file}: {e}")

    if results:
        with open(out_report, 'w', encoding='utf-8') as f:
            f.write("VALVUR - LOGIDE TERVIKLUSE RAPORT (SHA-256)\n")
            f.write("="*60 + "\n")
            for res in results:
                f.write(res + "\n")
        logger.info(f"Tervikluse raport loodud: {out_report}")
    else:
        logger.warning("Ühtegi logifaili ei leitud.")

if __name__ == "__main__":
    check_all_logs()
