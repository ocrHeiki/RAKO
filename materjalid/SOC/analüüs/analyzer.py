# ==============================================================
#  SOC Threat Analyser v5.2 (Koos Threat Intelligence Mooduliga)
#  Autor: Heiki Rebane (õpiprojekt)
#  Kuupäev: 17.11.2025
#  Kirjeldus:
#   - Loeb CSV-failid kaustast raw/ ja filtreerib ajavahemiku järgi.
#   - Analüüsib threat-nimesid, IP aktiivsust ja sündmuste jagunemist.
#   - Lisab WEEKLY TREND ANALYSIS mooduli.
#   - UUS: Genereerib eraldi faili unikaalsete threatide nimekirjast koos Threat Vault infoga.
#   - Tuvastab Volume-Based ja CVE Diversity IP-d.
#   - Lisab MITRE ATT&CK kaardistuse ja Threat Vault info (koos cache'iga).
#   - Koostab DOCX, TXT ja XLSX raportid graafikutega.
#   - Kasutab MOCK GeoIP lahendust.
# ==============================================================

import subprocess
import sys
import os
import importlib
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import re
from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import argparse
import requests
import json
import matplotlib.dates as mdates 
import io 

# ————————————————————————————————
# CLI Argumentide seadistus.
# ————————————————————————————————

def parse_args():
    parser = argparse.ArgumentParser(description="SOC Threat Analyser - Palo Alto logianalüüs")
    parser.add_argument("--timeframe", choices=["24h", "7d", "30d"], default="7d",
                        help="Analüüsitav ajavahemik (vaikimisi: '7d')")
    parser.add_argument("--output", choices=["brief", "detailed"], default="detailed",
                        help="Aruande detailne tase (vaikimisi: 'detailed')")
    parser.add_argument("--strict-local", action="store_true",
                        help="Kohalike (France/Réunion) IP-de kohta rakendatakse karmimaid reegleid")
    return parser.parse_args()


# ————————————————————————————————
# Algne projekti struktuur ja kaustade seaded
# ————————————————————————————————

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "raw" # Logifailid
REPORTS_DIR = BASE_DIR / "reports" # Graafikud
RESULTS_DIR = BASE_DIR / "tulemused" # Lõppraportid
THREAT_VAULT_CACHE = BASE_DIR / "threat_vault_cache" # Threat Vault andmete vahemälu
TRENDS_DIR = BASE_DIR / "trendid" # Kaust trendiraportite graafikute jaoks

for d in [RAW_DIR, REPORTS_DIR, RESULTS_DIR, THREAT_VAULT_CACHE, TRENDS_DIR]:
    d.mkdir(parents=True, exist_ok=True) 

# Seadistused ja püsivad andmed (lühendatud, kuna sisu jäi Sinu koodi)
# ... (COLORS_SEV, fp_guidance, attck_mapping ja MOCK GeoIP kood) ...

# MOCK GeoIP – Kasutatakse ainult juhul, kui päris GeoIP2 faile pole lubatud alla laadida
predefined_geo = {
    "192.168.1.20": {"country": "Prantsusmaa", "city": "Pariis"},
    "192.168.2.100": {"country": "Réunion", "city": "Saint-Denis"},
    "8.8.8.8": {"country": "Ameerika Ühendriigid", "city": "Kalifornia"},
    "203.12.160.45": {"country": "Hiina", "city": "Shenzhen"},
    "176.10.10.1": {"country": "Venemaa", "city": "Moskva"}
}

def get_country(ip):
    return predefined_geo.get(ip, {}).get("country", "Teadmata")

# ————————————————————————————————
# Threat Vault integratsioon (sisseehitatud API päring ja cache)
# ————————————————————————————————

def get_threat_details(threat_name):
    # Asenda keelatud märgid, et luua turvaline failinimi cache jaoks
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', threat_name)
    cache_file = THREAT_VAULT_CACHE / f"{safe_name}.json"
    
    # 1. Kontrolli cache'i olemasolu
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
             print(f"❗Viga cache'i lugemisel failist: {cache_file}")

    # 2. Tee reaalajas päring Palo Alto Threat Vault API-le
    try:
        url = "https://threatvault.paloaltonetworks.com/restapi/threats"
        headers = {"User-Agent": "SOC-Threat-Analyser"}
        params = {"search": threat_name}
        resp = requests.get(url, headers=headers, params=params, timeout=10) # 10 sekundi timeout
        
        if resp.status_code == 200:
            data = resp.json()
            threat = data.get("threats", [])[0] if data.get("threats") else {}
            
            # 3. Salvesta vastus cache'i
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(threat, f, indent=2)
            return threat
    
    except requests.exceptions.RequestException as e:
        # print(f"❗Võrgu/API viga Threat Vault otsingus '{threat_name}': {e}")
        pass
    except Exception as e:
        # print(f"❗Muu viga Threat Vault otsingus '{threat_name}': {e}")
        pass
    
    return {} # Tagastab tühja, kui päring ebaõnnestus

