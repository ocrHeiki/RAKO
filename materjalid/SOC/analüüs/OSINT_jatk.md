# 🔎 SOC L1 – OSINT ja korduvate LOW-sündmuste analüüs (ITO terminal)

## 📘 Ülevaade
See skript on **järg esialgsele 24h ja nädalasele alertide analüüsile** (Palo Alto Threat logid). Selles etapis:
- leitakse **TOP 10 allika IP-d** ja **TOP 10 Threat/Content**,
- tuvastatakse **LOW**-raskusastmega kordused (**valepositiivi** kandidaadid),
- tehakse **internal** (sisevõrk) konteksti analüüs,
- ning **OSINT** rikastamine avalikele IP-dele (AbuseIPDB, VirusTotal, OTX, ipinfo).

Kõik väljundid salvestatakse **`~/Documents/SOC/tulemused/`** kausta kuupäeva-põhiste nimedega ja **Wordi aruandena** (DOCX; kui see pole saadaval, siis RTF).

## 💻 Käivitamine (ITO terminal)
```bash
python3 soc_top10_osint.py
```
Vaikimisi:
- sisend: `~/Documents/SOC/raw/`
- väljund: `~/Documents/SOC/tulemused/`

## 🌍 OSINT API võtmed (valikuline)
```bash
export ABUSEIPDB_KEY="PASTE"
export VT_API_KEY="PASTE"
export OTX_API_KEY="PASTE"
export IPINFO_TOKEN="PASTE"
```

## 🧩 Väljundid
- `top10_osint_<YYYY-MM-DD>_summary.csv`
- `top10_osint_<YYYY-MM-DD>_enrich.csv`
- `top10_osint_<YYYY-MM-DD>_internal.csv`
- `enrich/<IP>.json` (iga avaliku IP OSINT detailid)
- `top10_osint_<YYYY-MM-DD>.docx` (või `.rtf` kui DOCX pole võimalik)

## 🧮 Otsustusloogika
**Internal:** LOW >80% ja sündmusi ≥50 → *likely_false_positive*; ALLOW+HIGH/CRITICAL → *suspicious*; kordub samal tunnil → ajastatud töö.  
**OSINT:** AbuseIPDB≥50 → +50; VT positives≥1 → +40; OTX pulses≥1 → +30.  
Skaleering: `≥70 malicious`, `30–69 suspicious`, `<30 unknown`.

> See etapp on mõeldud **pärast esmaseid 24h/nädala kokkuvõtteid**, et **kiirendada FP eristamist** ja **automatiseerida OSINTi**.
