# Etapp 5 — OSINT (võrguliikluse ja IP-de kontroll)

See etapp kirjeldab, kuidas käsitsi kontrollida kahtlasi IP-aadresse, domeene ja URL-e veebipõhiste OSINT tööriistade abil. Eesmärk on kinnitada või välistada pahatahtlikkus.

## Eeltingimused
- Veebibrauser (Chrome/Firefox mobiilis või töölaual)
- Tasuta kontod (soovitav): VirusTotal, AbuseIPDB (ei ole kohustuslik)
- Koputamine: tee ekraanitõmmised tulemustest

## Peamised tööriistad (veebiliidesed)
- VirusTotal (https://www.virustotal.com) — IP/domain/url/hash analüüs
- AbuseIPDB (https://www.abuseipdb.com) — kogukonnapõhine IP-reputatsioon
- Shodan (https://www.shodan.io) — avatud pordid/bännerid
- Censys (https://censys.io) — alternatiiv Shodanile
- SecurityTrails / PassiveTotal — passive DNS ja ajalooline info
- Whois lookup (whois.domaintools.com / whois.net) — registreerija ja reg. kuupäev
- IPinfo / bgp.he.net — ASN ja omaniku info

## Samm-sammult IP kontroll (näide)
Oletame, et sul on IP `185.203.116.5`:

1. VirusTotal: ava leht → vali search → kleebi IP → Enter. Vaata `last_analysis_stats` (malicious, suspicious). Vaata `Relations` ja `Community` märkusi. Kui `malicious` > 0 → märgi kõrge prioriteet.  
2. AbuseIPDB: ava → IP lookup → vaata `abuseConfidenceScore` ja reported categories. Kui score > 50 → prioriteet kõrge.  
3. Shodan: ava → IP search → vaata avatud porte ja teenuseid. Kui näed anon/proxy teenuseid → kahtlus tugev.  
4. Whois / ASN: kontrolli, kas IP kuulub suurfirmale (Amazon/Microsoft/Google) või väikesele hostingu-teenusele. Kui hostingu-teenus ja IP ei ole sinu organisatsioonile omane → kahtlus.  
5. Passive DNS (SecurityTrails): vaata, millised domeenid on IP-ga seotud ja kas need muutuvad kiiresti (fast-flux).

## Domeenide kontroll (näide)
- VirusTotal domain lookup → vaata sub-domains, associated URLs.  
- Whois → vaata registreerija ja registreerimise kuupäeva (väga uus domeen = kõrgem risk).

## Mida dokumenteerida OSINT-is
Iga kontrolli kohta lisa CSV/Excel või juhtumipileti kohta rea:  
- IP/Domeen, kontrollimise kellaaeg, VT_malicious_count, Abuse_score, Shodan_ports, Whois_ASN, otsus (benign/suspicious/malicious), analüütiku nimi.

## Heuristikad otsuse tegemiseks
- VT malicious >= 3 või Abuse score > 50 → eskaleeri (🔴 Critical).  
- VT malicious == 0 kuid ASN = cloud provider ja behaviour normal → tavaliselt 🟨/🔵 (whitelist candidate).  
- Shodan näitab proxy/suspicious services → 🟧/🔴 (sõltuvalt kontekstist).

## Kiire juhend ilma kontota
- Kasuta VirusTotal veebiliidest ilma kontota (piiratud).  
- Kasuta AbuseIPDB ilma kontota (piiratud).  
- Tee ekraanitõmmised ja lisa need juhtumisse.


