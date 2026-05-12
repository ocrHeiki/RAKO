#!/usr/bin/env python3
"""
03_otsing_marksonade_jargi.py - Otsib kahtlaseid märksõnu logide tekstist + MITRE & CVE mapping.
"""

import os
import csv

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
#   |   PROJEKT:     VALVUR - MITRE & CVE Maatriks                        |   #
#   |   FAILI NIMI:  03_otsing_marksonade_jargi.py                        |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   KIRJELDUS:   Kahtlaste märksõnade otsing ja ründe klassifitseerimine. |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def search_suspicious_keywords(in_dir='TULEMUSED', out_file='TULEMUSED/03_tulemus_kahtlased_marksonad.csv'):
    print(LOGO)
    
    # Ründemaatriks: Märksõna -> (MITRE ID, CVE viide, Kirjeldus)
    attack_mapping = {
        "mimikatz": ("T1003", "CVE-2014-0322", "OS Credential Dumping"),
        "psexec": ("T1570", "N/A", "Lateral Tool Transfer"),
        "whoami": ("T1033", "N/A", "System Owner/User Discovery"),
        "net user": ("T1087", "N/A", "Account Discovery"),
        "encodedcommand": ("T1027", "N/A", "Obfuscated Files or Information"),
        "vssadmin": ("T1490", "N/A", "Inhibit System Recovery (Ransomware sidekick)"),
        "certutil": ("T1105", "CVE-2021-40444", "Ingress Tool Transfer (Download)"),
        "bitsadmin": ("T1197", "N/A", "BITS Jobs (Persistence/Download)"),
        "rubeus": ("T1558", "N/A", "Steal or Forge Kerberos Tickets"),
        "bloodhound": ("T1482", "N/A", "Domain Trust Discovery"),
        "printnightmare": ("T1068", "CVE-2021-34527", "Exploitation for Privilege Escalation"),
        "proxyshell": ("T1190", "CVE-2021-34473", "Exploit Public-Facing Application"),
        "log4j": ("T1190", "CVE-2021-44228", "Log4Shell Exploit attempt"),
        "powershell -enc": ("T1059.001", "N/A", "PowerShell Obfuscation")
    }

    all_results = []
    if not os.path.exists(in_dir): return

    csv_files = [f for f in os.listdir(in_dir) if f.startswith('01_tulemus_eksport_') and f.endswith('.csv')]
    print(f"--- MITRE & CVE analüüs ({len(csv_files)} faili) ---")
    
    for file_name in csv_files:
        try:
            with open(os.path.join(in_dir, file_name), mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    message = row.get('Message', '').lower()
                    for word, info in attack_mapping.items():
                        if word in message:
                            row['MatchedKeyword'] = word
                            row['MITRE_ID'] = info[0]
                            row['CVE_ID'] = info[1]
                            row['Attack_Type'] = info[2]
                            row['SourceFile'] = file_name
                            all_results.append(row)
                            break
        except Exception as e:
            print(f"VIGA: {e}")

    if all_results:
        print(f"[+] Tuvastati {len(all_results)} ründeindikaatorit.")
        fieldnames = list(all_results[0].keys())
        with open(out_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_results)
    else:
        print("[-] Ründeindikaatoreid ei leitud.")

if __name__ == "__main__":
    search_suspicious_keywords()
