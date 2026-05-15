import gzip
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
#   |   FAILI NIMI:  15_tehniline_raport_pdf.py                    |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Tehnilise PDF-raporti genereerimine.          |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

14_linux_syvaanaluus.py - Linuxi logide terviklus ja süvaanalüüs (SSH, Auditd).
Tuvastab "Log Tampering" (ajalehed logides).
"""

import os
import re
import csv
from datetime import datetime

r

def detect_log_tampering(log_path):
    """Otsib logifailist suuri ajalisi auke."""
    print(f"[*] Kontrollin logide terviklust: {log_path}")
    if not os.path.exists(log_path):
        return []

    tampering_findings = []
    prev_time = None
    
    # Regulaaravaldis standardse Linuxi logi aja jaoks (nt May 12 10:00:01)
    time_pattern = r'^[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2}'
    
    try:
        opener = gzip.open if log_path.endswith(".gz") else open
    with opener(log_path, "rt", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = re.search(time_pattern, line)
                if match:
                    current_time_str = match.group()
                    # Lisame aasta, et saaksime arvutada vahet
                    current_time = datetime.strptime(f"{datetime.now().year} {current_time_str}", "%Y %b %d %H:%M:%S")
                    
                    if prev_time:
                        diff = (current_time - prev_time).total_seconds()
                        # Kui vahe on suurem kui 1 tund (3600 sek), märgime selle kui anomaalia
                        if diff > 3600:
                            tampering_findings.append({
                                "Aeg": current_time.isoformat(),
                                "Tüüp": "LOG_GAP",
                                "Kirjeldus": f"Logis on auk: {diff/3600:.1f} tundi.",
                                "Severity": "High",
                                "MITRE": "T1562.002" # Impair Defenses: Indicator Blocking
                            })
                    prev_time = current_time
    except Exception as e:
        print(f"[!] VIGA: {e}")
        
    return tampering_findings

def analyze_ssh_logins(log_path):
    """Eraldab auth.log-ist IP-aadressid ja sisselogimise katsed."""
    print(f"[*] Analüüsin SSH sisselogimisi: {log_path}")
    findings = []
    if not os.path.exists(log_path): return []

    # Otsime Accepted ja Failed password ridu
    pattern = r'(Accepted|Failed) password for (invalid user )?(\w+) from ([\d.]+) port \d+ ssh2'
    
    try:
        opener = gzip.open if log_path.endswith(".gz") else open
    with opener(log_path, "rt", encoding="utf-8", errors="ignore") as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    status, _, user, ip = match.groups()
                    findings.append({
                        "Aeg": datetime.now().isoformat(), # Lihtsuse mõttes praegune, reaalselt logist
                        "Tüüp": "SSH_LOGIN",
                        "Kirjeldus": f"{status} login: kasutaja '{user}' aadressilt {ip}",
                        "Severity": "Medium" if status == "Accepted" else "High",
                        "MITRE": "T1110" # Brute Force
                    })
    except: pass
    return findings

def main():
    print(LOGO)
    auth_log = "/var/log/auth.log"
    # Kui faili pole (nt teises masinas), proovime asenduskohta
    if not os.path.exists(auth_log):
        auth_log = "LOGID/auth.log" # Eksamikeskkonna jaoks

    tampering = detect_log_tampering(auth_log)
    ssh_logins = analyze_ssh_logins(auth_log)
    
    # Normaliseeritud väljund
    out_file = "TULEMUSED/14_tulemus_linux_syvaanaluus.csv"
    all_findings = tampering + ssh_logins
    
    if all_findings:
        with open(out_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Aeg", "Tüüp", "Kirjeldus", "Severity", "MITRE"])
            writer.writeheader()
            writer.writerows(all_findings)
        print(f"[+] Linuxi süvaanalüüs valmis. Leiti {len(all_findings)} sündmust.")
    else:
        print("[i] Linuxi süvaanalüüs anomaaliaid ei tuvastanud.")

if __name__ == "__main__":
    main()
