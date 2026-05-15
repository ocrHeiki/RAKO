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
#   |   FAILI NIMI:  10_threat_intel.py                                   |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   IP-aadresside kontroll mustade nimekirjade vastu     |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import re
import csv

def run_threat_intel():
    out_dir = os.environ.get("VALVUR_OUT", "TULEMUSED")
    KNOWN_BAD_IPS = ["1.2.3.4", "45.33.32.156", "185.220.101.10"] # Demo nimekiri
    
    found_ips = set()
    # Skaneerime kõik seni loodud tekstilised tulemused IP-de leidmiseks
    for filename in os.listdir(out_dir):
        if filename.endswith((".csv", ".txt")) and "tulemus" in filename:
            with open(os.path.join(out_dir, filename), 'r', errors='ignore') as f:
                content = f.read()
                ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
                for ip in ips:
                    # Välistame kohalikud aadressid
                    if not ip.startswith(("127.", "192.168.", "10.", "172.16.")):
                        found_ips.add(ip)

    out_file = os.path.join(out_dir, "10_tulemus_threat_intel.csv")
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["IP", "STAATUS", "LEITUD"])
        for ip in found_ips:
            status = "OHTLIK (C2/Botnet)" if ip in KNOWN_BAD_IPS else "PUHAS / TUNDMATU"
            writer.writerow([ip, status, "Süsteemne analüüs"])
    
    print(f"[OK] Threat Intel kontrollis {len(found_ips)} välis-IP-d.")

if __name__ == "__main__":
    run_threat_intel()
