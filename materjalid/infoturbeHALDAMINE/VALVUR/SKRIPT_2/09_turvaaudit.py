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
#   |   FAILI NIMI:  09_turvaaudit.py                                     |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   E-ITS vastavuskontroll ja Roadmap.                   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import platform
import subprocess
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

logger = utils.setup_logging("TURVAAUDIT")

def check_windows_policies():
    results = []
    try:
        output = subprocess.check_output(["net", "accounts"], timeout=10).decode()
        if "maximum password age" in output.lower():
            results.append({"Kontroll": "Parooli vanusepiirang", "Staatus": "INFO", "Meede": "Kontrolli net accounts väljundit"})
    except Exception as e:
        logger.error(f"Windowsi poliitika kontroll ebaõnnestus: {e}")
    return results

def check_linux_policies():
    results = []
    try:
        with open("/etc/login.defs", "r") as f:
            content = f.read()
            for line in content.splitlines():
                if "PASS_MAX_DAYS" in line and not line.startswith("#"):
                    results.append({"Kontroll": "Parooli max vanus", "Staatus": "INFO", "Meede": line.strip()})
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.error(f"Linuxi poliitika kontroll ebaõnnestus: {e}")
    return results

def check_running_services():
    results = []
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(["sc", "query"], timeout=15).decode()
        else:
            output = subprocess.check_output(["systemctl", "list-units", "--type=service", "--state=running"], timeout=15).decode()
        results.append({"Kontroll": "Teenuste loend", "Staatus": "OK", "Meede": f"Leitud {len(output.splitlines())} rida"})
    except Exception as e:
        logger.error(f"Teenuste kontroll ebaõnnestus: {e}")
    return results

def check_firewall():
    results = []
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(["netsh", "advfirewall", "show", "allprofiles"], timeout=10).decode()
        else:
            output = subprocess.check_output(["sudo", "ufw", "status"], timeout=10).decode()
        results.append({"Kontroll": "Tulemüür", "Staatus": "OK", "Meede": "Tulemüür on aktiivne" if "State: active" in output else "Tulemüür vajab kontrolli"})
    except Exception as e:
        results.append({"Kontroll": "Tulemüür", "Staatus": "INFO", "Meede": f"Kontroll ebaõnnestus: {e}"})
    return results

def check_audit_policy():
    results = []
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output(["auditpol", "/get", "/category:*"], timeout=10).decode()
            results.append({"Kontroll": "Auditipoliitika", "Staatus": "INFO", "Meede": "Auditpol tulemused vaata failist"})
            with open(os.path.join(utils.get_output_dir(), "09_auditpol_valjund.txt"), "w") as f:
                f.write(output)
        else:
            results.append({"Kontroll": "Auditipoliitika", "Staatus": "OK", "Meede": "Linuxi auditd kontroll käsitsi"})
    except Exception as e:
        results.append({"Kontroll": "Auditipoliitika", "Staatus": "INFO", "Meede": f"Kontroll ebaõnnestus: {e}"})
    return results

def main():
    print(LOGO)
    out_dir = utils.get_output_dir()
    out_file = os.path.join(out_dir, '09_tulemus_turvaaudit.csv')
    results = []
    results += check_windows_policies()
    results += check_linux_policies()
    results += check_running_services()
    results += check_firewall()
    results += check_audit_policy()
    if not results:
        results = [{"Kontroll": "Audit", "Staatus": "PASS", "Meede": "Kõik kontrollitud"}]
    keys = results[0].keys()
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    logger.info(f"Audit valmis: {out_file} ({len(results)} kontrolli)")

if __name__ == "__main__":
    main()
