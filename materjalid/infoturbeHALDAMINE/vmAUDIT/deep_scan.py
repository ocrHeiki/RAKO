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
#   |   FAILI NIMI:  deep_scan.py                                         |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Failisüsteemi skaneerimine, muudatuste tuvastamine   |   #
#   |                ja SHA256 kontrollsummade arvutamine.                |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import os
import hashlib
from datetime import datetime, timedelta

DAYS_TO_LOOK_BACK = 180
SUSPICIOUS_EXTS = ['.exe', '.dll', '.ps1', '.bat', '.vbs', '.js', '.scr', '.hta', '.zip', '.rar']
PATHS_TO_SCAN = [
    os.environ.get('TEMP'),
    os.path.join(os.environ.get('USERPROFILE'), 'Downloads'),
    os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Roaming'),
    os.path.join(os.environ.get('USERPROFILE'), 'AppData', 'Local'),
    'C:\\Users\\Public',
    'C:\\ProgramData',
    'C:\\Windows\\Temp'
]

def get_file_hash(fname):
    hash_sha256 = hashlib.sha256()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except:
        return "LIGIPÄÄS_PUUDUB"

def deep_scan():
    report_file = "deep_scan_raport.txt"
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_LOOK_BACK)
    
    print(f"[*] VALVUR: Alustan süvaskaneerimist...")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"VALVUR SÜVASKANEERIMISE RAPORT - Autor: Heiki Rebane\n")
        f.write(f"Analüüsitud periood alates: {cutoff_date.strftime('%Y-%m-%d')}\n\n")
        
        for base_path in PATHS_TO_SCAN:
            if not base_path or not os.path.exists(base_path):
                continue
            
            f.write(f"\n--- SEKTOR: {base_path} ---\\n")
            print(f"[+] Kontrollin: {base_path}")
            
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        if mtime > cutoff_date:
                            ext = os.path.splitext(file)[1].lower()
                            is_suspicious = ext in SUSPICIOUS_EXTS
                            
                            line = f"{ '[!!]' if is_suspicious else '[ ]'} | {mtime.strftime('%Y-%m-%d %H:%M')} | {file_path}"
                            f.write(line + "\n")
                            
                            if is_suspicious:
                                f.write(f"    -> SHA256: {get_file_hash(file_path)}\n")
                    except:
                        continue

    print(f"\n[!] Skaneerimine lõpetatud. Raport: {report_file}")

if __name__ == "__main__":
    deep_scan()
