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
#   |   KIRJELDUS:   IP-aadresside maine kontroll (AbuseIPDB).            |   #
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

logger = utils.setup_logging("THREAT_INTEL")

def extract_ips(text):
    return re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text)

def check_ip_reputation(ip):
    try:
        import urllib.request
        url = f"https://www.virustotal.com/ui/ip_addresses/{ip}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req, timeout=10)
        return f"Vastus {resp.status}"
    except Exception as e:
        return f"Kontroll ebaõnnestus: {e}"

def main():
    print(LOGO)
    out_dir = utils.get_output_dir()
    out_file = os.path.join(out_dir, '10_tulemus_threat_intel.csv')
    ips_found = set()
    csv_dir = out_dir
    if os.path.exists(csv_dir):
        for f_name in os.listdir(csv_dir):
            if f_name.endswith('.csv'):
                try:
                    with open(os.path.join(csv_dir, f_name), 'r', encoding='utf-8') as f:
                        for line in f:
                            ips_found.update(extract_ips(line))
                except:
                    continue
    local_ips = {'127.', '10.', '192.168.', '172.16.', '0.0.0.0'}
    results = []
    for ip in sorted(ips_found):
        if any(ip.startswith(p) for p in local_ips):
            continue
        reputation = check_ip_reputation(ip)
        results.append({"IP": ip, "Maine": reputation})
        logger.info(f"IP {ip}: {reputation}")
    if results:
        keys = results[0].keys()
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(results)
    logger.info(f"Maine kontroll lõpetatud: {len(results)} IP-d kontrollitud")

if __name__ == "__main__":
    main()
