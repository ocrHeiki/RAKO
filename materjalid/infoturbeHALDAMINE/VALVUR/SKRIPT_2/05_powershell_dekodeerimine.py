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
#   |   FAILI NIMI:  05_powershell_dekodeerimine.py                       |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   PowerShell Base64 ja XOR deobfuskatsioon.            |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################
"""

import os
import sys
import csv
import re
import base64

sys.path.append(os.path.join(os.path.dirname(__file__), "."))
import utils

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
###############################################################################
"""

logger = utils.setup_logging("PS_DECODE")

def xor_decrypt(data, key):
    return bytearray([b ^ key for b in data])

def find_xor_payloads(text):
    hex_pattern = r'(?:0x[0-9a-fA-F]{2}[, ]*){8,}'
    matches = re.findall(hex_pattern, text)
    results = []
    for m in matches:
        try:
            bytes_data = bytearray([int(x.strip(), 16) for x in m.split(",") if x.strip()])
            for key in range(1, 256):
                dec = xor_decrypt(bytes_data, key)
                try:
                    dec_str = dec.decode('ascii', errors='ignore').lower()
                    if any(k in dec_str for k in ['http', 'iex', 'invoke', 'cmd', 'powershell']):
                        results.append(f"XOR (Võti: {hex(key)}): {dec_str}")
                except:
                    continue
        except Exception as e:
            logger.debug(f"XOR viga: {e}")
            continue
    return results

def decode_ps_payload(text):
    b64_pattern = r'[A-Za-z0-9+/]{40,}'
    matches = re.findall(b64_pattern, text)
    decoded_list = []
    for m in matches:
        try:
            raw_data = base64.b64decode(m)
            decoded = raw_data.decode('utf-16-le', errors='ignore')
            if any(k in decoded.lower() for k in ['http', 'iex', 'invoke']): decoded_list.append(decoded.strip())
        except Exception as e:
            logger.debug(f"B64 dekodeerimise viga: {e}")
            continue
    return decoded_list

def run_deep_forensics():
    print(LOGO)
    out_dir = utils.get_output_dir()
    input_files = [os.path.join(out_dir, '03_tulemus_turvafiltreering.csv'), os.path.join(out_dir, '04_tulemus_kahtlased_marksonad.csv')]
    out_report = os.path.join(out_dir, '05_tulemus_suvaanaluusi_raport.txt')
    findings = 0
    with open(out_report, mode='w', encoding='utf-8') as f_out:
        f_out.write("VALVUR - SÜVAANALÜÜSI RAPORT\n" + "="*70 + "\n\n")
        for in_file in input_files:
            if not os.path.exists(in_file): continue
            try:
                with open(in_file, mode='r', encoding='utf-8') as f_in:
                    reader = csv.DictReader(f_in)
                    for row in reader:
                        msg = row.get('Message', '')
                        decoded = decode_ps_payload(msg)
                        xor_f = find_xor_payloads(msg)
                        if decoded or xor_f:
                            findings += 1
                            f_out.write(f"LEID #{findings} | Aeg: {row.get('TimeCreated')}\n")
                            for d in decoded: f_out.write(f"  [>>>] B64: {d}\n")
                            for x in xor_f: f_out.write(f"  [>>>] XOR: {x}\n")
            except Exception as e:
                logger.error(f"Faili {in_file} lugemisel viga: {e}")
    print(f"VALMIS! Raport: {out_report}")

if __name__ == "__main__":
    run_deep_forensics()
