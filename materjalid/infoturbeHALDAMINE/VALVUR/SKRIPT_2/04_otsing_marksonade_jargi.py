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
#   |   FAILI NIMI:  04_otsing_marksonade_jargi.py                        |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   MITRE ATT&CK märksõnade otsing ja analüüs.           |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import csv
from difflib import SequenceMatcher

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import utils

logger = utils.setup_logging("MARKSONAD")

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

def fuzzy_match(a, b):
    return SequenceMatcher(None, a, b).ratio()

def search_suspicious_keywords():
    print(LOGO)
    in_dir = utils.get_output_dir()
    out_file = os.path.join(in_dir, '04_tulemus_kahtlased_marksonad.csv')
    attack_mapping = {"mimikatz": ("T1003", "CVE-2014-0322", "Credential Dumping"), "whoami": ("T1033", "N/A", "Discovery"), "vssadmin": ("T1490", "N/A", "Ransomware")}
    all_results = []
    if not os.path.exists(in_dir): return
    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    for file_name in csv_files:
        try:
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    msg = row.get('Message', '').lower()
                    for word, info in attack_mapping.items():
                        if word in msg or any(fuzzy_match(word, w) > 0.7 for w in msg.split() if len(w) > 3):
                            row['MatchedKeyword'] = word
                            row['MITRE_ID'] = info[0]
                            row['Attack_Type'] = info[2]
                            all_results.append(row)
                            break
        except: continue
    if all_results:
        fieldnames = list(all_results[0].keys())
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"[+] Tuvastati {len(all_results)} ründeindikaatorit.")

if __name__ == "__main__":
    search_suspicious_keywords()
