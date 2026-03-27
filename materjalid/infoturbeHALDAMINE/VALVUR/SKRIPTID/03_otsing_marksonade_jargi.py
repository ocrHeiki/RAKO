#!/usr/bin/env python3
"""
03_otsing_marksonade_jargi.py - Otsib kahtlaseid märksõnu logide tekstist.
Kasutamine: python3 SKRIPTID/03_otsing_marksonade_jargi.py
"""

import os
import csv

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
#   |   FAILI NIMI:  03_otsing_marksonade_jargi.py                        |   #
#   |   LOODUD:      27:03:2027                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Kahtlaste märksõnade otsing logide tekstist.         |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def search_suspicious_keywords(in_dir='TULEMUSED', out_file='TULEMUSED/03_tulemus_kahtlased_marksonad.csv'):
    print(LOGO)
    suspicious_keywords = [
        "mimikatz", "psexec", "whoami", "net user", "net group", "net localgroup",
        "ipconfig /all", "tasklist", "encodedcommand", "iex", "invoke-expression",
        "rubeus", "bloodhound", "adfind", "net view", "net share", "quser", 
        "query user", "netdom", "nltest", "gpresult"
    ]
    
    all_results = []
    
    if not os.path.exists(in_dir):
        print(f"VIGA: Kausta {in_dir} ei leitud.")
        return

    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    print(f"--- Kahtlaste märksõnade otsing ({len(csv_files)} faili) ---")
    
    for file_name in csv_files:
        print(f"Otsin failist: {file_name}...")
        try:
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    message = row.get('Message', '').lower()
                    for word in suspicious_keywords:
                        if word in message:
                            row['MatchedKeyword'] = word
                            row['SourceFile'] = file_name
                            all_results.append(row)
                            break
        except Exception as e:
            print(f"VIGA failiga {file_name}: {e}")

    if all_results:
        print(f"Leiti {len(all_results)} kahtlast märksõna.")
        try:
            all_results.sort(key=lambda x: x.get('TimeCreated', ''))
        except Exception:
            pass
            
        fieldnames = list(all_results[0].keys())
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
        print(f"VALMIS! Tulemus salvestatud: {out_file}")
    else:
        print("Märksõnu ei leitud.")

if __name__ == "__main__":
    search_suspicious_keywords()
