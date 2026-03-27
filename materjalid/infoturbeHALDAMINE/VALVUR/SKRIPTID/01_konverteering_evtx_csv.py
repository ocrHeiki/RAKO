#!/usr/bin/env python3
"""
01_konverteering_evtx_csv.py - Windowsi .evtx logide konverteerimine CSV-formaati.
Kasutamine: python3 SKRIPTID/01_konverteering_evtx_csv.py --path LOGID
"""

import os
import csv
import argparse
import xml.etree.ElementTree as ET
from Evtx.Evtx import Evtx

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
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  01_konverteering_evtx_csv.py                         |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Konverteerib .evtx logid CSV formaati.               |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def parse_evtx(evtx_path, out_csv):
    """Konverteerib ühe .evtx faili CSV-ks."""
    headers = ['TimeCreated', 'Id', 'LevelDisplayName', 'Message', 'MachineName', 'RecordId']
    
    try:
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            with Evtx(evtx_path) as log:
                for record in log.records():
                    try:
                        xml_str = record.xml()
                        xml_str = xml_str.replace(' xmlns="http://schemas.microsoft.com/win/2004/08/events/event"', '')
                        root = ET.fromstring(xml_str)
                        
                        system = root.find('System')
                        event_data = root.find('EventData')
                        
                        event_id = system.find('EventID').text if system.find('EventID') is not None else "N/A"
                        time_created = system.find('TimeCreated').attrib.get('SystemTime') if system.find('TimeCreated') is not None else "N/A"
                        machine_name = system.find('Computer').text if system.find('Computer') is not None else "N/A"
                        record_id = system.find('EventRecordID').text if system.find('EventRecordID') is not None else "N/A"
                        level = system.find('Level').text if system.find('Level') is not None else "N/A"
                        
                        msg_parts = []
                        if event_data is not None:
                            for data in event_data.findall('Data'):
                                name = data.attrib.get('Name', '')
                                val = data.text if data.text else ""
                                msg_parts.append(f"{name}: {val}")
                        
                        message = " | ".join(msg_parts)
                        writer.writerow({
                            'TimeCreated': time_created,
                            'Id': event_id,
                            'LevelDisplayName': level,
                            'Message': message,
                            'MachineName': machine_name,
                            'RecordId': record_id
                        })
                    except Exception:
                        continue
        print(f"SALVESTATUD: {out_csv}")
    except Exception as e:
        print(f"VIGA: Ei saanud faili {evtx_path} konverteerida: {e}")

def main():
    print(LOGO)
    parser = argparse.ArgumentParser(description="Windowsi .evtx -> CSV konverter")
    parser.add_argument("--path", default="LOGID", help="Kaust, kus asuvad .evtx failid")
    args = parser.parse_args()
    
    out_dir = "TULEMUSED"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.lower().endswith('.evtx'):
                evtx_full_path = os.path.join(root, file)
                clean_name = file.replace('.evtx', '').replace('%4', '_')
                out_name = os.path.join(out_dir, f"01_tulemus_eksport_{clean_name}.csv")
                parse_evtx(evtx_full_path, out_name)

if __name__ == "__main__":
    main()
