#!/usr/bin/env python3
"""
08_tehniline_raport_pdf.py - Genereerib tehnilise PDF raporti juhtkonnale.
Selgitab VALVURi võimekust (XOR, Fuzzy matching jne).
"""

import os

# ASCII Logo (VALVUR standard)
r

def generate_technical_info():
    print(LOGO)
    content = """
    VALVUR - TEHNILINE VÕIMEKUS JA AUDITI LOGIIKA
    ============================================
    
    1. XOR JA DEKOODER
    VALVUR suudab automaatselt tuvastada ja dekodeerida PowerShell-i käske, 
    mis on peidetud Base64 või lihtsa XOR algoritmi taha. See võimaldab 
    näha ründaja tegelikke kavatsusi.

    2. FUZZY MATCHING (MÄÄRAMATU VASTAVUS)
    Logide analüüsil kasutatakse 'Fuzzy matching' loogikat, mis tähendab, 
    et me ei otsi ainult täpseid märksõnu (nt 'mimikatz'), vaid ka 
    variatsioone ja sarnaseid kirjapilte, mida ründajad kasutavad 
    tuvastuse vältimiseks.

    3. API INTEGRATSIOON
    VALVUR on ette valmistatud integratsiooniks väliste andmebaasidega 
    (nt VirusTotal või AbuseIPDB), et kontrollida leitud IP-sid ja 
    faili räsi-sid (hashes) reaalajas.

    4. E-ITS JA VASTAVUSKONTROLL
    Süsteemne audit võrdleb masina seadeid Eesti riikliku 
    infoturbe standardiga (E-ITS), pakkudes koheseid parandusmeetmeid.
    """
    
    # Proovime luua PDF-i kui fpdf on olemas
    try:
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="VALVUR - Tehniline Spetsifikatsioon", ln=1, align='C')
        pdf.set_font("Arial", size=11)
        pdf.ln(10)
        for line in content.split('\n'):
            pdf.multi_cell(0, 10, txt=line.strip(), align='L')
        
        out_file = "TULEMUSED/VALVUR_TEHNILINE_INFO.pdf"
        pdf.output(out_file)
        print(f"[+] Tehniline PDF raport loodud: {out_file}")
    except ImportError:
        # Kui FPDF puudub, teeme ilusa tekstifaili
        out_file = "TULEMUSED/VALVUR_TEHNILINE_INFO.txt"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[!] FPDF teeki ei leitud. Loodi tekstipõhine raport: {out_file}")
        print("    Vihje: 'pip install fpdf' PDF-i genereerimiseks.")

if __name__ == "__main__":
    generate_technical_info()
