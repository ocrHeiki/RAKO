#!/usr/bin/env python3
LOGO = """
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
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Kriitiliste sündmuste eraldamine logidest.           |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""
"""
02_turvafiltreering.py - Filtreerib eksporditud CSV-dest välja kriitilised sündmused.
Kasutamine: python3 SKRIPTID/02_turvafiltreering.py
"""

import os # Impordime mooduli failisüsteemi toiminguteks
import csv # Impordime mooduli CSV failide töötlemiseks


def filter_security_events(in_dir='TULEMUSED', out_file='TULEMUSED/02_tulemus_turvafiltreering.csv'):
    """Funktsioon kriitiliste sündmuste filtreerimiseks CSV-failidest."""
    print(LOGO) # Kuvame logo
    # Määrame kriitilised Event ID-d, mida otsime
    critical_ids = [
        4624, 4625, 4634, 4647, 4648, 4672, 4768, 4769, 4776, # Authentication & Logon
        4720, 4722, 4723, 4724, 4725, 4726, 4732, 4733, 4756, 4781, # Account Management
        4739, 5136, 5137, 5141, # Group Policy & Directory Service Changes
        4688, 4689, 4697, 7045, 4698, 4699, # Process & Service
        4663, 4656, 4658, 4660, 5145, # Object Access
        5156, 5157, 5158, 5152, # Network & Firewall
        1102, 104, 4719, # Log Clearing
        1116, 1117, 5007, # Windows Defender
        4104, # PowerShell Script Block Logging
        4778, 4779, # RDP Sessions
        1, 3, 7, 8, 11, 22, 23, # Sysmon
        1000 # Linux General Events
    ]
    all_results = [] # Siia kogume kõik leitud sündmused
    
    # Kontrollime, kas sisendkaust on olemas
    if not os.path.exists(in_dir):
        print(f"VIGA: Kausta {in_dir} ei leitud.")
        return

    # Otsime kõik CSV failid, mis on loodud esimese skriptiga
    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    print(f"--- Turvafiltreerimise alustamine ({len(csv_files)} faili) ---")
    
    # Töötleme iga faili eraldi
    for file_name in csv_files:
        print(f"Filtreerin: {file_name}...")
        try:
            # Avame CSV faili lugemiseks
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f) # Loeme CSV kui sõnastiku (dictionary)
                for row in reader:
                    try:
                        # Kontrollime, kas sündmuse ID on meie nimekirjas
                        event_id = int(row['Id'])
                        if event_id in critical_ids:
                            # Lisame info algallika kohta
                            row['OriginalLog'] = file_name
                            all_results.append(row) # Lisame sündmuse tulemustesse
                    except (ValueError, KeyError):
                        # Kui rea Id on vigane, liigume edasi
                        continue
        except Exception as e:
            print(f"VIGA failiga {file_name}: {e}")

    # Kui leidsime sündmusi, salvestame need uude faili
    if all_results:
        print(f"Leiti {len(all_results)} kriitilist sündmust.")
        # Sorteerime tulemused aja järgi (TimeCreated)
        try:
            all_results.sort(key=lambda x: x.get('TimeCreated', ''))
        except Exception:
            pass # Kui sorteerimine ebaõnnestub, jätkame sorteerimata
        
        # Määrame väljundfaili veerud (võtame esimesest sündmusest)
        fieldnames = list(all_results[0].keys())
        # Avame faili kirjutamiseks
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader() # Kirjutame CSV päise
            writer.writerows(all_results) # Kirjutame kõik kogutud sündmused korraga
        print(f"VALMIS! Tulemus salvestatud: {out_file}")
    else:
        print("Ühtegi kriitilist sündmust ei leitud.")

if __name__ == "__main__":
    filter_security_events() # Käivitame filtreerimise
