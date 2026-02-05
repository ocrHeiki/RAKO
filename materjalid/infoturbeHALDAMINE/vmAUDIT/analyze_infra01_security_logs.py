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
#   |   FAILI NIMI:  analyze_infra01_security_logs.py                     |   #
#   |   LOODUD:      2026-02-05                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Analüüsib rakendusserveri turvalogi intsidendi       |   #
#   |                kuupäeval, otsides sisselogimiskatseid ja kahtlasi   |   #
#   |                protsesse.                                           |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import subprocess
import sys
import re
import os

def analyze_infra01_security_logs(input_text_file, output_findings_file, incident_date="Nov 16, 2025"):
    """
    Analüüsib TRL-INFRA01 turvalogi kindla intsidendi kuupäeva kohta,
    otsides brute-force rünnaku katseid ja edukaid sisselogimisi.
    """
    if not os.path.exists(input_text_file):
        print(f"Viga: Sisendfaili ei leitud: {input_text_file}")
        sys.exit(1)

    findings = []
    
    # Brute-force periood: 09:01 kuni 09:51 UTC
    brute_force_start_time = "09:01"
    brute_force_end_time = "09:51"

    # Otsime ebaõnnestunud sisselogimiskatseid (Event ID 4625)
    # ja edukaid sisselogimisi (Event ID 4624) intsidendi kuupäeval
    try:
        with open(input_text_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Regex mustrid sündmuste ja nende detailide leidmiseks
        # Kasutame paindlikumat mustrit, et leida Event ID-d ja kuupäeva
        event_blocks = re.split(r'Event number\s*:\s*\d+', content)[1:] # Jaotame sündmuseplokkideks

        for block in event_blocks:
            if incident_date not in block:
                continue

            creation_time_match = re.search(r'Creation time\s*:\s*(.+? UTC)', block)
            event_id_match = re.search(r'Event identifier\s*:\s*0x[0-9a-fA-F]+\s*\((\d{4})\)', block)
            username_match = re.search(r'String:\s*6\s*:\s*(.+)', block)
            ip_address_match = re.search(r'String:\s*19\s*:\s*(.+)', block)

            if creation_time_match and event_id_match:
                creation_time_str = creation_time_match.group(1).strip()
                event_id = event_id_match.group(1)
                username = username_match.group(1).strip() if username_match else "N/A"
                ip_address = ip_address_match.group(1).strip() if ip_address_match else "N/A"
                
                # Ekstraheerime kellaaja sündmuse loomise ajast
                time_part_match = re.search(r'(\d{2}):(\d{2}):\d{2}', creation_time_str)
                if time_part_match:
                    event_hour = int(time_part_match.group(1))
                    event_minute = int(time_part_match.group(2))

                    # Kontrollime, kas sündmus jääb brute-force perioodi
                    is_in_brute_force_period = False
                    if event_hour == int(brute_force_start_time.split(':')[0]): # Tund on 09
                        if event_minute >= int(brute_force_start_time.split(':')[1]) and event_minute <= int(brute_force_end_time.split(':')[1]):
                            is_in_brute_force_period = True
                    elif event_hour == int(brute_force_end_time.split(':')[0]) and event_minute <= int(brute_force_end_time.split(':')[1]):
                         is_in_brute_force_period = True


                    if event_id == "4625" and is_in_brute_force_period:
                        failure_reason_match = re.search(r'String:\s*9\s*:\s*(.+)', block)
                        failure_reason = failure_reason_match.group(1).strip() if failure_reason_match else "N/A"
                        findings.append(f"LEID (Ebaõnnestunud sisselogimine - {incident_date}):\n  Aeg: {creation_time_str}\n  Kasutajanimi: {username}\n  IP-aadress: {ip_address}\n  Vea põhjus: {failure_reason}\n")
                    elif event_id == "4624" and is_in_brute_force_period:
                        logon_type_match = re.search(r'String:\s*9\s*:\s*(\d+)', block) # Logon Type for 4624 is String:9
                        logon_type = logon_type_match.group(1) if logon_type_match else "N/A"
                        findings.append(f"LEID (Edukas sisselogimine - {incident_date}):\n  Aeg: {creation_time_str}\n  Kasutajanimi: {username}\n  IP-aadress: {ip_address}\n  Sisselogimise tüüp: {logon_type}\n")
                    elif ("nmap.exe" in block or "chrome.exe" in block) and incident_date in creation_time_str and (event_id == "4688" or event_id == "5156" or event_id == "5145"):
                        process_name_match = re.search(r'String:\s*6\s*:\s*(.+)', block)
                        process_name = process_name_match.group(1).strip() if process_name_match else "N/A"
                        command_line_match = re.search(r'String:\s*9\s*:\s*(.+)', block)
                        command_line = command_line_match.group(1).strip() if command_line_match else "N/A"
                        findings.append(f"LEID (Kahtlane protsess - {incident_date}):\n  Aeg: {creation_time_str}\n  Protsess: {process_name}\n  Käsurida: {command_line}\n")
                    elif "pille.porgand" in block and incident_date in creation_time_str and (event_id == "5140" or event_id == "5145"):
                         share_name_match = re.search(r'String:\s*8\s*:\s*(.+)', block)
                         share_name = share_name_match.group(1).strip() if share_name_match else "N/A"
                         findings.append(f"LEID (Pille Porgandi juurdepääs jagatud kaustale - {incident_date}):\n  Aeg: {creation_time_str}\n  Juurdepääs: {share_name}\n")
                        

    except Exception as e:
        print(f"Viga logifaili analüüsimisel: {e}")
        sys.exit(1)

    with open(output_findings_file, 'w', encoding='utf-8') as outfile:
        if findings:
            for finding in findings:
                outfile.write(finding + "\n")
            print(f"Analüüsi tulemused salvestati edukalt faili '{output_findings_file}'")
        else:
            outfile.write(f"Intsidendi kuupäeval ({incident_date}) TRL-INFRA01 turvalogist kahtlast tegevust ei leitud.\n")
            print(f"Intsidendi kuupäeval ({incident_date}) TRL-INFRA01 turvalogist kahtlast tegevust ei leitud. Tulemused salvestati faili '{output_findings_file}'")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kasutus: python analyze_infra01_security_logs.py <sisend_teksti_fail> <väljund_leidude_fail>")
        sys.exit(1)

    input_text = sys.argv[1]
    output_findings = sys.argv[2]
    analyze_infra01_security_logs(input_text, output_findings)