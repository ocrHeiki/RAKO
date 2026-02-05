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
#   |   FAILI NIMI:  analyze_infra01_system_logs.py                       |   #
#   |   LOODUD:      2026-02-05                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Analüüsib rakendusserveri süsteemilogi intsidendi    |   #
#   |                kuupäeval, otsides süsteemi väljalülitamisi ja       |   #
#   |                kriitilisi vigu.                                     |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import subprocess
import sys
import re
import os

def analyze_infra01_system_logs(input_text_file, output_findings_file, incident_date="Nov 16, 2025"):
    """
    Analüüsib TRL-INFRA01 süsteemilogi kindla intsidendi kuupäeva kohta,
    otsides süsteemi väljalülitamisi ja taaskäivitamisi.
    """
    if not os.path.exists(input_text_file):
        print(f"Viga: Sisendfaili ei leitud: {input_text_file}")
        sys.exit(1)

    findings = []

    try:
        with open(input_text_file, 'r', encoding='utf-8') as f:
            content = f.read()

        event_blocks = re.split(r'Event number\s*:\s*\d+', content)[1:]

        for block in event_blocks:
            if incident_date not in block:
                continue
            
            creation_time_match = re.search(r'Creation time\s*:\s*(.+? UTC)', block)
            event_id_match = re.search(r'Event identifier\s*:\s*0x[0-9a-fA-F]+\s*\((\d{4})\)', block)
            event_level_match = re.search(r'Event level\s*:\s*(.+)', block)
            
            if creation_time_match and event_id_match:
                creation_time_str = creation_time_match.group(1).strip()
                event_id = event_id_match.group(1)
                event_level = event_level_match.group(1).strip() if event_level_match else "N/A"

                # Süsteemi väljalülitamised/taaskäivitamised
                if event_id == "6008":
                    findings.append(f"LEID (Ootamatu süsteemi väljalülitamine - {incident_date}):\n  Aeg: {creation_time_str}\n  Sündmuse tase: {event_level}\n")
                elif event_id == "1074":
                    user_match = re.search(r'String:\s*7\s*:\s*(.+)', block) # Kasutajanimi sündmuse ID 1074 jaoks
                    user = user_match.group(1).strip() if user_match else "N/A"
                    findings.append(f"LEID (Kasutaja algatatud väljalülitamine - {incident_date}):\n  Aeg: {creation_time_str}\n  Sündmuse tase: {event_level}\n  Kasutaja: {user}\n")
                elif event_id == "6006":
                    findings.append(f"LEID (Sündmuselogi teenus peatati - {incident_date}):\n  Aeg: {creation_time_str}\n  Sündmuse tase: {event_level}\n")
                elif event_level.startswith("Error") or event_level.startswith("Critical"):
                    findings.append(f"LEID (Kriitiline süsteemiviga - {incident_date}):\n  Aeg: {creation_time_str}\n  Sündmuse ID: {event_id}\n  Sündmuse tase: {event_level}\n  Sündmuse detailid: {block[:200]}...\n")

    except Exception as e:
        print(f"Viga logifaili analüüsimisel: {e}")
        sys.exit(1)

    with open(output_findings_file, 'w', encoding='utf-8') as outfile:
        if findings:
            for finding in findings:
                outfile.write(finding + "\n")
            print(f"Analüüsi tulemused salvestati edukalt faili '{output_findings_file}'")
        else:
            outfile.write(f"Intsidendi kuupäeval ({incident_date}) TRL-INFRA01 süsteemilogist kahtlast tegevust ei leitud.\n")
            print(f"Intsidendi kuupäeval ({incident_date}) TRL-INFRA01 süsteemilogist kahtlast tegevust ei leitud. Tulemused salvestati faili '{output_findings_file}'")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kasutus: python analyze_infra01_system_logs.py <sisend_teksti_fail> <väljund_leidude_fail>")
        sys.exit(1)

    input_text = sys.argv[1]
    output_findings = sys.argv[2]
    analyze_infra01_system_logs(input_text, output_findings)