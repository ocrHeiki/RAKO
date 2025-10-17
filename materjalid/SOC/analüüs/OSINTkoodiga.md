# SOC L1 – Palo Alto Threat Log TOP10 + OSINT (üks fail, ilma lisapaigaldusteta)

See on **üksainus Python-skript** (`soc_top10_osint.py`), mis töötab **ilma täiendavate teekide paigaldamiseta** (kasutab ainult standardteeki).
Väljundid: CSV/JSON ja **Markdown-raport**.

## Kiirstart
```bash
python3 soc_top10_osint.py --raw-dir RAW --outdir results --md-report
```

## OSINT API võtmed (valikuline)
```bash
export ABUSEIPDB_KEY="PASTE"
export VT_API_KEY="PASTE"
export OTX_API_KEY="PASTE"
export IPINFO_TOKEN="PASTE"
```

## Väljundid (`results/`)
- `top10_summary.csv` – Top 10 Source IP & Top 10 Threat
- `ips_for_enrichment.txt` – OSINTi siht-IP-d
- `enrich/<IP>.json` – IP-de OSINT detailid
- `enrich_summary.csv` – OSINT koond
- `internal_analysis.csv` – sisevõrgu analüüs
- `Top10_Enrichment_Report_<Seade>_<YYYY-MM-DD>.md` – Markdown-raport
