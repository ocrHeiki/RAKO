# SOC Praktikandi Rollid (L1 tase)

See dokument annab ülevaate SOC praktikandi (Level 1) tüüpilistest ülesannetest ja töövoost. Praktika eesmärk on anda kogemus infoturbe monitooringus, intsidentide esmastes tegevustes ja turbelahenduste haldamises.

---

## 🔐 SOC praktikandi (L1) tüüpilised rollid

### 1. Monitooring ja triaaž
- Jälgida SIEM-i (nt ELK, Splunk, Wazuh, QRadar) häireid ja logivooge.  
- Eristada **vale-positiivseid** ja **tõelisi intsidente**.  
- Vajadusel eskaleerida intsident L2 analüütikule.  

➡️ Praktikandi vaates: õpid tundma, mis on normaalne liiklus ja mis on kahtlane.

---

### 2. Intsidentide esmase käsitluse toetus
- Koguda infot kahtlase sündmuse kohta (IP, kasutaja, seade, kellaaeg, tegevus).  
- Dokumenteerida tehtud tegevused.  
- Sulgeda pilet või edastada see edasi L2-le.  

➡️ Praktikandi vaates: harjutad kiiret reageerimist ja intsidendi logimist.

---

### 3. Turbelahenduste haldamise abistamine
- Viirusetõrje ja EDR alertide ülevaatus.  
- IDS/IPS logide jälgimine (nt Snort, Suricata).  
- VPN-i, tulemüüri ja proxy logide kontroll.  

➡️ Praktikandi vaates: saad kogemuse, kuidas töötavad erinevad turbetööriistad.

---

### 4. Raportite ja dokumentatsiooni koostamine
- Igapäevased/igakuised turberaportid.  
- Logistatistika kokkuvõtted (nt top 10 IP-d).  
- SOP (Standard Operating Procedure) juhiste järgimine.  

➡️ Praktikandi vaates: õpid infot struktureerima ja tiimile arusaadavalt esitama.

---

### 5. OSINT ja ohuluure toetamine
- Kontrollida, kas ettevõtte IP-d/domeenid on mustades nimekirjades.  
- Koguda IOC-sid (Indicators of Compromise).  
- Teha lihtsamaid taustauuringuid (nt Shodan, VirusTotal).  

➡️ Praktikandi vaates: tutvud ohuluure tööriistade ja meetoditega.

---

### 6. Automatiseerimine ja väiksemad projektid
- Lihtsad skriptid (nt logide puhastamine, failide sorteerimine).  
- Dashboardide loomine (Kibana, Grafana).  
- Uute logiallikate testimine SIEM-is.  

➡️ Praktikandi vaates: kui sul on Pythoni/Linuxi oskust, saad katsetada automatiseerimist.

---

## 🧭 Kokkuvõte
SOC praktikandi töö hõlmab:
- **Logide jälgimist ja intsidentide triaaži.**
- **Esmast intsidentidele reageerimist ja dokumenteerimist.**
- **Turbelahenduste ja raportite toetamist.**
- **OSINT ja ohuluure lihtsamaid tegevusi.**
- **Väikseid arendus- või automatiseerimisprojekte.**

See annab tugeva aluse, et liikuda edasi L2 analüütiku tasemele, kus rollid on sügavam tehniline analüüs ja intsidentide lahendamine.

---

## 📊 Praktikandi töövoog

SOC praktikandi tööprotsess (L1 tasemel) näeb välja järgmiselt:

[Alert SIEM-is]
    ↓
[Praktikant (L1) kontrollib logi]
    ↓
[Kas vale-positiivne?]
    ├─ Jah → [Sulgeb pileti / dokumenteerib]
    └─ Ei  → [Kogub lisainfot (IP, kasutaja, seade, kellaaeg)]
                 ↓
            [Esmane dokumenteerimine ja pilet]
                 ↓
            [Eskaleerimine L2 analüütikule või sulgemine]
