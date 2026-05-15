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
#   |   FAILI NIMI:  08_kasutajate_nimekiri.py                            |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Süsteemi ja logide kasutajakontode audit.            |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import csv

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

logger = utils.setup_logging("KASUTAJAD")

def extract_users():
    print(LOGO)
    out_dir = utils.get_output_dir()
    users = set()
    in_file = os.path.join(out_dir, '03_tulemus_turvafiltreering.csv')
    if os.path.exists(in_file):
        try:
            with open(in_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    msg = row.get('Message', '')
                    if "TargetUserName:" in msg: users.add(msg.split("TargetUserName:")[1].split("|")[0].strip())
        except Exception as e:
            logger.error(f"CSV lugemisel viga: {e}")
    if os.path.exists("/etc/passwd"):
        try:
            with open("/etc/passwd", "r") as f:
                for line in f: users.add(line.split(":")[0])
        except Exception as e:
            logger.error(f"/etc/passwd lugemisel viga: {e}")
    out_file = os.path.join(out_dir, '08_tulemus_kasutajad.txt')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("VALVUR - TUVASATUD KASUTAJAD\n" + "="*40 + "\n")
        for u in sorted(users): f.write(f"- {u}\n")
    logger.info(f"Leiti {len(users)} kasutajat: {out_file}")

if __name__ == "__main__":
    extract_users()
