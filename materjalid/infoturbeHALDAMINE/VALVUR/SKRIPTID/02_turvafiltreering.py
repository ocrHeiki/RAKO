#!/usr/bin/env python3
"""
02_turvafiltreering.py - Filtreerib eksporditud CSV-dest välja kriitilised sündmused.
Kasutamine: python3 SKRIPTID/02_turvafiltreering.py
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
#   |   FAILI NIMI:  02_turvafiltreering.py                               |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Kriitiliste Event ID-de filtreerimine CSV-dest.      |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def filter_security_events(in_dir='TULEMUSED', out_file='TULEMUSED/02_tulemus_turvafiltreering.csv'):
    print(LOGO)
    critical_ids = [4624, 4625, 4688, 4672, 4697, 7045, 1102, 4720, 4732, 4104]
    all_results = []
    
    if not os.path.exists(in_dir):
        print(f"VIGA: Kausta {in_dir} ei leitud.")
        return

    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    print(f"--- Turvafiltreerimise alustamine ({len(csv_files)} faili) ---")
    
    for file_name in csv_files:
        print(f"Filtreerin: {file_name}...")
        try:
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        event_id = int(row['Id'])
                        if event_id in critical_ids:
                            row['OriginalLog'] = file_name
                            all_results.append(row)
                    except (ValueError, KeyError):
                        continue
        except Exception as e:
            print(f"VIGA failiga {file_name}: {e}")

    if all_results:
        print(f"Leiti {len(all_results)} kriitilist sündmust.")
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
        print("Ühtegi kriitilist sündmust ei leitud.")

if __name__ == "__main__":
    filter_security_events()
