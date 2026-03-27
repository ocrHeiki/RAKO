#!/usr/bin/env python3
"""
01_konverteering_evtx_csv.py - Windowsi .evtx logide konverteerimine CSV-formaati.
Kasutamine: python3 SKRIPTID/01_konverteering_evtx_csv.py --path LOGID
"""

import os # Impordime mooduli operatsioonisüsteemi failitoiminguteks
import csv # Impordime mooduli CSV failide kirjutamiseks
import argparse # Impordime mooduli käsurea argumentide töötlemiseks
import xml.etree.ElementTree as ET # Impordime XML-i töötlemise mooduli
from Evtx.Evtx import Evtx # Impordime spetsiaalse teegi .evtx failide lugemiseks

# ASCII Logo ja metainfo definitsioon
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
#   |   LOODUD:      26.03.2026                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Konverteerib .evtx logid CSV formaati.               |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def parse_evtx(evtx_path, out_csv):
    """Funktsioon ühe .evtx faili konverteerimiseks CSV-ks."""
    # Määrame CSV faili veerud
    headers = ['TimeCreated', 'Id', 'LevelDisplayName', 'Message', 'MachineName', 'RecordId']
    
    try:
        # Avame väljundfaili kirjutamiseks (UTF-8 koodingus)
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader() # Kirjutame päiseriba
            
            # Avame .evtx faili kasutades Evtx teeki
            with Evtx(evtx_path) as log:
                # Käime läbi kõik logikirjed
                for record in log.records():
                    try:
                        # Võtame kirje XML-kujul
                        xml_str = record.xml()
                        # Eemaldame XML nimeruumi, et otsing oleks lihtsam
                        xml_str = xml_str.replace(' xmlns="http://schemas.microsoft.com/win/2004/08/events/event"', '')
                        root = ET.fromstring(xml_str) # Parsime XML-i
                        
                        # Leiame süsteemse sündmuse info (System ja EventData sektsioonid)
                        system = root.find('System')
                        event_data = root.find('EventData')
                        
                        # Eraldame vajalikud väljad XML-ist
                        event_id = system.find('EventID').text if system.find('EventID') is not None else "N/A"
                        time_created = system.find('TimeCreated').attrib.get('SystemTime') if system.find('TimeCreated') is not None else "N/A"
                        machine_name = system.find('Computer').text if system.find('Computer') is not None else "N/A"
                        record_id = system.find('EventRecordID').text if system.find('EventRecordID') is not None else "N/A"
                        level = system.find('Level').text if system.find('Level') is not None else "N/A"
                        
                        # Kogume kokku täiendava sündmuse info (EventData elemendid)
                        msg_parts = []
                        if event_data is not None:
                            for data in event_data.findall('Data'):
                                name = data.attrib.get('Name', '')
                                val = data.text if data.text else ""
                                msg_parts.append(f"{name}: {val}")
                        
                        message = " | ".join(msg_parts) # Ühendame info üheks tekstiks
                        
                        # Kirjutame rea CSV faili
                        writer.writerow({
                            'TimeCreated': time_created,
                            'Id': event_id,
                            'LevelDisplayName': level,
                            'Message': message,
                            'MachineName': machine_name,
                            'RecordId': record_id
                        })
                    except Exception:
                        # Kui ühe kirje lugemine ebaõnnestub, liigume edasi järgmise juurde
                        continue
        print(f"SALVESTATUD: {out_csv}")
    except Exception as e:
        print(f"VIGA: Ei saanud faili {evtx_path} konverteerida: {e}")

def main():
    """Skripti põhifunktsioon."""
    print(LOGO) # Kuvame logo
    # Seadistame käsurea argumentide töötleja
    parser = argparse.ArgumentParser(description="Windowsi .evtx -> CSV konverter")
    parser.add_argument("--path", default="LOGID", help="Kaust, kus asuvad .evtx failid")
    args = parser.parse_args()
    
    out_dir = "TULEMUSED"
    # Loome tulemuste kausta, kui seda veel pole
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Käime läbi etteantud kausta ja otsime .evtx faile
    for root, dirs, files in os.walk(args.path):
        for file in files:
            if file.lower().endswith('.evtx'):
                evtx_full_path = os.path.join(root, file)
                # Puhastame failinime väljundi jaoks
                clean_name = file.replace('.evtx', '').replace('%4', '_')
                out_name = os.path.join(out_dir, f"01_tulemus_eksport_{clean_name}.csv")
                parse_evtx(evtx_full_path, out_name)

if __name__ == "__main__":
    main() # Käivitame peaprogrammi
