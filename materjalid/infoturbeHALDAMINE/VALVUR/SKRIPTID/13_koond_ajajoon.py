#!/usr/bin/env python3
"""
13_koond_ajajoon.py - Ühtse kronoloogilise ajajoone loomine kõikidest logiallikatest.
"""

import os
import csv
from datetime import datetime

r

def generate_unified_timeline(in_dir='TULEMUSED', out_file='TULEMUSED/13_tulemus_koond_ajajoon.csv'):
    print(LOGO)
    print("[*] Koondan logisid ühtseks ajajooneks...")
    
    timeline = []
    
    # Otsime faile, mis sisaldavad töödeldud andmeid
    target_files = {
        '02_tulemus_turvafiltreering.csv': 'Win_Security',
        '03_tulemus_kahtlased_marksonad.csv': 'Suspicious_Match',
        '07_tulemus_turvaaudit.csv': 'Audit_Finding'
    }

    for file_name, source_type in target_files.items():
        file_path = os.path.join(in_dir, file_name)
        if not os.path.exists(file_path):
            continue
            
        print(f" [+] Töötlen: {file_name}")
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Proovime leida aja välja (võib olla 'TimeCreated' või 'Time')
                timestamp = row.get('TimeCreated') or row.get('Time') or '1970-01-01 00:00:00'
                
                # Loome lihtsustatud kirje ajajoone jaoks
                event = {
                    'Aeg': timestamp,
                    'Allikas': source_type,
                    'Sündmus': row.get('Message', '')[:200].replace('
', ' '), # Lõikame lühemaks
                    'Kasutaja': row.get('TargetUserName') or row.get('User') or 'N/A',
                    'Arvuti': row.get('MachineName') or 'N/A',
                    'Info': f"Matched: {row.get('MatchedKeyword', 'N/A')}"
                }
                timeline.append(event)

    # Sorteerime kogu nimekirja aja järgi
    # Märkus: Eeldame ISO formaati (YYYY-MM-DD...), mis sorteerub tekstina õigesti
    timeline.sort(key=lambda x: x['Aeg'])

    if timeline:
        fieldnames = ['Aeg', 'Allikas', 'Kasutaja', 'Arvuti', 'Sündmus', 'Info']
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(timeline)
        print(f"
[OK] Ühtne ajajoon loodud: {out_file}")
        print(f"[*] Kokku koondati {len(timeline)} sündmust kronoloogilisse järjekorda.")
    else:
        print("[!] Sündmusi ei leitud, ajajoon on tühi.")

if __name__ == "__main__":
    generate_unified_timeline()
