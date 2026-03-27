#!/usr/bin/env python3
"""
03_otsing_marksonade_jargi.py - Otsib kahtlaseid märksõnu logide tekstist.
Kasutamine: python3 SKRIPTID/03_otsing_marksonade_jargi.py
"""

import os # Impordime mooduli operatsioonisüsteemi toiminguteks
import csv # Impordime mooduli CSV failide töötlemiseks

# ASCII Logo ja metainfo definitsioon
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
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Kahtlaste märksõnade otsing logide tekstist.         |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def search_suspicious_keywords(in_dir='TULEMUSED', out_file='TULEMUSED/03_tulemus_kahtlased_marksonad.csv'):
    """Funktsioon kahtlaste märksõnade otsimiseks logide sisu hulgast."""
    print(LOGO) # Kuvame logo
    # Nimekiri märksõnadest ja käskudest, mida ründajad sageli kasutavad
    suspicious_keywords = [
        "mimikatz", "psexec", "whoami", "net user", "net group", "net localgroup",
        "ipconfig /all", "tasklist", "encodedcommand", "iex", "invoke-expression",
        "rubeus", "bloodhound", "adfind", "net view", "net share", "quser", 
        "query user", "netdom", "nltest", "gpresult"
    ]
    
    all_results = [] # Siia kogume sündmused, millest leidsime märksõnu
    
    # Kontrollime, kas kaust on olemas
    if not os.path.exists(in_dir):
        print(f"VIGA: Kausta {in_dir} ei leitud.")
        return

    # Otsime kõik CSV-d, mis on konverteeritud esimese skriptiga
    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    print(f"--- Kahtlaste märksõnade otsing ({len(csv_files)} faili) ---")
    
    # Töötleme iga faili eraldi
    for file_name in csv_files:
        print(f"Otsin failist: {file_name}...")
        try:
            # Avame CSV faili lugemiseks
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f) # Loeme CSV kui sõnastiku
                for row in reader:
                    # Võtame sündmuse kirjelduse (Message) ja muudame selle väiketähtedeks
                    message = row.get('Message', '').lower()
                    # Kontrollime iga märksõna olemasolu sõnumis
                    for word in suspicious_keywords:
                        if word in message:
                            # Kui leidsime, lisame info selle kohta
                            row['MatchedKeyword'] = word # Märksõna, mis leiti
                            row['SourceFile'] = file_name # Allikas, kus leiti
                            all_results.append(row) # Lisame tulemustesse
                            break # Ühe sündmuse kohta piisab ühest leitud märksõnast
        except Exception as e:
            print(f"VIGA failiga {file_name}: {e}")

    # Kui leidsime kahtlaseid sündmusi, salvestame need uude faili
    if all_results:
        print(f"Leiti {len(all_results)} kahtlast märksõna.")
        # Sorteerime tulemused kronoloogiliselt
        try:
            all_results.sort(key=lambda x: x.get('TimeCreated', ''))
        except Exception:
            pass # Kui sorteerimine ebaõnnestub, liigume edasi
            
        # Määrame väljundfaili veerud (võtame esimesest sündmusest)
        fieldnames = list(all_results[0].keys())
        # Avame faili kirjutamiseks
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader() # Kirjutame CSV päise
            writer.writerows(all_results) # Kirjutame kõik sündmused faili
        print(f"VALMIS! Tulemus salvestatud: {out_file}")
    else:
        print("Märksõnu ei leitud.")

if __name__ == "__main__":
    search_suspicious_keywords() # Käivitame otsingu
