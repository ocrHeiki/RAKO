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
#   |   FAILI NIMI:  10_vorgu_skaneerimine.py                      |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Võrguvarade ja teenuste kaardistamine.        |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

10_vorgu_skaneerimine.py - Teostab võrgu skaneerimist (nmap) infovarade kaardistamiseks.
"""

import os
import subprocess
import platform
import csv

# ASCII Logo (VALVUR standard)
r

def check_nmap():
    """Kontrollib, kas nmap on süsteemis olemas."""
    try:
        subprocess.check_output(["nmap", "--version"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_local_subnet():
    """Proovib tuvastada kohaliku alamvõrgu."""
    if platform.system() == "Linux":
        try:
            route_out = subprocess.check_output(["ip", "route", "show"]).decode()
            for line in route_out.splitlines():
                if "default" not in line and "link" in line:
                    return line.split()[0]
        except: pass
    return "192.168.1.0/24" # Default fallback

def run_nmap_scan(target=None):
    print(LOGO)
    if not check_nmap():
        print("[!] VIGA: 'nmap' ei ole paigaldatud. Kasuta: sudo apt install nmap")
        return

    if not target:
        target = get_local_subnet()

    print(f"[*] Alustan võrgu skaneerimist: {target}")
    # -sn (Ping scan) on kiire ja tuvastab hostid ilma portideta
    # Kui soovid põhjalikumalt, kasuta -F (Fast mode) või -p 80,443,445,3389
    try:
        # Kasutame XML väljundit, et seda oleks lihtsam parssida või tekstiväljundit kiireks ülevaateks
        cmd = ["nmap", "-sn", target]
        result = subprocess.check_output(cmd).decode()
        
        out_file = "TULEMUSED/10_tulemus_vorgu_skaneerimine.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result)
        
        print(f"[+] Skaneerimine lõpetatud. Tulemused: {out_file}")
        
        # Proovime leida unikaalsed IP-d ja nimed lühidalt
        found_hosts = []
        for line in result.splitlines():
            if "Nmap scan report for" in line:
                host_info = line.replace("Nmap scan report for ", "").strip()
                found_hosts.append(host_info)
                print(f"  [+] Leiti host: {host_info}")
                
        return found_hosts
    except Exception as e:
        print(f"[!] Skaneerimine ebaõnnestus: {e}")
        return []

if __name__ == "__main__":
    run_nmap_scan()
