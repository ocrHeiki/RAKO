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

01_linux_logid_csv.py - Linuxi logide (/var/log/auth.log jne) konverteerimine CSV-ks.
"""

import os
import csv
import re
from datetime import datetime


def parse_linux_logs():
    print(LOGO)
    out_dir = "TULEMUSED"
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    
    log_files = ["/var/log/auth.log", "/var/log/syslog", "/var/log/messages"]
    headers = ['TimeCreated', 'Id', 'LevelDisplayName', 'Message', 'MachineName', 'RecordId']
    
    count = 0
    for log_path in log_files:
        if not os.path.exists(log_path): continue
        
        out_csv = os.path.join(out_dir, f"01_tulemus_eksport_linux_{os.path.basename(log_path)}.csv")
        print(f"Konverteerin: {log_path} -> {out_csv}")
        
        try:
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f_in, \
                 open(out_csv, 'w', newline='', encoding='utf-8') as f_out:
                
                writer = csv.DictWriter(f_out, fieldnames=headers)
                writer.writeheader()
                
                for i, line in enumerate(f_in):
                    # Lihtne syslog parsimine
                    parts = line.split(maxsplit=4)
                    if len(parts) < 5: continue
                    
                    time_str = f"{parts[0]} {parts[1]} {parts[2]}"
                    machine = parts[3]
                    msg = parts[4]
                    
                    # Pseudo-ID määramine Linuxi sündmustele
                    event_id = "1000" # Üldine sündmus
                    if "Accepted password" in msg or "session opened" in msg:
                        event_id = "4624" # Successful Logon
                    elif "Failed password" in msg or "authentication failure" in msg:
                        event_id = "4625" # Failed Logon
                    elif "new user" in msg:
                        event_id = "4720" # User Created
                    elif "password changed" in msg:
                        event_id = "4723" # Password Changed
                    
                    writer.writerow({
                        'TimeCreated': time_str,
                        'Id': event_id,
                        'LevelDisplayName': 'Info',
                        'Message': msg,
                        'MachineName': machine,
                        'RecordId': str(i)
                    })
                    count += 1
        except Exception as e:
            print(f"VIGA {log_path} lugemisel: {e}")
            
    print(f"[+] Kokku konverteeritud {count} logirida.")

if __name__ == "__main__":
    parse_linux_logs()
