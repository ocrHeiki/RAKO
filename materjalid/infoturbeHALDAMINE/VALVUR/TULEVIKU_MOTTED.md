# VALVUR - Tulevikuarendused ja ideed

Siia on koondatud mõtted VALVUR-i edasiseks arendamiseks pärast kooliprojekti lõppu.

## 1. Arhitektuur ja andmehaldus
- **SQLite integratsioon**: CSV failide asendamine keskse andmebaasiga, et võimaldada pikaajalist trendianalüüsi.
- **Agent-põhine kogumine**: Pythoni teenus (agent), mis saadetakse masinatesse logide reaalajas tsentraliseerimiseks.
- **API liidestused**: Täielik integratsioon VirusTotal, AbuseIPDB ja Shodan API-dega.

## 2. Analüüsivõimekus
- **CVE automaatne sobitamine**: Süsteemi tarkvaraloendi (Software Inventory) võrdlemine NIST CVE andmebaasiga.
- **Tehisintellekt (ML)**: Masinõppe mudel, mis tuvastab anomaaliaid kasutajate sisselogimise aegades (nt "Impossible Travel").
- **Võrguliikluse analüüs**: PCAP failide ja Zeek/Suricata logide tugi.

## 3. Visualiseerimine ja Konteinerid
- **Konteinerite audit**: Docker ja Kubernetes konfiguratsiooni kontroll (privileged konteinerid, ohtlikud mount-punktid).
- **Unified Timeline**: Kõigi logiallikate (Win, Linux, Network) koondamine ühele kronoloogilisele teljele.
- **Web Dashboard**: Reaalajas veebiliides (React/Next.js), mis kuvab ründeid kaardil.
- **MITRE Heatmap**: Visualiseerimine, millised MITRE ATT&CK taktikad on hetkel kõige rohkem rünnaku all.
- **Täpsem MITRE sidumine**: Automaatne viitamine (nt PowerShell deobfuskatsioon -> T1059.001) kõikides raportites.

## 4. Turvalisus ja Forensika
- **Mäluforensika**: Liides Volatility 3 tööriistaga mälutõmmiste analüüsiks, et tuvastada *fileless* malware-i.
- **Logide signeerimine**: Logide krüptograafiline signeerimine, et vältida nende muutmist.
