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
#   |   FAILI NIMI:  00_terviklus_kontroll.py                             |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Logifailide SHA-256 räside arvutamine.               |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""
"""
00_terviklus_kontroll.py - Arvutab algallika logide räsid (Data Integrity).
Tagab, et tõendusmaterjali pole analüüsi käigus muudetud.
"""

import os
import hashlib


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def check_all_logs(log_dir='LOGID', out_report='TULEMUSED/00_terviklus_raport.txt'):
    print(LOGO)
    if not os.path.exists(log_dir):
        print(f"[!] VIGA: Kausta {log_dir} ei leitud.")
        return

    results = []
    print(f"[*] Arvutan räsid logidele asukohas: {log_dir}")
    
    for root, dirs, files in os.walk(log_dir):
        for file in files:
            if file.lower().endswith(('.evtx', '.log', '.syslog')):
                full_path = os.path.join(root, file)
                file_hash = calculate_sha256(full_path)
                results.append(f"{file}: {file_hash}")
                print(f"  [OK] {file}")

    if results:
        with open(out_report, 'w', encoding='utf-8') as f:
            f.write("VALVUR - LOGIDE TERVIKLUSE RAPORT (SHA-256)\n")
            f.write("="*60 + "\n")
            for res in results:
                f.write(res + "\n")
        print(f"\n[+] Tervikluse raport loodud: {out_report}")
    else:
        print("[!] Hoiatus: Ühtegi logifaili ei leitud.")

if __name__ == "__main__":
    check_all_logs()
