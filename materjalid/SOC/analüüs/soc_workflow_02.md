# 🧠 SOC L1 käsitsi OSINT ja jätkuanalüüsi juhend  
### Jätk 24h ja nädala alertide kokkuvõttele (Palo Alto Threat logid)

---

## 🎯 Eesmärk

See juhend kirjeldab **SOC L1 taseme töövoogu**, mida kasutada pärast esmast 24h või nädala logianalüüsi.  
Fookuses on **madala raskusastmega (LOW)**, kuid **sagedased** sündmused, mis võivad olla **valepositiivid (false positives)**.  
Juhend sobib olukordadeks, kus automaatset OSINT-skripti ei saa kasutada — kõik tehakse **käsitsi**.

---

## 🪜 Ülevaade töövoost

1. **Alus:** valmis 24h / week report Palo Alto Threat logidest  
   → Top 10 Source IP, Top 10 Threat/Content Name, Severity, Action, Application, Port, Time  
2. **Fookus:** korduvad **LOW + ALLOW** sündmused  
3. **Eesmärk:** tuvastada võimalikud **valepositiivid** või **päris ohuindikaatorid**

---

## ⚙️ Samm 1 — Otsusta, kas uurid IP-d või signatuuri

### Kui Threat/Content Name viitab **anomaaliale või skännimisele**
Näited:  
- `Nmap Aggressive Option Print Detection(94318)`  
- `OpenSSL Handshake Cipher Two More Times Changed Anomaly(31120)`  
- `SSL Double Client Hello Cipher Suite Length Mismatch(32467)`

➡ Tegemist on **võrgu- või TLS-protokolli anomaaliaga**, mitte otsese ründega.

