#!/usr/bin/env python3
"""
12_malu_analuus.py - Liides Volatility 3 jaoks mälutõmmiste analüüsimiseks.
"""

import os
import subprocess

r

def run_volatility(image_path, plugin):
    """Käivitab Volatility 3 plugina antud mälutõmmisel."""
    print(f"[*] Käivitan: {plugin}...")
    try:
        # Eeldame, et vol.py või volatility on PATH-is
        cmd = ["vol", "-f", image_path, plugin]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return f"VIGA: Volatility käivitamine ebaõnnestus ({e})"

def analyze_memory(dump_file):
    print(LOGO)
    if not os.path.exists(dump_file):
        print(f"[!] Mälutõmmist failiga {dump_file} ei leitud.")
        print("MÄRKUS: Kopeeri .raw või .mem fail siia, et alustada analüüsi.")
        return

    out_file = "TULEMUSED/12_tulemus_malu_analuus.txt"
    
    # Õppimiseks: siin on nimekiri olulistest Volatility 3 pluginatest
    plugins = {
        "windows.pslist": "Tavaline protsesside nimekiri",
        "windows.psscan": "Leitakse ka peidetud (terminating/hidden) protsessid",
        "windows.netscan": "Võrguühendused mälust",
        "windows.malfind": "Võimaliku süstitud koodi (injected code) tuvastus",
        "windows.registry.hivelist": "Mälus olevad registri tarud"
    }

    with open(out_file, "w", encoding="utf-8") as f:
        f.write("VALVUR - MÄLU ANALÜÜSI RAPORT (Volatility 3)
")
        f.write("="*70 + "

")
        
        for plugin, desc in plugins.items():
            print(f"[+] Analüüsin: {desc} ({plugin})")
            output = run_volatility(dump_file, plugin)
            f.write(f"--- {plugin} ({desc}) ---
")
            f.write(output)
            f.write("
" + "-"*70 + "

")

    print(f"
[OK] Mälu analüüs lõpetatud. Raport: {out_file}")

if __name__ == "__main__":
    # Siia saad panna oma mälutõmmise tee (nt 'memdump.raw')
    analyze_memory("LOGID/memdump.raw")
