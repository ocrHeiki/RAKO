###############################################################################
#                                                                             #
#   █████   █████           ████                                              #
#  ▒▒███   ▒▒███           ▒▒███                                              #
#   ▒███    ▒███   ██████   ▒███  █████ █████ █████ ████ ████████             #
#   ▒███    ▒▒███ ▒▒▒▒▒███  ▒███ ▒▒███ ▒▒███ ▒▒███ ▒███ ▒▒███▒▒███            #
#   ▒▒███   ███    ███████  ▒███  ▒███  ▒███  ▒███ ▒███  ▒███ ▒▒▒             #
#    ▒▒▒█████▒    ███▒▒███  ▒███  ▒▒███ ███   ▒███ ▒███  ▒███                 #
#      ▒▒███     ▒▒████████ █████  ▒▒█████    ▒▒████████ █████                #
#       ▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒      ▒▒▒▒▒▒▒▒ ▒▒▒▒▒                 #
#                                                                             #
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  find_downloads.py                                    |   #
#   |   LOODUD:      2026-02-05                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Skript otsib logifailidest allalaadimiste ja         |   #
#   |                failiedastuste indikaatoreid.                        |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import re
import sys
import os
import argparse

def find_downloads(log_file_path, custom_filename_pattern=None):
    """
    Otsib logifailist allalaadimiste ja failiedastuste indikaatoreid.
    """
    if not os.path.exists(log_file_path):
        print(f"Viga: Logifaili ei leitud: {log_file_path}")
        return

    # Tavallised märksõnad ja regulaaravaldised allalaadimiste tuvastamiseks
    # Fookus on Event ID 4688 (Process Creation) puhul käsurea argumentidel.
    download_patterns = [
        re.compile(r'wget', re.IGNORECASE),
        re.compile(r'curl', re.IGNORECASE),
        re.compile(r'Invoke-WebRequest', re.IGNORECASE),
        re.compile(r'Invoke-RestMethod', re.IGNORECASE),
        re.compile(r'BITSAdmin', re.IGNORECASE),
        re.compile(r'Certutil\s+-urlcache\s+-f', re.IGNORECASE),
        re.compile(r'http[s]?:\/\/', re.IGNORECASE), # URL-id käsureal
        re.compile(r'\.(exe|dll|zip|rar|7z|ps1|js|vbs|hta|bat|cmd)', re.IGNORECASE), # Tüüpilised pahatahtlikud faililaiendid
    ]

    found_downloads = []
    current_event = []
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line.startswith("LEID ("):
                if current_event:
                    process_event(found_downloads, current_event, download_patterns, custom_filename_pattern)
                current_event = [line.strip()]
            else:
                current_event.append(line.strip())
        # Töötle viimane sündmus
        if current_event:
            process_event(found_downloads, current_event, download_patterns, custom_filename_pattern)

    if found_downloads:
        print(f"\nLeitud potentsiaalsed allalaadimiste indikaatorid failist '{log_file_path}':")
        for finding in found_downloads:
            print(finding)
    else:
        print(f"\nFailist '{log_file_path}' ei leitud ühtegi allalaadimise indikaatorit.")

def process_event(found_downloads_list, event_lines, patterns, custom_pattern):
    """
    Töötleb üksikut sündmusekirjet allalaadimiste indikaatorite leidmiseks.
    """
    event_text = "\n".join(event_lines)

    # Otsi Event ID 4688 (Process Creation) käsurida
    if "Sündmuse ID: 4688" in event_text:
        command_line_match = re.search(r'Käsurida:\s*(.+)', event_text)
        if command_line_match:
            command_line = command_line_match.group(1)
            
            # Kontrolli tavalisi allalaadimismustreid
            for pattern in patterns:
                if pattern.search(command_line):
                    found_downloads_list.append(f"\nPotentsiaalne allalaadimine (Event ID 4688):\n{event_text}")
                    return # Lisa ainult üks kord leitud sündmuse kohta

            # Kontrolli kohandatud failinime mustrit
            if custom_pattern and re.search(custom_pattern, command_line, re.IGNORECASE):
                found_downloads_list.append(f"\nPotentsiaalne allalaadimine (Event ID 4688, kohandatud failinimi '{custom_pattern}'):\n{event_text}")
                return

    # Laiendatud otsing faililaiendite ja URL-ide järgi ka muudes sündmustes
    # See võib olla mürarikas, aga kasutaja soovis kõike
    for pattern in patterns:
        if pattern.search(event_text):
            # Veendu, et see ei ole juba lisatud 4688 sündmus
            if "Sündmuse ID: 4688" in event_text:
                command_line_match = re.search(r'Käsurida:\s*(.+)', event_text)
                if command_line_match and pattern.search(command_line_match.group(1)):
                    continue # Juba Event ID 4688 kontrollis tuvastatud
            
            found_downloads_list.append(f"\nPotentsiaalne allalaadimine (laiendatud otsing):\n{event_text}")
            return # Lisa ainult üks kord leitud sündmuse kohta


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Otsib logifailidest allalaadimiste ja failiedastuste indikaatoreid.")
    parser.add_argument("log_file", help="Logifaili tee, mida analüüsida.")
    parser.add_argument("--filename", help="Valikuline: Spetsiifiline failinime muster, mida otsida (regulaaravaldis).", default=None)
    
    args = parser.parse_args()
    
    find_downloads(args.log_file, args.filename)