# ————————————————————————————————
# Abifunktsioonid
# ————————————————————————————————

def iso_from_filename(name: str):
    # Ekstraktib kuupäeva failinimest
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    if m:
        return datetime.strptime(f"{m.group(3)}-{m.group(2)}-{m.group(1)}", "%Y-%m-%d").date()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", name)
    return m.group(0) if m else datetime.now().date()

def first_existing(df, names):
    # Leiab logifailist esimese sobiva veeru nime
    for n in names:
        if n in df.columns:
            return n
    return None

def norm_lower(col):
    # Normaliseerib andmed: kõik väiketähtedeks, tühikud ja reavahetused eemaldatud
    return col.astype(str).str.lower().str.strip()

def bar(series, title, outpath, colors=None, rot=0, is_date_trend=False):
    # Loob ja salvestab tulpdiagrammi
    if series.empty: return
    
    plt.figure(figsize=(10, 5))
    ax = series.plot(kind="bar", color="#3399FF")
    plt.title(title)
    
    if is_date_trend:
        ax.set_xticklabels(series.index.strftime('%Y-%m-%d'))
        plt.xticks(rotation=45, ha='right')
    else:
        plt.xticks(rotation=rot)
        
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()

def add_image(doc, img_path, caption, width_in=6.0):
    # Lisab graafiku Microsoft Word (DOCX) raportisse
    if not img_path.exists(): return
    p = doc.add_paragraph()
    run = p.add_run()
    run.add_picture(str(img_path), width=Inches(width_in))
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph(caption)
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER

# ————————————————————————————————
# THREAT INTELLIGENCE GENEREERIMISE MOODUL (UUS)
# ————————————————————————————————

