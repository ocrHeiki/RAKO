# analyser.py

import subprocess
import sys
import os
import importlib

# -------------------------
# AUTOMAATNE PAKETI KONTROLL
# -------------------------
def install_and_import(package):
    try:
        importlib.import_module(package)
    except ImportError:
        print(f"📦 Paigaldan {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user"])

REQUIRED = ["pandas", "numpy", "matplotlib", "seaborn", "python-docx", "scikit-learn", "requests"]

for pkg in REQUIRED:
    pkg_name = pkg.replace("-", "_").split("==")[0]
    install_and_import(pkg_name)

# -------------------------
# NÜÜD IMPORDI KÕIK MOODULID
# -------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from docx import Document
from docx.shared import Inches
from datetime import datetime, timedelta
import requests
from sklearn.cluster import KMeans

# -------------------------
# SEADED
# -------------------------
ABUSEIPDB_API_KEY = 'YOUR_ABUSEIP_KEY_HERE'  # Asenda oma võtmega
RAW_DIR = "RAW"
OUTPUT_DIR = "TULEMUSED"
CHARTS_DIR = os.path.join(OUTPUT_DIR, "charts")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR, exist_ok=True)

# -------------------------
# WHITELIST & BLACKLIST
# -------------------------
whitelist = ["10.0.0.1 – Gateway", "10.0.0.10 – Server OK", "192.168.1.1 – Internal Router", "Allowed_Internal_Traffic"]
blacklist = ["185.234.219.0/24 – Botnet / abuse", "Known_Malicious_IP", "Suspicious_Rule", "Tor_Exit_Node"]

# -------------------------
# FALSE POSITIVE MAPPING
# -------------------------
fp_mapping = {
    "ICMP Ping": ["Legitiimne teenusedetektsioon (health-check)", "Tavapärane sisemine võrguliiklus"],
    "Port Scan": ["Automatiseeritud süsteemi taustaprotsess", "Korrelatsioonireegli vale tundlikkus"],
    "HTTP Outbound": ["VPN kasutamine", "Tarkvara uuendus"],
    "DNS Lookup": ["Tavapärane sisemine võrguliiklus"],
}
default_fp_reasons = [
    "Kasutaja käivitatud tegevus",
    "Normaalne töökoormus / backup / scan",
    "Tarkvara uuendus / package manager",
]

# -------------------------
# MITRE ATT&CK MAPPING
# -------------------------
attck_mapping = {
    "SMB Login Attempt": {"tactic": "Lateral Movement", "technique": "T1021 - Remote Services"},
    "Outbound C2 Traffic": {"tactic": "Command and Control", "technique": "T1071 - Application Layer Protocol"},
    "Malware Download": {"tactic": "Execution", "technique": "T1204 - Malicious File"},
    "Suspicious PowerShell": {"tactic": "Execution", "technique": "T1059 - Command and Scripting Interpreter"},
    "Port Scan": {"tactic": "Reconnaissance", "technique": "T1046 - Network Service Scanning"},
    "ICMP Ping": {"tactic": "Discovery", "technique": "T1018 - Remote System Discovery"},
    "DNS Tunneling": {"tactic": "Exfiltration", "technique": "T1048 - Exfiltration Over Alternative Protocol"},
    "Brute Force Login": {"tactic": "Credential Access", "technique": "T1110 - Brute Force"}
}

# -------------------------
# LOGI LOETLEMINE
# -------------------------
log_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.csv')]
if not log_files:
    print("⚠️ Kaustas RAW ei leitud CSV-logifaile.")
    sys.exit()

# Loeme esimese logifaili (võid täiendada, et töötle kõik)
log_path = os.path.join(RAW_DIR, log_files[0])
df = pd.read_csv(log_path)
df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
df["date"] = df["timestamp"].dt.date
df["hour"] = df["timestamp"].dt.hour

# -------------------------
# BEHAVIORAL BASELINE
# -------------------------
def detect_behavioral_anomalies(df):
    hourly = df.groupby(['source', 'hour']).size().reset_index(name='counts')
    pivot = hourly.pivot(index='source', columns='hour', values='counts').fillna(0)
    kmeans = KMeans(n_clusters=5, random_state=42)
    pivot['cluster'] = kmeans.fit_predict(pivot)
    anomaly_cluster = pivot['cluster'].value_counts().idxmin()
    return pivot[pivot['cluster'] == anomaly_cluster].index.tolist()

# -------------------------
# THREAT INTELLIGENCE
# -------------------------
def check_abuseipdb(ip):
    if not ip or ip in ['Unknown', '-', np.nan]:
        return 'unknown'
    url = 'https://api.abuseipdb.com/api/v2/check'
    headers = {'Accept': 'application/json', 'Key': ABUSEIPDB_API_KEY}
    params = {'ipAddress': ip, 'maxAgeInDays': 90}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        data = response.json()
        score = data['data'].get('abuseConfidenceScore', 0)
        if score > 75:
            return 'malicious'
        elif score > 40:
            return 'suspicious'
        else:
            return 'clean'
    except:
        return 'unknown'

# -------------------------
# FALSE POSITIVE + MITRE
# -------------------------
def generate_fp_reason(row):
    return np.random.choice(fp_mapping.get(row['rule'], default_fp_reasons))
df['false_positive_reason'] = df.apply(generate_fp_reason, axis=1)

def map_attck(row):
    mapping = attck_mapping.get(row['rule'], {"tactic": "Unknown", "technique": "N/A"})
    return pd.Series([mapping['tactic'], mapping['technique']])
df[['attck_tactic', 'attck_technique']] = df.apply(map_attck, axis=1)

