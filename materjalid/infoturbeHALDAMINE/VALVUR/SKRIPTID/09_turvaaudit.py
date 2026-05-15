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
#   |   FAILI NIMI:  09_turvaaudit.py                                     |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   Vastavuskontroll ja E-ITS parandusmeetmete kava      |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import csv

def run_audit():
    out_dir = os.environ.get("VALVUR_OUT", "TULEMUSED")
    
    # Simuleerime auditi tulemusi tuginedes E-ITS standardile
    results = [
        {"Kontroll": "SSH Parooliautentimine", "Staatus": "FAIL", "Meede": "Kasuta ainult võtmepõhist sisselogimist."},
        {"Kontroll": "Logide säilitusaeg", "Staatus": "WARNING", "Meede": "Pikenda logide hoidmist 90 päevani."},
        {"Kontroll": "Kasutajaõiguste audit", "Staatus": "OK", "Meede": "Nõuetele vastav."}
    ]
    
    out_file = os.path.join(out_dir, "09_tulemus_turvaaudit.csv")
    roadmap_file = os.path.join(out_dir, "09_tulemus_E-ITS_roadmap.txt")
    
    with open(out_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
        
    with open(roadmap_file, 'w', encoding='utf-8') as f:
        f.write("VALVUR - E-ITS ROADMAP (TEGEVUSKAVA)\n" + "="*40 + "\n")
        for r in results:
            if r['Staatus'] != "OK":
                f.write(f"[*] {r['Kontroll']}: {r['Meede']}\n")
    
    print(f"[OK] Audit ja Roadmap loodud kausta: {out_dir}")

if __name__ == "__main__":
    run_audit()