def generate_threat_list(df_all): 
    """
    Ekstraheerib kõik unikaalsed threatide nimed, teeb Threat Vault päringu 
    (kasutades cache'i) ja salvestab detailse nimekirja TXT-faili.
    """
    print("📜 Käivitan unikaalsete threatide nimekirja koostamise koos Vault infoga...")
    
    threat_col = first_existing(df_all, ["Threat/Content Name", "threat_name"])
    
    if not threat_col:
        print("❗ Viga: Threat Name veergu ei leitud logifailidest!")
        return 
        
    unique_threats = df_all[threat_col].dropna().unique()
    output_path = RESULTS_DIR / "palo_alto_threat_list.txt"
    total_found = 0
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Palo Alto Networks: Unikaalsete Threatide nimekiri koos Vault detailidega\n")
        f.write(f"# Koostatud: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("=" * 80 + "\n\n")
        
        for i, threat_name in enumerate(unique_threats):
            # Kindlustab string-töötluse
            threat_name = str(threat_name).strip() 
            if not threat_name: continue
            
            # Hankige detailid Threat Vault funktsiooniga (mis kasutab cache'i)
            # Eemaldab sulud, et saata Vaultile puhas nimi (nt 'MS RPC (12345)' -> 'MS RPC')
            match = re.match(r"(.*?)\s+\(\d+\)", threat_name)
            clean_name = match.group(1).strip() if match else threat_name
            
            vault_info = get_threat_details(clean_name)
            
            f.write(f"Threat Nimi Logis: {threat_name}\n")
            
            if vault_info.get('id'):
                f.write(f"ID:          {vault_info.get('id', 'N/A')}\n")
                f.write(f"Severity:    {vault_info.get('severity', 'N/A')}\n")
                f.write(f"Tüüp:        {vault_info.get('type', 'N/A')}\n")
                f.write(f"Kategooria:  {vault_info.get('category', 'N/A')}\n")
                f.write(f"Kirjeldus:   {vault_info.get('description', 'Kirjeldus puudub')[:150]}...\n") 
                total_found += 1
            else:
                f.write("Vault Info:  OTSUST EI LEITUD CACHE'IST EGA VAULT API-ST\n")
                
            f.write("-" * 50 + "\n")
            
    print(f"✔️ Nimekiri koos Vault infoga salvestatud: {output_path}")

# ————————————————————————————————
# TRENDIANALÜÜSI MOODUL
# ————————————————————————————————

def analyze_trends(df_all):
    # ... (Sisu sama, nagu eelnevalt, toimib df_all peal)
    
    print("📈 Käivitan nädalapõhise trendianalüüsi...")

    df_trends = df_all.copy()
    df_trends["log_date"] = pd.to_datetime(df_trends["log_date"], errors='coerce') 
    
    df_trends.dropna(subset=["log_date"], inplace=True)

    df_trends['week_start'] = df_trends['log_date'].apply(
        lambda x: x - timedelta(days=x.weekday()) 
    ).dt.normalize()

    weekly_volume = df_trends.groupby('week_start').size() 
    
    out_trend_vol = TRENDS_DIR / "trend_weekly_volume.png"
    bar(weekly_volume, "Nädalapõhine Logide Maht (Trend)", out_trend_vol, is_date_trend=True)

    top5_threat_names = df_trends['tname_norm'].value_counts().head(5).index.tolist()
    
    weekly_threats = df_trends.groupby(['week_start', 'tname_norm']).size().unstack(fill_value=0)
    
    top5_trend = weekly_threats[weekly_threats.columns.intersection(top5_threat_names)]

    out_trend_top5 = TRENDS_DIR / "trend_top5_threats.png"
    
    plt.figure(figsize=(12, 6))
    top5_trend.plot(kind='line', marker='o', ax=plt.gca()) 
    plt.title("TOP 5 Threat'i Aktiivsus Aja Jooksul")
    plt.xlabel("Nädala Algus")
    plt.ylabel("Kirjete Arv")
    plt.legend(title='Threat', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(out_trend_top5)
    plt.close()
    
    trend_result = {
        "weekly_volume": weekly_volume.to_string(), 
        "top5_trend": top5_trend.to_string(),
        "plot_volume": out_trend_vol,
        "plot_top5": out_trend_top5
    }
    
    print("✔️ Trendianalüüs lõpetatud. Tulemused salvestatud /trendid kausta.")
    return trend_result


# ————————————————————————————————
# PROJEKTI PÕHIPLOKK – ANALÜÜSI JA RAPORTITE LOOMINE
# ————————————————————————————————

def main():
    args = parse_args()
    timeframe_days = {"24h": 1, "7d": 7, "30d": 30}[args.timeframe]

    print(f"🔍 Käivitan {args.timeframe} analüüsi ({timeframe_days} päeva) | Strict Local: {args.strict_local}")

    csv_files = list(RAW_DIR.glob("*.csv"))
    if not csv_files:
        print("⚠️ Ühtegi CSV-faili ei leitud kaustas: raw/")
        return

    dfs = []
    today = datetime.now().date()

    for f in csv_files:
        df = pd.read_csv(f, low_memory=False)
        date = iso_from_filename(f.name)
        df["log_date"] = date
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)
    print(f"✔️ Loetud {len(df_all)} kirjet {len(csv_files)} logifailist")
    
    # ----------------------------------------------------
    # TINGIMUSTETA VÄLJAKUTSE: Genereerib kogu ajaloo põhjal threatide nimekirja
    generate_threat_list(df_all) 
    # ----------------------------------------------------

    # Ülejäänud analüüs töötab filtreeritud andmetega
    df_all["log_date"] = pd.to_datetime(df_all["log_date"])
    cutoff_date = today - timedelta(days=timeframe_days)
    df_filtered = df_all[df_all["log_date"].dt.date >= cutoff_date]
    
    # Trend töötab kogu andmemassiivi peal, et näidata ajalugu
    trend_data = analyze_trends(df_all.copy()) # Kasuta koopiat, et mitte rikkuda df_filtered
    
    # ... (Jätkub veergude tuvastuse, normaliseerimise ja aruandlusega)

    # (Lõpuosa)

    # ... (DOCX raporti kood) ...
    doc = Document()
    doc.add_heading(f"SOC {time_range.upper()} ARUANNE – {today_str}", 0)
    
    # ... (DOCX sisu, sh trendide lisamine) ...

    doc.save(out_docx)
    print(f"📄 DOCX aruanne salvestatud: {out_docx}")

    
    # ... (Main lõpetab TXT ja XLSX failide salvestamisega) ...

if __name__ == "__main__":
    main()
