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
#   |   FAILI NIMI:  analyze_infra01_application_logs.py                  |   #
#   |   LOODUD:      2026-02-05                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Analüüsib rakendusserveri rakenduslogi intsidendi    |   #
#   |                kuupäeval, otsides PostgreSQL-i vigu ja muid         |   #
#   |                kriitilisi rakendusvigu.                             |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import subprocess
import sys
import re
import os

def analyze_infra01_application_logs(input_text_file, output_findings_file, incident_date="Nov 16, 2025"):
    """
    Analüüsib TRL-INFRA01 rakenduslogi kindla intsidendi kuupäeva kohta,
    otsides PostgreSQL-i vigu ja väljalülitamisi.
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
            event_id_match = re.search(r'Event identifier\s*:\s*0x[0-9a-fA-F]+\s*\((\d+)\)', block)
            event_level_match = re.search(r'Event level\s*:\s*(.+)', block)
            source_name_match = re.search(r'Source name\s*:\s*(.+)', block)
            
            if creation_time_match and event_id_match and source_name_match:
                creation_time_str = creation_time_match.group(1).strip()
                event_id = event_id_match.group(1)
                event_level = event_level_match.group(1).strip() if event_level_match else "N/A"
                source_name = source_name_match.group(1).strip()
                
                # Otsime PostgreSQL-i vigu ja väljalülitamisi
                if source_name == "PostgreSQL" and (event_level.startswith("Error") or "shutdown" in block.lower()):
                    details = re.search(r'String:\s*1\s*:\s*(.+)', block)
                    detail_str = details.group(1).strip() if details else "N/A"
                    findings.append(f"LEID (PostgreSQL viga/väljalülitamine - {incident_date}):\n  Aeg: {creation_time_str}\n  Sündmuse ID: {event_id}\n  Sündmuse tase: {event_level}\n  Detailid: {detail_str}\n")
                elif event_level.startswith("Error") or event_level.startswith("Critical"):
                    findings.append(f"LEID (Kriitiline rakendusviga - {incident_date}):\n  Aeg: {creation_time_str}\n  Sündmuse ID: {event_id}\n  Sündmuse tase: {event_level}\n  Allikas: {source_name}\n  Sündmuse detailid: {block[:200]}...\n")

    except Exception as e:
        print(f"Viga logifaili analüüsimisel: {e}")
        sys.exit(1)

    with open(output_findings_file, 'w', encoding='utf-8') as outfile:
        if findings:
            for finding in findings:
                outfile.write(finding + "\n")
            print(f"Analüüsi tulemused salvestati edukalt faili '{output_findings_file}'")
        else:
            outfile.write(f"Intsidendi kuupäeval ({incident_date}) TRL-INFRA01 rakenduslogist kahtlast tegevust ei leitud.\n")
            print(f"Intsidendi kuupäeval ({incident_date}) TRL-INFRA01 rakenduslogist kahtlast tegevust ei leitud. Tulemused salvestati faili '{output_findings_file}'")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kasutus: python analyze_infra01_application_logs.py <sisend_teksti_fail> <väljund_leidude_fail>")
        sys.exit(1)

    input_text = sys.argv[1]
    output_findings = sys.argv[2]
    analyze_infra01_application_logs(input_text, output_findings)