# -------------------------
# DAILY ANOMALY DETECTION
# -------------------------
daily = df.groupby("date").size()
mean = daily.mean()
std = daily.std()
anomalies = daily[daily > mean + 2 * std]

# -------------------------
# SOC PRIORITY ENGINE
# -------------------------
def severity_score(sev):
    sev = str(sev).lower()
    if sev == "critical":
        return 70
    if sev == "high":
        return 50
    if sev == "medium":
        return 30
    return 10

def is_blacklisted(value):
    for b in blacklist:
        if str(b).split("–")[0].strip() in str(value):
            return True
    return False

def is_whitelisted(value):
    for w in whitelist:
        if str(w).split("–")[0].strip() in str(value):
            return True
    return False

rule_freq = df["rule"].value_counts().to_dict()
max_freq = max(rule_freq.values()) if rule_freq else 1

def calculate_priority(row):
    score = 0
    ip = str(row['source'])
    score += severity_score(row["severity"])
    if is_blacklisted(ip): score += 35
    if is_whitelisted(ip): score -= 25
    rarity = 1 - (rule_freq.get(row["rule"], 0) / max_freq)
    score += int(rarity * 20)
    if row["date"] in anomalies.index: score += 20
    if ip in detect_behavioral_anomalies(df): score += 25
    if check_abuseipdb(ip) in ['malicious', 'suspicious']: score += 30
    score = max(0, min(100, score))
    if score >= 85:
        priority = "CRITICAL"
    elif score >= 60:
        priority = "HIGH"
    elif score >= 35:
        priority = "MEDIUM"
    else:
        priority = "LOW"
    return pd.Series([score, priority])

df[["soc_score", "soc_priority"]] = df.apply(calculate_priority, axis=1)

# -------------------------
# GRAAFIKUD
# -------------------------
def save_chart(series, title, filename):
    plt.figure(figsize=(8,5))
    series.plot(kind="bar")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

severity_counts = df["severity"].value_counts()
rule_top10 = df["rule"].value_counts().head(10)
top_source = df["source"].value_counts().head(10)
top_risky = df.nlargest(10, 'soc_score')

save_chart(severity_counts, "Severity Distribution", os.path.join(CHARTS_DIR, "severity.png"))
save_chart(rule_top10, "Top 10 Rules", os.path.join(CHARTS_DIR, "rules.png"))
save_chart(top_source, "Top 10 Source IPs", os.path.join(CHARTS_DIR, "top_source.png"))
save_chart(top_risky.set_index('rule')['soc_score'], "Top 10 SOC Scores", os.path.join(CHARTS_DIR, "top_soc.png"))

heatmap_data = df.pivot_table(index="source", columns="hour", values="rule", aggfunc="count").fillna(0)
plt.figure(figsize=(12,7))
sns.heatmap(heatmap_data, cmap="viridis")
plt.title("Heatmap: Source vs Hour")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "heatmap.png"))
plt.close()

timeline = df.groupby(pd.Grouper(key="timestamp", freq="1H")).size()
plt.figure(figsize=(12,4))
timeline.plot()
plt.title("Timeline (Events per Hour)")
plt.tight_layout()
plt.savefig(os.path.join(CHARTS_DIR, "timeline.png"))
plt.close()

# -------------------------
# DOCX REPORT
# -------------------------
doc = Document()
doc.add_heading("Enhanced Security Log Analysis Report", level=1)
doc.add_paragraph(f"Total events: {len(df)}")
doc.add_paragraph(f"Unique sources: {df['source'].nunique()}")
doc.add_paragraph(f"Unique destinations: {df['destination'].nunique()}")

doc.add_heading("Top 10 SOC Score Rules", level=2)
doc.add_picture(os.path.join(CHARTS_DIR, "top_soc.png"), width=Inches(5.5))

doc.add_heading("Detected Behavioral Anomalies", level=2)
anomalous_sources = detect_behavioral_anomalies(df)
for ip in anomalous_sources[:10]:
    doc.add_paragraph(f"- {ip}")

doc.add_heading("Threat Intelligence Findings", level=2)
malicious_ips = df[df['source'].apply(check_abuseipdb) == 'malicious']['source'].unique()
for ip in malicious_ips[:10]:
    doc.add_paragraph(f"- {ip} (malicious)")

doc.add_heading("MITRE ATT&CK Mapping", level=2)
for tactic in df['attck_tactic'].unique():
    if tactic == 'Unknown': continue
    doc.add_heading(f"Tactic: {tactic}", level=3)
    subset = df[df['attck_tactic'] == tactic]
    techniques = subset['attck_technique'].value_counts()
    for tech, count in techniques.items():
        doc.add_paragraph(f"{tech}: {count} events")

doc.add_heading("Top MITRE Techniques Detected", level=3)
top_techniques = df['attck_technique'].value_counts().head(10)
for tech, count in top_techniques.items():
    doc.add_paragraph(f"{tech}: {count}")

doc_file = os.path.join(OUTPUT_DIR, "enhanced_report.docx")
doc.save(doc_file)

# -------------------------
# CSV EKSPORT
# -------------------------
csv_file = os.path.join(OUTPUT_DIR, "mitre_mapping.csv")
df[['attck_tactic', 'attck_technique', 'source', 'destination', 'soc_priority', 'soc_score']].to_csv(csv_file, index=False)

print(f"✅ Töö lõpetatud!")
print(f"📄 Aruanne: {doc_file}")
print(f"📊 Kaust: {CHARTS_DIR}")
print(f"💾 CSV: {csv_file}")
