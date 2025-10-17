# 🔎 SOC L1 – OSINT ja korduvate LOW-sündmuste analüüs (ITO terminal)

## 📘 Ülevaade

See skript on **järg esialgsele 24h ja nädalasele alertide analüüsile**, kus koguti ja tuvastati **Palo Alto Threat logidest** kõige sagedamini esinenud ohud ja IP-aadressid.  
Antud etapp keskendub **järgmiseks tasemeks (SOC L1+)** – ehk:
- tuvastama **madala raskusastmega (LOW)** sündmuste korduseid,
- otsima **valepositiivseid mustreid** sisevõrgus,
- ja automaatselt **rikastama** väliste (avalike) IP-de infot OSINT allikatest (nt AbuseIPDB, VirusTotal, OTX).

Eesmärk on vähendada käsitsi tehtavat kontrolli ja anda **ITO terminalis** töötavale analüütikule **täpne ja automatiseeritud ülevaade** sellest, millised IP-d ja ohud vajavad täiendavat tähelepanu.

---

## ⚙️ Töövoog

1. **Eelnev etapp:**  
   - Oled juba käivitanud 24h ja nädalase logianalüüsi skriptid, mis lõid failid nagu:
     - `24h_threat_summary.docx`
     - `week_threat_summary.docx`
     - `24h_ip.txt` (või sarnane IP-nimekiri)
   - Need failid asuvad tavaliselt kaustas `Documents/SOC/raw/` või `Documents/SOC/tulemused/`.

2. **Käesolev etapp (OSINT ja FP analüüs):**  
   - Käesolev skript (`soc_top10_osint.py`) loeb kõik need logid sisse,  
   - leiab **TOP 10 allika IP-d** ja **TOP 10 Threat/Content Name’id**,  
   - otsib **LOW-severity korduseid** (võimalikud valepositiivid),  
   - analüüsib **sisevõrgu IP-d (CIDR /24, /16 jne)**,  
   - teeb avalike IP-de kohta automaatselt **OSINT enrichment’i**.

---

## 💻 Käivitamine (ITO terminalis)

```bash
python3 soc_top10_osint.py --raw-dir RAW --outdir results --md-report
```

**Selgitus:**
- `--raw-dir RAW` → kaust, kus on toorlogid (CSV, JSON, TXT)
- `--outdir results` → väljundkaust, kuhu raportid salvestatakse
- `--md-report` → loob Markdown-aruande (loetav terminalis või VS Code'is)

---

## 🌍 OSINT rikastamine (valikuline)

Kui sul on õigused ja API võtmed (nt AbuseIPDB või VirusTotal), saad lisada need keskkonnamuutujatena terminalis:

```bash
export ABUSEIPDB_KEY="SINU_ABUSEIPDB_KEY"
export VT_API_KEY="SINU_VIRUSTOTAL_KEY"
export OTX_API_KEY="SINU_OTX_KEY"
export IPINFO_TOKEN="SINU_IPINFO_KEY"
```

Kui võtmeid pole, töötab skript **offline-režiimis** ning teeb ainult sisevõrgu ja korduvate sündmuste analüüsi.

---

## 🧩 Väljundid (`results/` kaustas)

| Fail | Kirjeldus |
|------|------------|
| **top10_summary.csv** | TOP 10 Source IP & TOP 10 Threat nimekiri |
| **ips_for_enrichment.txt** | Avalike IP-de nimekiri, mille kohta tehakse OSINT |
| **enrich/** | JSON-failid iga IP kohta (toorandmed OSINTist) |
| **enrich_summary.csv** | OSINT koond (riik, ISP, hinnang, punktid) |
| **internal_analysis.csv** | Sisevõrgu IP-de tegevusanalüüs (LOW mustrid) |
| **Top10_Enrichment_Report_<Seade>_<Kuupäev>.md** | Markdown-raport (kogu kokkuvõte) |

---

## 📘 Mida edasi teha SOC töövoos

| Etapp | Kirjeldus | Tulemus |
|-------|------------|---------|
| **1. Logide kogumine (24h/week)** | Kogutakse ja salvestatakse 24h ning nädalased threat logid | `24h_summary.docx`, `week_summary.docx` |
| **2. OSINT & FP analüüs (see skript)** | Analüüsitakse madala raskusastme sündmusi ja rikastatakse IP infot | `Top10_Enrichment_Report_*.md` |
| **3. Graylog või SIEM sisestus** | Tulemustest luuakse märkus või whitelist/blacklist reegel | kiire eskaleerimine või FP märge |
| **4. SOC L2/L3 analüüs** | Täpsem ohuanalüüs (failid, hashid, võrguvoolud) | raport või intsident |

---

> 📎 *Projekt kuulub SOC L1–L3 õppeprojekti “24h ja nädalane logianalüüs – OSINT jätk” alla.*  
> Autor: **ocrHeiki**  
> GitHub: [github.com/ocrHeiki](https://github.com/ocrHeiki)
