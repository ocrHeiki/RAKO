#!/usr/bin/env python3
"""
01_konverteering_evtx_csv.py - Windowsi .evtx logide konverteerimine CSV-formaati.
Kasutamine: python3 SKRIPTID/01_konverteering_evtx_csv.py --path LOGID
"""

import os # Impordime mooduli operatsioonisüsteemi failitoiminguteks
import csv # Impordime mooduli CSV failide kirjutamiseks
import argparse # Impordime mooduli käsurea argumentide töötlemiseks
import xml.etree.ElementTree as ET # Impordime XML-i töötlemise mooduli
import shutil # Moodul failide kopeerimiseks
import tempfile # Moodul ajutiste failide loomiseks
from Evtx.Evtx import Evtx # Impordime spetsiaalse teegi .evtx failide lugemiseks

# ASCII Logo ja metainfo definitsioon
r

def parse_evtx(evtx_path, out_csv):
    """Funktsioon ühe .evtx faili konverteerimiseks CSV-ks."""
    headers = ['TimeCreated', 'Id', 'LevelDisplayName', 'Message', 'MachineName', 'RecordId']
    
    # KUI FAIL ON LUKUS (nt reaalajas süsteemis), TEE AJUTINE KOOPIA
    temp_dir = tempfile.gettempdir()
    temp_evtx = os.path.join(temp_dir, os.path.basename(evtx_path))
    
    try:
        shutil.copy2(evtx_path, temp_evtx)
        path_to_analyze = temp_evtx
    except:
        path_to_analyze = evtx_path

    try:
        with open(out_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            with Evtx(path_to_analyze) as log:
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
                    except: continue
        print(f"SALVESTATUD: {out_csv}")
    except Exception as e:
        print(f"VIGA: {evtx_path} -> {e}")
    finally:
        # Kustutame ajutise faili, kui see loodi
        if path_to_analyze == temp_evtx and os.path.exists(temp_evtx):
            try: os.remove(temp_evtx)
            except: pass

def main():
    print(LOGO)
    parser = argparse.ArgumentParser(description="Windowsi .evtx -> CSV konverter")
    parser.add_argument("--path", default="LOGID", help="Kaust, kus asuvad .evtx failid")
    parser.add_argument("--live", action="store_true", help="Võta logid otse süsteemsest kataloogist")
    args = parser.parse_args()
    
    source_path = args.path
    if args.live:
        # LIVE režiimis kopeerime failid esmalt oma kontrolli alla
        system_logs = r"C:\Windows\System32\winevt\Logs"
        print(f"[*] REŽIIM: LIVE (Kopeerin logid: {system_logs} -> {args.path})")
        if not os.path.exists(args.path): os.makedirs(args.path)
        
        for f_name in ["Security.evtx", "System.evtx", "Application.evtx"]:
            src = os.path.join(system_logs, f_name)
            dst = os.path.join(args.path, f_name)
            if os.path.exists(src):
                try:
                    shutil.copy2(src, dst)
                    print(f"  [+] Kopeeritud: {f_name}")
                except Exception as e:
                    print(f"  [!] Ei saanud faili {f_name} kopeerida: {e}")
        source_path = args.path

    out_dir = "TULEMUSED"
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    for root, dirs, files in os.walk(source_path):
        for file in files:
            if file.lower().endswith('.evtx'):
                evtx_full_path = os.path.join(root, file)
                clean_name = file.replace('.evtx', '').replace('%4', '_')
                out_name = os.path.join(out_dir, f"01_tulemus_eksport_{clean_name}.csv")
                parse_evtx(evtx_full_path, out_name)

if __name__ == "__main__":
    main() # Käivitame peaprogrammi
