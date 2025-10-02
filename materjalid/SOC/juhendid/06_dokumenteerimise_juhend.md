# SOC 24h Palo Alto Analüüsi Checklist ✅

## Etapp 1 — Excel (L1 triage)
- [ ] Ava log.csv Excelis või Google Sheetsis
- [ ] Sorteeri `Risk of app` (kõrge -> madal)
- [ ] Lisa värvikoodid (🔴, 🟧, 🟨, 🔵)
- [ ] Salvesta eraldi filtrid: proxy_logs, dns_logs, ssl_logs, smb_logs
- [ ] Lisa `triage_note` iga anomaalia juurde

## Etapp 2 — Pandas (L1→L2, kui võimalik)
- [ ] Lae log.csv Pandasega
- [ ] Filtreeri Risk>=4
- [ ] Ekspordi Top 20 Destination IP
- [ ] Ekspordi Top 20 Source IP (DNS päringud)
- [ ] Märgi kahtlased → OSINT kontroll

## Etapp 3 — Visualiseerimine
- [ ] Loo riskipirukas (värvikoodidega)
- [ ] Loo Top Destination ja Top Source graafikud
- [ ] Loo sessions/hour joonis (tipphetked)
- [ ] Salvesta PNG-d

## Etapp 4 — OSINT kontroll
- [ ] Kontrolli IP VirusTotal-is
- [ ] Kontrolli AbuseIPDB-s
- [ ] Kontrolli Shodan-is (avatud pordid)
- [ ] Kontrolli Whois / ASN (pilv vs väike hosting)
- [ ] Märgi otsus: 🔴/🟧/🟨/🔵

## Etapp 5 — SIEM (kui ligipääs on)
- [ ] Tee Splunk/Elastic päring risk>=4
- [ ] Kontrolli DNS masspäringuid ühelt IP-lt
- [ ] Kontrolli SMB liiklust tööjaamade vahel
- [ ] Salvesta otsingu tulemused ticketi juurde

## Etapp 6 — Dokumenteerimine
- [ ] Täida märkmiku mall (IP, OSINT tulemused, otsus)
- [ ] Lisa ekraanitõmmised VT/Abuse/Shodanist
- [ ] Eskaleeri 🔴/🟧 vastavalt SOC protsessile
- [ ] Märgi valepositiivid eraldi (AWS, CDN jne)

---
**Märkus:** Hoia checklist telefonis/Markdownis, saad kiiresti punkte üle vaadata praktika käigus.