**Tee järgmist:**
- Kontrolli, kas allikas on **sise skänner** või automaatne töö (nt Nmap -A, vuln scan).  
- Vaata `Application` ja `Destination Port` — kui 80/443/53, on tihti tavaline liiklus.  
- Kontrolli `Action=allow` ja `Severity=low` → võimalik valepositiiv.  
- Ava [**Palo Alto Threat Vault**](https://threatvault.paloaltonetworks.com/) ja otsi signatuuri ID või nimi — vaata, mida signatuur tegelikult kontrollib ja kas on soovitatud tuning.

---

### Kui Threat/Content Name viitab **konkreetsel pahavarale või CVE-le**
Näited:
- `Suspicious C2 Traffic`
- `MSRPC DCOM Exploit Attempt`
- `ET TROJAN Downloader`

➡ Tegemist on **tõelise ohuga** või vähemalt kahtlase tegevusega.

**Tee järgmist:**
- Kontrolli IP maine (vt OSINT tööriistu allpool).  
- Vaata, kas samal ajal ilmnes EDR-i, proxy või auth logides kõrvalekaldeid.  
- Kui mitmes allikas on “malicious” → eskaleeri L2/L3-le.

---

## 🔍 Samm 2 — Kontrolli logikontexti

| Kontrollpunkt | Küsimus | Miks oluline |
|----------------|----------|---------------|
| **Source IP** | On see sisevõrk (10.x / 172.16-31 / 192.168)? | Sise-IP võib olla legitiimne seadme liiklus |
| **NAT IP** | Kas NAT väli viitab avalikule IP-le? | Avalik IP tuleb OSINT’iga kontrollida |
| **Action** | ALLOW või DENY? | ALLOW + LOW = FP-kandidaat |
| **Frequency** | mitu korda kordub? | Regulaarne muster = automatiseeritud töö |
| **Rule / App / Port** | Kas vastab ootusele? | Nt “http” 443 peal on ok |
| **Time Logged** | On kindel kellaaeg (nt 01:00)? | Ajastatud töö – FP |

---

## 🌐 Samm 3 — Käsitsi OSINT (veebipõhine)

### A. IP keskne kontroll
| Tööriist | Eesmärk | Link |
|-----------|----------|------|
| **AbuseIPDB** | Kas IP on kuritarvitatud? (score, raportid) | [https://www.abuseipdb.com/](https://www.abuseipdb.com/) |
| **VirusTotal** | IP analüüs, seotud domeenid, failid | [https://www.virustotal.com/](https://www.virustotal.com/) |
| **AlienVault OTX** | Kas IP on ohu pulse’is? | [https://otx.alienvault.com/](https://otx.alienvault.com/) |
| **Cisco Talos** | Maine ja kategooria | [https://talosintelligence.com/reputation_center/](https://talosintelligence.com/reputation_center/) |
| **GreyNoise** | Kas tegemist on skänneriga / internetimüraga? | [https://viz.greynoise.io/](https://viz.greynoise.io/) |
| **Shodan / Censys** | Avatud teenused ja bännerid | [https://www.shodan.io/](https://www.shodan.io/), [https://search.censys.io/](https://search.censys.io/) |
| **RIPEstat / ARIN / BGP.he.net** | IP omanik, ASN, riik | [https://stat.ripe.net/](https://stat.ripe.net/), [https://bgp.he.net/](https://bgp.he.net/) |

---

### B. Signatuuri keskne kontroll
| Tööriist | Eesmärk | Link |
|-----------|----------|------|
| **Palo Alto Threat Vault** | Signatuuri kirjeldus ja soovitused | [https://threatvault.paloaltonetworks.com/](https://threatvault.paloaltonetworks.com/) |
| **SSL Labs Server Test** | TLS tervisekontroll (avalikud sihtkohad) | [https://www.ssllabs.com/ssltest/](https://www.ssllabs.com/ssltest/) |
| **Hardenize** | Ülevaade: DNS, TLS, MTA, poliitikad | [https://www.hardenize.com/](https://www.hardenize.com/) |

---

## 📊 Samm 4 — Graylog testkeskkonnas käsitsi analüüs

1. Ava Graylog ja vali **Search → Severity:LOW AND Type:THREAT**
2. Kasuta **Quick Values**:
   - `threat/content name`
   - `source address`
   - `application`
3. Lisa **ajagraafik (per hour)**, et tuvastada korduv ajastus
4. Drill-down TOP Threat/Content või IP peale
5. Salvesta otsing nimega:
   - `LOW Repeaters 24h`
   - `LOW Repeaters 7d`

Saad kiirelt tuvastada korduvaid FP sündmusi ja mustreid.

---

## 🧩 Samm 5 — Otsustuspuu (L1 tasemel)

| Tulemus | Tunnused | Tegevus |
|----------|-----------|----------|
| **False Positive (FP)** | LOW, ALLOW, korduv muster, GreyNoise “internet noise”, legitiimne App | Märgi FP, tee reeglitäpsustus (exclude või threshold) |
| **Suspicious** | Segatud SEV (LOW/HIGH), DENY, ebatavaline App või Port | Vajab L2 kontrolli / lisa logid |
| **Malicious** | HIGH/CRITICAL, pahavara/C2, mitmes allikas “malicious” | Eskaleeri L2/L3 |

---

## 🧰 Samm 6 — Kiirvahendid (Windows / käsurida)

**PowerShell:**
```powershell
Resolve-DnsName example.com
Test-NetConnection example.com -Port 443
```

**WHOIS ja BGP päringud:**
- [RIPEstat](https://stat.ripe.net/)
- [ARIN WHOIS](https://whois.arin.net/)
- [BGP.he.net](https://bgp.he.net/)
- [BGP.Tools](https://bgp.tools/)

---

## 🪄 Samm 7 — Dokumenteerimine (Word / SOC logiraamat)

Lisa iga kontrolli kohta lühikirje:

| Väli | Näide |
|------|-------|
| **Case ID** | SOC-L1-2025-10-17-LOW01 |
| **Periood** | 24h (16.–17.10.2025) |
| **Logifail(id)** | threat-log-2025-10-17.csv |
| **Top Finding** | `Nmap Aggressive Option Detection` – 172.27.66.0/24 |
| **Kontrollid** | AbuseIPDB: OK (0 reports), GreyNoise: scanner, Talos: benign |
| **Järeldus** | False Positive – sisemine Nmap skänn |
| **Soovitus** | Reegli täpsustus „exclude internal scanner“ või signatuuri tuning |

---

## 🧭 Samm 8 — Praktiline ajaplaan

| Etapp | Kestus | Tulem |
|-------|---------|--------|
| Graylog “LOW Repeaters” otsing | 10 min | 3–5 korduvat IP-d |
| OSINT kontroll 3 IP-le | 15–20 min | maine ja signatuuride ülevaade |
| Dokumenteerimine | 10 min | Word / SOC raport |
| Kokku | ~45 min | FP või ohu kinnitamine |

---

## 💡 Kokkuvõte

See juhend annab sulle SOC L1 tasemel **käsitsi kontrollimise töövoo** olukorras, kus automaatne OSINT või enrichment pole lubatud.  
Sa saad siiski:
- kiiresti tuvastada **valepositiivid** (LOW kordused),
- valideerida **signatuuri käitumist** Threat Vaultist,
- kasutada **avalikke OSINT tööriistu** IP-de ja maine kontrolliks,
- ja dokumenteerida tulemused SOC standardi järgi.

---

📄 **Failinimi:** `SOC_L1_Manual_OSINT_Jatk.md`  
🧑‍💻 **Autor:** ocrHeiki (GitHub: [https://github.com/ocrHeiki](https://github.com/ocrHeiki))  
📅 **Versioon:** v1.0 – 2025-10-17  
