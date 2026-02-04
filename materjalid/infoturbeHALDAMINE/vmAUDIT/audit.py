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
#   |   FAILI NIMI:  audit.py                                             |   #
#   |   LOODUD:      2025-11-17                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   GITHUB:      github.com/ocrHeiki                                  |   #
#   |   KIRJELDUS:   Süsteemi esmane triaaž: protsessid, võrguühendused   |   #
#   |                ja kasutajate audit.                                 |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

import os
import subprocess
from datetime import datetime

def run_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('cp850', errors='replace').strip()
    except Exception as e:
        return f"Viga käsu käivitamisel: {str(e)}"

def collect_audit():
    print(f"[*] VALVUR: Käivitan süsteemi auditi: {datetime.now()}")
    output_dir = "audit_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audit_data = {
        "1_Systeemi_info": "systeminfo",
        "2_Jooksvad_protsessid": "tasklist /v",
        "3_Vorguyhendused": "netstat -ano",
        "4_DNS_vahemalu": "ipconfig /displaydns",
        "5_Teenused": "sc query type= service state= all",
        "6_Startup_programmid": "wmic startup get caption,command",
        "7_Kasutajakontod": "net user",
        "8_Admin_grupp": "net localgroup administrators"
    }

    for filename, command in audit_data.items():
        print(f"[+] Kogumisel: {filename}...")
        result = run_command(command)
        with open(f"{output_dir}/{filename}.txt", "w", encoding="utf-8") as f:
            f.write(result)

    ps_commands = {
        "9_Kaik_ajastatud_ulesanded": "Get-ScheduledTask | Where-Object {$_.TaskPath -notlike '\\Microsoft*'} | Select-Object TaskName, State, Actions",
        "10_PowerShell_ajalugu": "if (Test-Path (Get-PSReadlineOption).HistorySavePath) { Get-Content (Get-PSReadlineOption).HistorySavePath } else { 'Ajalugu puudub' }"
    }

    for filename, command in ps_commands.items():
        print(f"[+] Kogumisel (PowerShell): {filename}...")
        result = run_command(f"powershell -Command \"{command}\"")
        with open(f"{output_dir}/{filename}.txt", "w", encoding="utf-8") as f:
            f.write(result)

    print(f"\n[!] Audit lõpetatud. Failid: {output_dir}")

if __name__ == "__main__":
    collect_audit()
