#!/usr/bin/env python3
"""
11_kasutajate_nimekiri.py - Tuvastab logidest kõik unikaalsed kasutajakontod.
Aitab täita infovarade tabelit (kontod).
"""

import os
import csv

# ASCII Logo (VALVUR standard)
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
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Kasutajate Tuvastus                         |   #
#   |   FAILI NIMI:  11_kasutajate_nimekiri.py                             |   #
#   |   KIRJELDUS:   Logidest leitud kasutajakontode koondamine.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def extract_users(in_file='TULEMUSED/02_tulemus_turvafiltreering.csv'):
    print(LOGO)
    if not os.path.exists(in_file):
        print("Filtreeritud logisid ei leitud.")
        return

    users = set()
    print("[*] Otsin kasutajakontosid...")
    
    try:
        with open(in_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg = row.get('Message', '')
                # Otsime tüüpilisi kasutajatunnuseid Windowsi logist (TargetUserName: nimi)
                if "TargetUserName:" in msg:
                    parts = msg.split("TargetUserName:")
                    if len(parts) > 1:
                        username = parts[1].split("|")[0].strip()
                        if username and username not in ["-", "SYSTEM", "NETWORK SERVICE", "LOCAL SERVICE"]:
                            users.add(username)
                
                # Otsime Linuxi logist (user nimi)
                if "for user" in msg:
                    parts = msg.split("for user")
                    if len(parts) > 1:
                        username = parts[1].split()[0].strip()
                        users.add(username)

        out_file = 'TULEMUSED/11_tulemus_kasutajad.txt'
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write("VALVUR - Tuvastatud kasutajakontod\n" + "="*40 + "\n")
            for user in sorted(users):
                f.write(f"- {user}\n")
        
        print(f"[+] Leiti {len(users)} unikaalset kasutajat. Nimekiri: {out_file}")
    except Exception as e:
        print(f"VIGA: {e}")

if __name__ == "__main__":
    extract_users()
