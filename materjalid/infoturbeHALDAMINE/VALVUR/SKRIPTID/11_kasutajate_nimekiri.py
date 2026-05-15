#!/usr/bin/env python3
LOGO = """
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
#   |   FAILI NIMI:  11_kasutajate_nimekiri.py                            |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Süsteemi ja logide kasutajakontode audit.            |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""
11_kasutajate_nimekiri.py - Tuvastab logidest kõik unikaalsed kasutajakontod.
Aitab täita infovarade tabelit (kontod).
"""

import os
import csv

# ASCII Logo (VALVUR standard)
r

def get_linux_system_users():
    """Loeb Linuxi kasutajad otse süsteemifailist /etc/passwd."""
    system_users = set()
    if os.path.exists("/etc/passwd"):
        print("[*] Loen Linuxi süsteemseid kasutajaid (/etc/passwd)...")
        try:
            with open("/etc/passwd", "r") as f:
                for line in f:
                    parts = line.split(":")
                    if len(parts) >= 3:
                        username = parts[0]
                        uid = parts[2]
                        # Tuvastame kõik kasutajad, kellel on ROOT õigused (UID 0)
                        if uid == "0":
                            system_users.add(f"{username} (UID: 0 - ROOT PRIVILEGED)")
                        else:
                            system_users.add(username)
        except: pass
    return system_users

def extract_users(in_file='TULEMUSED/02_tulemus_turvafiltreering.csv'):
    print(LOGO)
    users = get_linux_system_users()
    
    if os.path.exists(in_file):
        print("[*] Otsin täiendavaid kasutajaid logidest...")
        try:
            with open(in_file, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    msg = row.get('Message', '')
                    if "TargetUserName:" in msg:
                        parts = msg.split("TargetUserName:")
                        if len(parts) > 1:
                            username = parts[1].split("|")[0].strip()
                            if username and username not in ["-", "SYSTEM", "NETWORK SERVICE", "LOCAL SERVICE"]:
                                users.add(username)
                    if "for user" in msg:
                        parts = msg.split("for user")
                        if len(parts) > 1:
                            username = parts[1].split()[0].strip()
                            users.add(username)
        except: pass

    out_file = 'TULEMUSED/11_tulemus_kasutajad.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("VALVUR - Tuvastatud kasutajakontod (Süsteem + Logid)\n" + "="*50 + "\n")
        for user in sorted(users):
            f.write(f"- {user}\n")
    
    print(f"[+] Kokku tuvastati {len(users)} kasutajaviidet. Nimekiri: {out_file}")

if __name__ == "__main__":
    extract_users()
