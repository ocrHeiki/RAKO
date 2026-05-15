#!/usr/bin/env python3
"""
09_threat_intel.py - IP maine kontroll ja Threat Intelligence liides.
"""

import os
import re
import csv

# ASCII Logo (VALVUR standard)
r

# Testimiseks: tuntud pahatahtlikud IP-d (simuleerime andmebaasi)
KNOWN_BAD_IPS = ["1.2.3.4", "8.8.8.8", "192.168.1.100", "45.33.32.156"]

def check_ip_reputation(ip):
    """Siia saab lisada AbuseIPDB või VirusTotal API väljakutse."""
    if ip in KNOWN_BAD_IPS:
        return "MALICIOUS (Known C2)"
    return "CLEAN / UNKNOWN"

def run_threat_intel(in_file='TULEMUSED/04_tulemus_suvaanaluusi_raport.txt'):
    print(LOGO)
    if not os.path.exists(in_file):
        print("Süvaanalüüsi raportit ei leitud.")
        return

    print("[*] Teostan IP maine kontrolli...")
    
    with open(in_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Leiame kõik IP-d raportist
    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
    unique_ips = set(ips)
    
    if not unique_ips:
        print("Raportist IP-sid ei leitud.")
        return

    out_file = 'TULEMUSED/09_tulemus_threat_intel.csv'
    with open(out_file, 'w', newline='', encoding='utf-8') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(['IP', 'Reputation', 'Action_Required'])
        
        for ip in unique_ips:
            reputation = check_ip_reputation(ip)
            print(f"  [?] Kontrollin {ip}: {reputation}")
            action = "BLOCK" if "MALICIOUS" in reputation else "NONE"
            writer.writerow([ip, reputation, action])
            
    print(f"[+] Maine kontroll lõpetatud. Tulemused: {out_file}")

if __name__ == "__main__":
    run_threat_intel()
