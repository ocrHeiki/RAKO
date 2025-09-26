# 📑 SOC Logi Analüüsi Kokkuvõte — Näidis (DEMO)

## 1. Faili põhiandmed
- **Allikas / failinimi:** Palo Alto Threat Log (2025-09-25, viimased 24h)
- **Analüüsi aeg:** 26.09.2025 kell 10:30
- **Tööriistad:** Excel + SOC L1 Dashboard preset

## 2. Alertide üldarv ja jaotus
- Kokku: 3 450
- Critical: 20
- High: 130
- Medium: 1 200
- Low: 2 100
- Võrdlus eelmise perioodiga: High +30% suurem kui eile

## 3. Peamised ohukategooriad
1. Malware (85% High/Critical)
2. Network reconnaissance
3. Identity brute-force

## 4. Top korduvad ohud (7 päeva jooksul)
- Rule: "Suspicious DNS tunneling" (45x)
- Rule: "Multiple login failures from same IP" (32x)

## 5. Allikad ja sihtmärgid
- **Top lähte-IP:** 185.23.44.67 (Critical brute-force, korduv)
- **Top sihtmärgid:** DC1.company.local (High asset, privilege kasutaja loginid)

## 6. MITRE taktika ülevaade
- Initial Access: Critical x12
- Execution: High x45
- Exfiltration: Medium x20

## 7. Riskiskoor ja eskaleerimine
- Kõrge riskiskooriga juhtumid: 5 (RiskScore ≥ 8)
- Eskaleeritud L2 analüütikule: jah

## 8. Tehtud tegevused ja soovitused
- False Positive: VPN login alert (kontrollitud, lubatud)
- Lahendatud: Konto kasutaja 'j.kask' lukustatud (brute-force attempt)
- Eskaleeritud: intsident TCK-2025-119 SOC L2-le

---
✍️ **Analüütiku nimi / allkiri:** H.
