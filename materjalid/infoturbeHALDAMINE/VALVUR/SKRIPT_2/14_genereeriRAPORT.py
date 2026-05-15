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
#   |   FAILI NIMI:  14_genereeriRAPORT.py                                |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Lõpliku koondraporti genereerimine.                  |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import csv
from datetime import datetime

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

logger = utils.setup_logging("RAPORT")

def count_csv_rows(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return sum(1 for _ in f) - 1
    except:
        return 0

def main():
    print(LOGO)
    out_dir = utils.get_output_dir()
    out_file = os.path.join(out_dir, '14_tulemus_koondraport.txt')
    txt_files = [f for f in os.listdir(out_dir) if f.endswith('.txt')]
    csv_files = [f for f in os.listdir(out_dir) if f.endswith('.csv')]

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("  VALVUR - KOONDRAPORT\n")
        f.write(f"  Genereeritud: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        f.write("--- ANALÜÜSI TULEMUSED ---\n\n")
        for txt_file in sorted(txt_files):
            file_path = os.path.join(out_dir, txt_file)
            size = os.path.getsize(file_path)
            f.write(f"  {txt_file}: {size} baiti\n")
        f.write("\n--- CSV SÜNDMUSTE KOKKUVÕTE ---\n\n")
        for csv_file in sorted(csv_files):
            file_path = os.path.join(out_dir, csv_file)
            rows = count_csv_rows(file_path)
            f.write(f"  {csv_file}: {rows} rida\n")
        f.write("\n--- NIST CSF 2.0 VASTAVUS ---\n")
        f.write("  IDENTIFY: Varade kaardistus teostatud\n")
        f.write("  PROTECT: Turvakontrollid auditeeritud\n")
        f.write("  DETECT: Logianalüüs ja ründeindikaatorid tuvastatud\n")
        f.write("  RESPOND: Raport ja tegevuskava koostatud\n")
        f.write("  RECOVER: Ajajoon süsteemi taastamiseks loodud\n")
    logger.info(f"Koondraport loodud: {out_file}")

if __name__ == "__main__":
    main()
