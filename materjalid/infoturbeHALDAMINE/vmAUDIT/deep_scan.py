import os
import hashlib
from datetime import datetime, timedelta

# SEADISTUS
DAYS_TO_LOOK_BACK = 180  # Analüüsime viimase poole aasta muudatusi
# Faililaiendid, mis on küberintsidentide puhul kriitilised
SUSPICIOUS_EXTS = ['.exe', '.dll', '.ps1', '.bat', '.vbs', '.js', '.scr', '.hta', '.zip', '.rar']
# Kaustad, kuhu ründajad end kõige sagedamini peidavad
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
    """Arvutab faili SHA256 räsi."""
    hash_sha256 = hashlib.sha256()
    try:
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except:
        return "PUUDUB_LIGIPÄÄS"

def deep_scan():
    report_file = "deep_scan_raport.txt"
    cutoff_date = datetime.now() - timedelta(days=DAYS_TO_LOOK_BACK)
    
    print(f"[*] Alustan süvaskaneerimist (viimased {DAYS_TO_LOOK_BACK} päeva)...")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(f"=== SÜVASKANEERIMISE RAPORT ({datetime.now()}) ===\n")
        f.write(f"Analüüsitud periood alates: {cutoff_date.strftime('%Y-%m-%d')}\n\n")
        
        for base_path in PATHS_TO_SCAN:
            if not base_path or not os.path.exists(base_path):
                continue
            
            f.write(f"\n--- KAUST: {base_path} ---\n")
            print(f"[+] Skaneerin: {base_path}")
            
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        # Võtame faili loomis- ja muutmise aja
                        mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
                        ctime = datetime.fromtimestamp(os.path.getctime(file_path))
                        
                        # Kui faili on muudetud meie valitud ajavahemikus
                        if mtime > cutoff_date or ctime > cutoff_date:
                            ext = os.path.splitext(file)[1].lower()
                            is_suspicious = ext in SUSPICIOUS_EXTS
                            
                            # Märgime kahtlased failid raportis hüüumärkidega
                            prefix = "[!!] KAHTLANE" if is_suspicious else "[ ]"
                            f.write(f"{prefix} | Muudetud: {mtime.strftime('%Y-%m-%d %H:%M')} | {file_path}\n")
                            
                            # Kui fail on kahtlane, lisame kohe ka SHA256 räsi
                            if is_suspicious:
                                file_hash = get_file_hash(file_path)
                                f.write(f"    -> SHA256: {file_hash}\n")
                    except:
                        continue

    print(f"\n[!] Skaneerimine valmis! Tulemused: {report_file}")

if __name__ == "__main__":
    deep_scan()
