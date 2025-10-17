# SOC L1 – Palo Alto Threat Log Analysis & OSINT Enrichment Tool

## 🧭 Kirjeldus
See tööriist loeb Palo Alto tulemüüri logisid kaustast `RAW/`, analüüsib neid ja koostab automaatselt:
- Top 10 allika IP-d
- Top 10 ohu / sisu nimetust (Threat/Content Name)
- Madala raskusastmega (LOW) sündmuste kordused (võimalikud false positive’d)
- Internal subnet analüüsi (sisevõrgu IP-de kontekst)
- OSINT enrichment (AbuseIPDB, VirusTotal, AlienVault OTX, ipinfo, rDNS, WHOIS)
- Word-raporti koos kokkuvõtte ja soovitustega
