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
#   |   FAILI NIMI:  12_linux_syvaanaluus.py                              |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Linuxi logide terviklus ja SSH süvaanalüüs.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import re
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

logger = utils.setup_logging("LINUX_SYVA")

def get_log_timestamps(log_path):
    timestamps = []
    pattern = re.compile(r'^\w{3}\s+\d+\s+\d{2}:\d{2}:\d{2}')
    try:
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                m = pattern.search(line)
                if m:
                    timestamps.append(m.group())
    except Exception as e:
        logger.error(f"Logi lugemine ebaõnnestus {log_path}: {e}")
    return timestamps

def detect_log_tampering(auth_log_path):
    timestamps = get_log_timestamps(auth_log_path)
    if len(timestamps) < 3:
        return []
    gaps = []
    for i in range(1, len(timestamps)):
        try:
            from datetime import datetime
            t1 = datetime.strptime(timestamps[i-1], "%b %d %H:%M:%S")
            t2 = datetime.strptime(timestamps[i], "%b %d %H:%M:%S")
            diff = (t2 - t1).total_seconds()
            if diff > 3600:
                gaps.append(f"Logipraeg: {timestamps[i-1]} -> {timestamps[i]} ({diff/60:.0f} min)")
        except ValueError:
            continue
    return gaps

def analyze_ssh_logins(auth_log_path):
    results = []
    patterns = [
        (r'Accepted\s+\w+\s+for\s+(\S+)\s+from\s+(\S+)', '4624', 'SSV sisselogimine'),
        (r'Failed\s+password\s+for\s+(\S+)\s+from\s+(\S+)', '4625', 'Ebaõnnestunud SSV'),
        (r'Connection closed by authenticating user\s+(\S+)\s+(\S+)', '4625', 'SSV ühendus katkestatud'),
    ]
    try:
        with open(auth_log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                for pattern, event_id, desc in patterns:
                    m = re.search(pattern, line, re.IGNORECASE)
                    if m:
                        results.append({"EventID": event_id, "Kirjeldus": desc, "Detail": line.strip()})
                        break
    except Exception as e:
        logger.error(f"SSH analüüs ebaõnnestus: {e}")
    return results

def main():
    print(LOGO)
    out_dir = utils.get_output_dir()
    out_file = os.path.join(out_dir, '12_tulemus_linux_syvaanaluus.csv')
    auth_log_path = "/var/log/auth.log"
    if not os.path.exists(auth_log_path):
        auth_log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LOGID", "auth.log")
    results = []
    if os.path.exists(auth_log_path):
        logger.info(f"Analüüsin: {auth_log_path}")
        results += analyze_ssh_logins(auth_log_path)
        gaps = detect_log_tampering(auth_log_path)
        for g in gaps:
            results.append({"EventID": "TAMPER", "Kirjeldus": "Logide võltsimise kahtlus", "Detail": g})
    else:
        logger.warning(f"auth.log ei leitud teelt: {auth_log_path}")
        results.append({"EventID": "N/A", "Kirjeldus": "Info", "Detail": "auth.log puudub, SSH analüüs teostamata"})
    if results:
        keys = results[0].keys()
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
    logger.info(f"Linuxi süvaanalüüs valmis: {out_file} ({len(results)} leidu)")

if __name__ == "__main__":
    main()
