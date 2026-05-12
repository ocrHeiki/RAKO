#!/usr/bin/env python3
"""
06_kahtlased_failid.py - Tuvastab kahtlased failid nii logidest kui ka süsteemist (Live Scan).
"""

import os
import csv
import platform

# ASCII Logo (VALVUR standard)
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
#   |   FAILI NIMI:  06_kahtlased_failid.py                               |   #
#   |   LOODUD:      2026-05-12                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Kahtlaste failide süvaskann (Live & Logid).          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def live_system_scan():
    print("[*] Alustan süsteemi reaalajas kontrolli (Live Scan)...")
    suspicious_files = []
    
    # Määrame skaneeritavad laiendid
    exts = ('.exe', '.ps1', '.bat', '.sh', '.php', '.scr', '.vbs')
    
    # Alustame skaneerimist skripti asukohast või juurkataloogist
    # NB! Täisskaneerimine võib võtta aega, piirdume oluliste kohtadega
    search_paths = []
    if platform.system() == "Windows":
        search_paths = [os.environ.get('TEMP', 'C:\\Windows\\Temp'), 'C:\\Users\\Public']
    else:
        search_paths = ['/tmp', '/var/tmp', '/home', '/dev/shm']

    for path in search_paths:
        if not os.path.exists(path): continue
        print(f"  Skaneerin: {path}...")
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.lower().endswith(exts):
                    full_path = os.path.join(root, file)
                    suspicious_files.append({
                        "Tüüp": "LIVE_FILE",
                        "Asukoht": full_path,
                        "Põhjus": "Käivitatav fail ajutises kaustas"
                    })
    return suspicious_files

def analyze_logs(in_dir='TULEMUSED'):
    all_results = []
    if not os.path.exists(in_dir): return []
    
    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    
    for file_name in csv_files:
        try:
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    msg = row.get('Message', '').lower()
                    if any(x in msg for x in ['.exe', '.ps1', '.sh', '.php', 'temp\\', '/tmp/']):
                        row['Source'] = "LOG_ENTRY"
                        all_results.append(row)
        except: pass
    return all_results

def main():
    print(LOGO)
    live_findings = live_system_scan()
    log_findings = analyze_logs()
    
    out_file = 'TULEMUSED/06_tulemus_kahtlased_failid.csv'
    # Salvestame koondtulemuse (lihtsuse mõttes logi-formaadis)
    import csv
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        if log_findings or live_findings:
            writer = csv.writer(f)
            writer.writerow(['Type', 'Path/Message', 'Reason/Time'])
            for fnd in live_findings:
                writer.writerow(['LIVE', fnd['Asukoht'], fnd['Põhjus']])
            for fnd in log_findings:
                writer.writerow(['LOG', fnd.get('Message', '')[:200], fnd.get('TimeCreated')])
    
    print(f"[+] Kokku leiti {len(live_findings) + len(log_findings)} kahtlast viidet.")
    print(f"[+] Tulemused: {out_file}")

if __name__ == "__main__":
    main()
