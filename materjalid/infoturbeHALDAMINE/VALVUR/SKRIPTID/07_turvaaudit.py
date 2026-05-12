#!/usr/bin/env python3
"""
07_turvaaudit.py - Süsteemi turvaaudit (E-ITS vastavuskontroll).
Võrdleb seadeid standardiga ja annab parandusmeetmed.
"""

import os
import platform
import subprocess

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
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  07_turvaaudit.py                                      |   #
#   |   LOODUD:      2026-05-12                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   E-ITS vastavuskontroll ja turvaaudit.                |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def check_windows():
    results = []
    print("[*] Teostan Windowsi turvaauditit...")
    
    # 1. Parooli pikkus
    try:
        out = subprocess.check_output("net accounts", shell=True).decode('cp850')
        min_len = 0
        for line in out.splitlines():
            if "Minimum password length" in line:
                min_len = int(line.split(":")[-1].strip())
        
        status = "PASS" if min_len >= 12 else "FAIL"
        results.append({
            "Kontroll": "Minimaalne parooli pikkus",
            "Hetkeseis": f"{min_len} märki",
            "Ootus": "12 märki",
            "Staatus": status,
            "Selgitus": "Liiga lühike parool on kergemini murtav brute-force ründega.",
            "Meede": "net accounts /minpwlen:12"
        })
    except: pass

    # 2. Parooli kehtivus
    results.append({
        "Kontroll": "Parooli aegumine",
        "Hetkeseis": "Tuvastamata",
        "Ootus": "90 päeva",
        "Staatus": "INFO",
        "Selgitus": "Paroole peaks regulaarselt vahetama.",
        "Meede": "net accounts /maxpwage:90"
    })
    
    return results

def check_linux():
    results = []
    print("[*] Teostan Linuxi turvaauditit...")
    
    # 1. SSH root login
    if os.path.exists("/etc/ssh/sshd_config"):
        try:
            with open("/etc/ssh/sshd_config", "r") as f:
                content = f.read()
                if "PermitRootLogin yes" in content:
                    status = "FAIL"
                else:
                    status = "PASS"
            results.append({
                "Kontroll": "SSH Root Login",
                "Hetkeseis": "Lubatud" if status == "FAIL" else "Keelatud",
                "Ootus": "Keelatud (no)",
                "Staatus": status,
                "Selgitus": "Root kasutajana sisselogimine üle SSH on turvarisk.",
                "Meede": "Muuda /etc/ssh/sshd_config: PermitRootLogin no"
            })
        except: pass

    # 2. Parooli keerukus (/etc/login.defs)
    if os.path.exists("/etc/login.defs"):
        results.append({
            "Kontroll": "Süsteemne paroolipoliitika",
            "Hetkeseis": "Kontrolli manuaalselt",
            "Ootus": "E-ITS vastavus",
            "Staatus": "INFO",
            "Selgitus": "Kontrolli PASS_MAX_DAYS ja PASS_MIN_LEN väärtusi.",
            "Meede": "nano /etc/login.defs"
        })

    return results

def save_audit_results(results):
    out_file = 'TULEMUSED/07_tulemus_turvaaudit.csv'
    import csv
    if not results: return
    
    keys = results[0].keys()
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    print(f"[+] Auditi tulemused salvestatud: {out_file}")

def main():
    print(LOGO)
    os_type = platform.system()
    if os_type == "Windows":
        res = check_windows()
    else:
        res = check_linux()
    save_audit_results(res)

if __name__ == "__main__":
    main()
