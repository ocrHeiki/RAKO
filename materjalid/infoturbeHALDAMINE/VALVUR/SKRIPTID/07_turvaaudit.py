#!/usr/bin/env python3

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
#   |   FAILI NIMI:  07_turvaaudit.py                                     |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   E-ITS vastavuskontroll ja Roadmap.                   |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

07_turvaaudit.py - Süsteemi turvaaudit (E-ITS vastavuskontroll).
Võrdleb seadeid standardiga ja annab parandusmeetmed.
"""

import os
import platform
import subprocess

# ASCII Logo (VALVUR standard)
r

def check_windows():
    results = []
    print("[*] Teostan Windowsi turvaauditit...")
    
    # 1. Parooli pikkus
    try:
        out = subprocess.check_output("net accounts", shell=True).decode('cp850')
        min_len = 0
        for line in out.splitlines():
            if "Minimum password length" in line:
                min_len = int(line.split(":")[-1].strip())
        
        status = "PASS" if min_len >= 12 else "FAIL"
        results.append({
            "Kontroll": "Minimaalne parooli pikkus",
            "NIST_Kood": "PR.AC-01",
            "Hetkeseis": f"{min_len} märki",
            "Ootus": "12 märki",
            "Staatus": status,
            "Selgitus": "Liiga lühike parool on kergemini murtav brute-force ründega.",
            "Meede": "net accounts /minpwlen:12"
        })
    except: pass

    # 2. Volume Shadow Copies (vssadmin) - NIST ID.RA-01
    try:
        out = subprocess.check_output("vssadmin list shadows", shell=True).decode('cp850')
        status = "PASS" if "No items found" not in out else "WARNING"
        results.append({
            "Kontroll": "Volume Shadow Copies",
            "NIST_Kood": "ID.RA-01",
            "Hetkeseis": "Olemas" if status == "PASS" else "Puuduvad",
            "Ootus": "Olemasolu",
            "Staatus": status,
            "Selgitus": "Lunavara (Ransomware) kustutab esimesena varukoopiad.",
            "Meede": "Kontrolli vssadmin logisid ja taasta varukoopiad."
        })
    except:
        results.append({
            "Kontroll": "Volume Shadow Copies",
            "Hetkeseis": "VIGA",
            "Ootus": "Olemasolu",
            "Staatus": "FAIL",
            "Selgitus": "vssadmin käivitamine ebaõnnestus. Võimalik ründaja sekkumine.",
            "Meede": "Kontrolli süsteemi terviklust."
        })
    
    return results

def check_linux():
    results = []
    print("[*] Teostan Linuxi turvaauditit...")
    
    # 1. SSH root login
    # ... (olemasolev kood jääb) ...

    # 2. Sudoers NOPASSWD kontroll (Kriitiline privileegide eskaleerimine)
    sudoers_path = "/etc/sudoers"
    if os.path.exists(sudoers_path):
        try:
            # Kasutame grep-i, et leida NOPASSWD ridu
            out = subprocess.check_output(f"grep -r 'NOPASSWD' /etc/sudoers*", shell=True, text=True)
            if out:
                results.append({
                    "Kontroll": "Sudo NOPASSWD",
                    "NIST_Kood": "RS.AN-01",
                    "Hetkeseis": "Leitud riskantsed seaded",
                    "Ootus": "Paroolita sudo keelamine",
                    "Staatus": "FAIL",
                    "Selgitus": "NOPASSWD võimaldab ründajal saada root õigused ilma paroolita.",
                    "Meede": "Eemalda NOPASSWD rida failist /etc/sudoers"
                })
        except subprocess.CalledProcessError:
            results.append({
                "Kontroll": "Sudo NOPASSWD",
                    "NIST_Kood": "RS.AN-01",
                "Hetkeseis": "Puhas",
                "Ootus": "Paroolita sudo keelamine",
                "Staatus": "PASS",
                "Selgitus": "Kõik sudo tegevused vajavad parooli.",
                "Meede": "Pole vajalik"
            })
        except:
            results.append({
                "Kontroll": "Sudo NOPASSWD",
                    "NIST_Kood": "RS.AN-01",
                "Hetkeseis": "LIGIPÄÄS PUUDUB",
                "Ootus": "Kontrollitud",
                "Staatus": "WARNING",
                "Selgitus": "Sudoers faili lugemiseks on vaja sudo õigusi.",
                "Meede": "Käivita skript sudo õigustes."
            })

    # 2. Parooli keerukus (/etc/login.defs)
    if os.path.exists("/etc/login.defs"):
        results.append({
            "Kontroll": "Süsteemne paroolipoliitika",
            "Hetkeseis": "Kontrolli manuaalselt",
            "Ootus": "E-ITS vastavus",
            "Staatus": "INFO",
            "Selgitus": "Kontrolli PASS_MAX_DAYS ja PASS_MIN_LEN väärtusi.",
            "Meede": "nano /etc/login.defs"
        })

    return results

def save_audit_results(results):
    out_file = 'TULEMUSED/07_tulemus_turvaaudit.csv'
    roadmap_file = 'TULEMUSED/07_tulemus_E-ITS_roadmap.txt'
    import csv
    if not results: return
    
    # Salvestame CSV
    keys = results[0].keys()
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
    
    # GENEREERIME E-ITS ROADMAPI (Punkt 48)
    with open(roadmap_file, 'w', encoding='utf-8') as f:
        f.write("VALVUR - E-ITS PARANDUSMEETMETE KAVA (ROADMAP)\n")
        f.write("="*60 + "\n")
        f.write("Järgnevad sammud on vajalikud süsteemi viimiseks vastavusse E-ITS standardiga:\n\n")
        
        counter = 1
        for res in results:
            if res['Staatus'] in ['FAIL', 'WARNING']:
                f.write(f"{counter}. [ ] {res['Kontroll']}\n")
                f.write(f"   MÕJU: {res['Selgitus']}\n")
                f.write(f"   TEGEVUS: {res['Meede']}\n\n")
                counter += 1
        
        if counter == 1:
            f.write("Kõik kontrollitud punktid vastavad nõuetele! Täiendavad sammud pole hetkel vajalikud.\n")

    print(f"[+] Auditi tulemused salvestatud: {out_file}")
    print(f"[+] E-ITS Roadmap loodud: {roadmap_file}")

def main():
    print(LOGO)
    os_type = platform.system()
    if os_type == "Windows":
        res = check_windows()
    else:
        res = check_linux()
    save_audit_results(res)

if __name__ == "__main__":
    main()
