#!/usr/bin/env python3
import os, csv, re, base64

# ASCII Logo (VALVUR standard)
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
#   |   FAILI NIMI:  04_powershell_dekodeerimine.py                       |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   PowerShell Base64 ja XOR dekodeerimine.              |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

def decode_ps_payload(text):
    """Otsib ja dekodeerib PowerShell Base64 sisu (UTF-16LE)."""
    b64_pattern = r'[A-Za-z0-9+/]{40,}'
    matches = re.findall(b64_pattern, text)
    decoded_list = []
    for m in matches:
        try:
            raw_data = base64.b64decode(m)
            decoded = raw_data.decode('utf-16-le', errors='ignore')
            if any(k in decoded.lower() for k in ['http', 'iex', 'invoke', 'net.webclient']):
                decoded_list.append(decoded.strip())
        except: continue
    return decoded_list

def run_deep_forensics():
    # Võtame sisendiks nii märksõnade tulemused kui ka üldise turvafiltreeringu (sest 4104 võib seal olla)
    input_files = ['TULEMUSED/02_tulemus_turvafiltreering.csv', 'TULEMUSED/03_tulemus_kahtlased_marksonad.csv']
    out_report = 'TULEMUSED/04_tulemus_suvaanaluusi_raport.txt'
    
    findings = 0
    processed_records = set() # Väldime duplikaate
    
    with open(out_report, mode='w', encoding='utf-8') as f_out:
        f_out.write("VALVUR - SÜVAANALÜÜSI JA DEKODEERIMISE RAPORT\n" + "="*70 + "\n\n")
        
        for in_file in input_files:
            if not os.path.exists(in_file): continue
            with open(in_file, mode='r', encoding='utf-8') as f_in:
                reader = csv.DictReader(f_in)
                for row in reader:
                    # Loome unikaalse ID kirjele (RecordId + MachineName)
                    rec_id = f"{row.get('RecordId')}_{row.get('MachineName')}"
                    if rec_id in processed_records: continue
                    
                    msg = row.get('Message', '')
                    decoded_scripts = decode_ps_payload(msg)
                    ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', msg + "".join(decoded_scripts))
                    
                    if decoded_scripts or ips:
                        processed_records.add(rec_id)
                        findings += 1
                        f_out.write(f"LEID #{findings} | Aeg: {row.get('TimeCreated')} | EventID: {row.get('Id')}\n")
                        if ips: f_out.write(f"  [!] IP-D: {', '.join(set(ips))}\n")
                        if decoded_scripts:
                            for i, script in enumerate(decoded_scripts):
                                f_out.write(f"  [>>>] DEKODEERITUD SKRIPT #{i+1}:\n{script}\n")
                        f_out.write("-" * 40 + "\n\n")
    print(f"VALMIS! Süvaanalüüs tuvastas {findings} sündmust. Raport: {out_report}")

if __name__ == "__main__":
    print(LOGO)
    run_deep_forensics()
