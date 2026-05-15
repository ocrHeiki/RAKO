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
#   |   FAILI NIMI:  06_kahtlased_failid.py                        |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Kahtlaste failide süvaskann (Live & Logid).   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

06_kahtlased_failid.py - Tuvastab kahtlased failid nii logidest kui ka süsteemist (Live Scan).
"""

import os
import csv
import platform

# ASCII Logo (VALVUR standard)
r

def live_system_scan():
    print("[*] Alustan süsteemi reaalajas kontrolli (Live Scan)...")
    suspicious_files = []
    
    # Määrame skaneeritavad laiendid (nii Windows kui Linux)
    exts = ('.exe', '.ps1', '.bat', '.sh', '.php', '.scr', '.vbs', '.elf')
    
    is_win = platform.system() == "Windows"
    search_paths = [os.environ.get('TEMP', 'C:\\Windows\\Temp'), 'C:\\Users\\Public'] if is_win else ['/tmp', '/var/tmp', '/dev/shm']

    # 1. FAILISÜSTEEMI KONTROLL
    for path in search_paths:
        if not os.path.exists(path): continue
        print(f"  Skaneerin: {path}...")
        for root, dirs, files in os.walk(path):
            # Kontrollime ka peidetud kaustu (Linuxi rootkit-ide lemmik)
            if not is_win:
                files.extend([f for f in os.listdir(root) if f.startswith('.') and not os.path.isdir(os.path.join(root, f))])
            
            for file in files:
                if file.lower().endswith(exts) or (not is_win and file.startswith('.')):
                    full_path = os.path.join(root, file)
                    suspicious_files.append({
                        "Tüüp": "LIVE_FILE",
                        "Asukoht": full_path,
                        "Põhjus": "Käivitatav või peidetud fail kahtlases asukohas"
                    })

    # 2. PERSISTENCE (PÜSIVUS) KONTROLL
    if is_win:
        # Windows: PowerShell-i ajalugu (ConsoleHost_history.txt)
        history_path = os.path.expandvars(r"%AppData%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt")
        if os.path.exists(history_path):
            suspicious_files.append({"Tüüp": "HISTORY", "Asukoht": history_path, "Põhjus": "PowerShell käskude ajalugu leitud"})
    else:
        # Linux: SSH volitatud võtmed (authorized_keys)
        # Kontrollime nii /home kui /root kaustu
        for h in ['/root'] + [f.path for f in os.scandir('/home') if f.is_dir()]:
            auth_keys = os.path.join(h, ".ssh/authorized_keys")
            if os.path.exists(auth_keys):
                suspicious_files.append({"Tüüp": "SSH_KEY", "Asukoht": auth_keys, "Põhjus": "SSH püsivuse kontrollpunkt"})
        
        # Linux: Cron-tööd ja Systemd (ajastatud tegevused)
        for cp in ["/etc/crontab", "/etc/cron.d"]:
            if os.path.exists(cp):
                suspicious_files.append({"Tüüp": "CRON", "Asukoht": cp, "Põhjus": "Süsteemne ajastatud töö"})

    # 3. BRAUSERI INDIKAATORID (Punkt 12)
    browser_paths = []
    if is_win:
        browser_paths = [
            os.path.expandvars(r"%LocalAppData%\Google\Chrome\User Data\Default\History"),
            os.path.expandvars(r"%AppData%\Mozilla\Firefox\Profiles")
        ]
    else:
        browser_paths = [
            os.path.expanduser("~/.config/google-chrome/Default/History"),
            os.path.expanduser("~/.mozilla/firefox")
        ]
    
    for bp in browser_paths:
        if os.path.exists(bp):
            suspicious_files.append({"Tüüp": "BROWSER", "Asukoht": bp, "Põhjus": "Brauseri profiil/ajalugu tuvastatud"})

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
