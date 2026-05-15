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
#   |   KIRJELDUS:   Süsteemsete ja logides esinevate kasutajate tuvastus |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import csv

def extract_users():
    out_dir = os.environ.get("VALVUR_OUT", "TULEMUSED")
    users = set()
    
    # 1. Kontrollime eelmise etapi (03) filtreeritud logisid
    in_file = os.path.join(out_dir, "03_tulemus_turvafiltreering.csv")
    if os.path.exists(in_file):
        try:
            with open(in_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    msg = row.get('Message', '')
                    if "TargetUserName:" in msg:
                        user = msg.split("TargetUserName:")[1].split("|")[0].strip()
                        if user and user not in ["-", "SYSTEM"]: users.add(user)
        except Exception as e:
            print(f"[!] Viga logide parsimisel: {e}")

    # 2. Linuxi süsteemsed kasutajad
    if os.path.exists("/etc/passwd"):
        with open("/etc/passwd", "r") as f:
            for line in f:
                users.add(line.split(":")[0])

    out_file = os.path.join(out_dir, "08_tulemus_kasutajad.txt")
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("TUVASTATUD KASUTAJAD:\n" + "="*20 + "\n")
        for u in sorted(users):
            f.write(f"- {u}\n")
    print(f"[OK] Kasutajate nimekiri loodud: {out_file}")

if __name__ == "__main__":
    extract_users()
