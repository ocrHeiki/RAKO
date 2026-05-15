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
#   |   FAILI NIMI:  07_vorgu_skaneerimine.py                             |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Kohaliku võrgu skaneerimine aktiivsete seadmete jaoks|   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import subprocess
import sys

def run_nmap_scan():
    out_dir = os.environ.get("VALVUR_OUT", "TULEMUSED")
    out_file = os.path.join(out_dir, "07_tulemus_vorgu_skaneerimine.txt")
    
    print(f"[*] VALVUR - Alustan võrgu skaneerimist...")
    
    # Nmap kontroll
    try:
        # Skaneerime tavalist sisevõrku (eeldame /24)
        # Reaalses olukorras tuvastatakse subnet dünaamiliselt
        cmd = ["nmap", "-sn", "192.168.1.0/24"]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
        
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"[OK] Võrgu leiud salvestatud: {out_file}")
    except FileNotFoundError:
        print("[!] VIGA: 'nmap' ei ole installitud. Jätkan...")
    except Exception as e:
        print(f"[!] VIGA skaneerimisel: {e}")

if __name__ == "__main__":
    run_nmap_scan()
