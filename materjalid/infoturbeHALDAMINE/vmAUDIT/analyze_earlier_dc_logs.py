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
#   |   FAILI NIMI:  analyze_earlier_dc_logs.py                           |   #
#   |   LOODUD:      2026-02-05                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Analüüsib domeenikontrolleri turvalogi määratud      |   #
#   |                varasema perioodi kohta, otsides kahtlast tegevust.  |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import sys
import re
import os
from datetime import datetime, timedelta

def analyze_earlier_dc_logs(input_text_file, output_findings_file, start_date_str, end_date_str):
    """
    Analüüsib DC turvalogi varasema perioodi kohta, otsides kahtlast tegevust.
    """
    if not os.path.exists(input_text_file):
        print(f"Viga: Sisendfaili ei leitud: {input_text_file}")
        sys.exit(1)

    findings = []
    mon_map = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }

    try:
        with open(input_text_file, 'r', encoding='utf-8') as f:
            content = f.read()

        event_blocks = re.split(r'Event number\s*:\s*\d+', content)[1:]

        start_date = datetime.strptime(start_date_str, "%b %d, %Y")
        end_date = datetime.strptime(end_date_str, "%b %d, %Y")

        target_users = ["Administrator", "jaak-admin", "peeter.meeter", "kalle.kartul", "rpd7service", "Pille.Porgand", "pille.porgand"]
        relevant_event_ids = ["4624", "4625", "4720", "4728", "4688"] # Logon, Logoff, Account Creation, Group Change, Process Creation

        for block in event_blocks:
            creation_time_match = re.search(r'Creation time\s*:\s*(.+? UTC)', block)
            if creation_time_match:
                creation_time_str = creation_time_match.group(1).strip()
                
                # Convert 'Nov 16, 2025' to '11 16, 2025' for datetime parsing
                parsed_date_str = creation_time_str
                for mon_abbr, mon_num in mon_map.items():
                    parsed_date_str = parsed_date_str.replace(mon_abbr, mon_num)
                
                # Further refine to remove day, year, time for date comparison
                date_only_str = re.search(r'(\d{2} \d{2}, \d{4})', parsed_date_str).group(1)
                event_date = datetime.strptime(date_only_str, "%m %d, %Y")

                if start_date <= event_date <= end_date:
                    event_id_match = re.search(r'Event identifier\s*:\s*0x[0-9a-fA-F]+\s*\((\d{4})\)', block)
                    username_match = re.search(r'(String:\s*6\s*:\s*(.+)|String:\s*2\s*:\s*(.+))', block) # Check both String:6 and String:2 for username
                    
                    event_id = event_id_match.group(1) if event_id_match else "N/A"
                    username = "N/A"
                    if username_match:
                        # Prioritize String:6 if present, otherwise String:2
                        if username_match.group(2): # String:6
                            username = username_match.group(2).strip()
                        elif username_match.group(3): # String:2
                            username = username_match.group(3).strip()

                    
                    # Kontrollime, kas sündmus on seotud huvipakkuvate kasutajatega või sündmuse ID-dega
                    is_relevant_user = any(user.lower() in username.lower() for user in target_users)
                    is_relevant_event_id = event_id in relevant_event_ids
                    
                    if is_relevant_user or is_relevant_event_id:
                        findings.append(f"LEID (Varasem tegevus {event_date.strftime('%b %d, %Y')}):\n  Aeg: {creation_time_str}\n  Sündmuse ID: {event_id}\n  Kasutajanimi: {username}\n  Detailid: {block[:300]}...\n")

    except Exception as e:
        print(f"Viga logifaili analüüsimisel: {e}")
        sys.exit(1)

    with open(output_findings_file, 'w', encoding='utf-8') as outfile:
        if findings:
            for finding in findings:
                outfile.write(finding + "\n")
            print(f"Analüüsi tulemused salvestati edukalt faili '{output_findings_file}'")
        else:
            outfile.write(f"Varasemast perioodist ({start_date_str} - {end_date_str}) kahtlast tegevust ei leitud.\n")
            print(f"Varasemast perioodist ({start_date_str} - {end_date_str}) kahtlast tegevust ei leitud. Tulemused salvestati faili '{output_findings_file}'")


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Kasutus: python analyze_earlier_dc_logs.py <sisend_teksti_fail> <väljund_leidude_fail> <alguskuupäev_format_MMM_DD_YYYY> <lõppkuupäev_format_MMM_DD_YYYY>")
        sys.exit(1)

    input_text = sys.argv[1]
    output_findings = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]

    analyze_earlier_dc_logs(input_text, output_findings, start_date, end_date)