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
#   |   FAILI NIMI:  02_linux_logid_csv.py                                |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Linuxi logide konverteerimine ja normaliseerimine.   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import csv
import re

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

logger = utils.setup_logging("LINUX_CSV")

def parse_linux_logs():
    print(LOGO)
    out_dir = utils.get_output_dir()
    if not os.path.exists(out_dir): os.makedirs(out_dir, exist_ok=True)

    search_dirs = ["/var/log", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "LOGID")]
    log_files_to_find = ["auth.log", "syslog", "messages", "secure"]

    headers = ['TimeCreated', 'Id', 'LevelDisplayName', 'Message', 'MachineName', 'RecordId']
    count = 0

    for d in search_dirs:
        if not os.path.exists(d): continue
        for f_name in os.listdir(d):
            if any(target in f_name for target in log_files_to_find):
                log_path = os.path.join(d, f_name)
                out_csv = os.path.join(out_dir, f"01_tulemus_eksport_linux_{f_name}.csv")
                print(f"Konverteerin: {log_path} -> {out_csv}")
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f_in, \
                         open(out_csv, 'w', newline='', encoding='utf-8') as f_out:
                        writer = csv.DictWriter(f_out, fieldnames=headers)
                        writer.writeheader()
                        for i, line in enumerate(f_in):
                            parts = line.split(maxsplit=4)
                            if len(parts) < 5: continue
                            time_str = f"{parts[0]} {parts[1]} {parts[2]}"
                            machine = parts[3]
                            msg = parts[4]
                            event_id = "1000"
                            if "Accepted password" in msg or "session opened" in msg: event_id = "4624"
                            elif "Failed password" in msg or "authentication failure" in msg: event_id = "4625"
                            elif "new user" in msg: event_id = "4720"
                            writer.writerow({'TimeCreated': time_str, 'Id': event_id, 'LevelDisplayName': 'Info', 'Message': msg, 'MachineName': machine, 'RecordId': str(i)})
                            count += 1
                except Exception as e:
                    logger.error(f"Viga faili {log_path} töötlemisel: {e}")
                    continue
    print(f"[+] Kokku konverteeritud {count} logirida.")

if __name__ == "__main__":
    parse_linux_logs()
