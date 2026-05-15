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
#   |   FAILI NIMI:  03_otsing_marksonade_jargi.py                        |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   MITRE ATT&CK märksõnade otsing ja analüüs.           |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""
"""
03_otsing_marksonade_jargi.py - Otsib kahtlaseid märksõnu logide tekstist + MITRE & CVE mapping.
"""

import os
import csv
from difflib import SequenceMatcher

def fuzzy_match(a, b):
    """
    Arvutab kahe sõna sarnasuse skoori vahemikus 0.0 kuni 1.0.
    Kasutame difflib teeki, mis leiab pikima ühise alamjada.
    See aitab meil leida 'm1m1katz' kui otsime 'mimikatz'.
    """
    return SequenceMatcher(None, a, b).ratio()


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
        "powershell -enc": ("T1059.001", "N/A", "PowerShell Obfuscation"),
        "schtasks": ("T1053.005", "N/A", "Scheduled Task/Job: Scheduled Task"),
        "reg add": ("T1547.001", "N/A", "Boot or Logon Autostart Execution: Registry Run Keys"),
        "net localgroup": ("T1069", "N/A", "Permission Groups Discovery"),
        "sudoers": ("T1548.003", "N/A", "Abuse Elevation Control Mechanism: Sudo and Sudo Caching")
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
                    # Tükeldame logikirje 'Message' välja sõnadeks, et võrrelda neid ükshaaval
                    words_in_message = message.split()
                    
                    found = False
                    for word, info in attack_mapping.items():
                        # SAMM 1: Kontrollime esmalt otsest vastet (kiire meetod)
                        if word in message:
                            score = 1.0
                            found = True
                        else:
                            # SAMM 2: Kui otsest vastet pole, proovime 'Fuzzy matchingut'
                            # Käime läbi kõik sõnad sõnumis, mis on pikemad kui 3 märki
                            score = 0
                            for m_word in words_in_message:
                                if len(m_word) > 3: 
                                    s = fuzzy_match(word, m_word)
                                    # Lävend 0.7 on valitud empiiriliselt: see on piisavalt kõrge,
                                    # et vältida liiga palju valepositiivseid, aga piisavalt madal,
                                    # et tabada märgi-asendusi (nt 'a' asendatud '4'-ga).
                                    if s > 0.7:
                                        score = s
                                        found = True
                                        break
                        
                        if found:
                            # Kui leidsime vaste, salvestame selle koos metainfoga
                            row['MatchedKeyword'] = word
                            row['SimilarityScore'] = f"{score:.2f}"
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
