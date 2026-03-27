#!/usr/bin/env python3
"""
05_genereeri_raport.py - Koostab analüüsi tulemustest Wordi (.docx) raporti.
Teisendab UTC ajatemplid Eesti ajavööndisse (Europe/Tallinn).
Kasutamine: python3 SKRIPTID/05_genereeri_raport.py
"""

import os
import csv
from datetime import datetime
from zoneinfo import ZoneInfo
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# ASCII Logo metainfo (VALVUR standard)
LOGO = r"""
###############################################################################
#                                                                             #
#   PROJEKT:     VALVUR - Raporti Genereerimine                               #
#   FAILI NIMI:  05_genereeriRAPORT.py                                       #
#   LOODUD:      27.03.2026                                                   #
#   AUTOR:       Heiki Rebane                                                 #
#   KIRJELDUS:   Koostab kronoloogilise raporti Eesti ajavööndis.             #
#                                                                             #
###############################################################################
"""

def convert_to_ee_time(utc_string):
    """
    Teisendab Windowsi UTC (Z) aja Eesti ajavööndisse.
    Näide: 2026-03-27T14:00:00.123Z -> 27.03.2026 16:00:00
    """
    if not utc_string or utc_string == "N/A":
        return "N/A"
    try:
        # Puhastame stringi ja muudame selle datetime objektiks
        # Windowsi ISO formaat võib sisaldada 'Z' lõpus
        clean_time = utc_string.replace('Z', '+00:00')
        dt_utc = datetime.fromisoformat(clean_time)
        
        # Teisendame Eesti aega (arvestab automaatselt suve/talveaega)
        dt_ee = dt_utc.astimezone(ZoneInfo("Europe/Tallinn"))
        
        return dt_ee.strftime('%d.%m.%Y %H:%M:%S')
    except Exception:
        return utc_string

def create_word_report():
    print(LOGO)
    doc = Document()

    # --- 1. TIITELLEHT JA PEALKIRI ---
    title = doc.add_heading('VALVUR - Intsidendi Analüüsi Raport', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    meta = doc.add_paragraph()
    meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = meta.add_run(f"Raporti koostamise aeg (Eesti): {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    run.italic = True

    # --- 2. KRONOLOOGILINE TIMELINE (Skriptist 02) ---
    doc.add_heading('1. Sündmuste kronoloogia (Timeline)', level=1)
    doc.add_paragraph("Kriitiliste sündmuste koondtabel Eesti ajavööndis (EET/EEST).")
    
    csv_path = 'TULEMUSED/02_tulemus_turvafiltreering.csv'
    if os.path.exists(csv_path):
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            table = doc.add_table(rows=1, cols=4)
            table.style = 'Table Grid'
            
            # Päis
            hdr_cells = table.rows[0].cells
            for i, text in enumerate(['Aeg (Eesti)', 'Event ID', 'Masin', 'Sündmuse sisu']):
                hdr_cells[i].text = text
                hdr_cells[i].paragraphs[0].runs[0].font.bold = True

            for row in reader:
                row_cells = table.add_row().cells
                row_cells[0].text = convert_to_ee_time(row.get('TimeCreated', ''))
                row_cells[1].text = row.get('Id', 'N/A')
                row_cells[2].text = row.get('MachineName', 'N/A')
                # Võtame sõnumist esimesed 100 märki, et tabel ei läheks liiga laiaks
                msg = row.get('Message', 'N/A')
                row_cells[3].text = (msg[:100] + '...') if len(msg) > 100 else msg
    else:
        doc.add_paragraph("HOIATUS: Timeline faili ei leitud. Käivita skript 02.")

    # --- 3. TEOSTATUD OTSINGUD (Skriptist 03) ---
    doc.add_heading('2. Tuvastatud ründeindikaatorid (IOC)', level=1)
    keywords_path = 'TULEMUSED/03_tulemus_kahtlased_marksonad.csv'
    
    if os.path.exists(keywords_path):
        with open(keywords_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(f"MÄRKSÕNA: {row.get('MatchedKeyword')}").bold = True
                p.add_run(f"\nAeg: {convert_to_ee_time(row.get('TimeCreated'))}")
                p.add_run(f"\nAllikas: {row.get('SourceFile')}")
    else:
        doc.add_paragraph("Kahtlaseid märksõnu logidest ei leitud.")

    # --- 4. DEKODEERITUD POWERSHELL (Skriptist 04) ---
    doc.add_heading('3. Dekodeeritud PowerShell käsud', level=1)
    deep_path = 'TULEMUSED/04_tulemus_suvaanaluusi_raport.txt'
    
    if os.path.exists(deep_path):
        with open(deep_path, 'r', encoding='utf-8') as f:
            content = f.read()
            para = doc.add_paragraph()
            run = para.add_run(content)
            run.font.name = 'Courier New'
            run.font.size = Pt(8)
    else:
        doc.add_paragraph("Süvaanalüüsi raportit ei leitud.")

    # --- SALVESTAMINE ---
    output_docx = 'TULEMUSED/VALVUR_LOPLIK_RAPORT.docx'
    try:
        doc.save(output_docx)
        print(f"\n[+] EDU: Raport salvestatud: {output_docx}")
    except Exception as e:
        print(f"\n[!] VIGA salvestamisel: {e}")

if __name__ == "__main__":
    create_word_report()
