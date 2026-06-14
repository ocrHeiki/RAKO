# Wazuh SIEM Eksami Taktikaline Töövool ja Arhitektuur (LAB04)

Käesolev juhend kirjeldab strateegilist ja taktikalist töövoolu, mida rakendada kohe pärast eksamikeskkonda (virtuaallaborisse) sisenemist. 
Juhend selgitab, kuidas SIEM-põhist küberkaitse võimekust reaalajas üles ehitada, milliseid masinaid jälgida ja kuidas logisid tsentraalselt hallata.

---

## 1. Taktikaline Esmane Tegevuskava (Eksami algus)

Niipea kui saavutatakse ligipääs eksamikeskkonnale, tuleb koheselt alustada tsentraalse "peamaja" ehk seirevõimekuse loomist. 
See tagab, et kõik hilisemad rünnakud, testid ja konfiguratsioonid salvestatakse taustal automaatselt tõendusmaterjaliks.


```text
[ Eksamikeskkonda sisenemine ]
              │
              ▼
[ Tuvasta masinate IP-aadressid (ip a / ifconfig) ]
              │
              ▼
[ Käivita keskne Wazuh SIEM server (Docker paigaldus) ]
              │
              ▼
[ Logi sisse Dashboardile (admin / SecretPassword) ]
              │
              ▼
[ Genereeri Agendi paigalduskäsk ja vii see ohvirmasina(te)sse ]
```
2. Võrguarhitektuur ja Agentide Jaotamise Loogika

Küberkaitse laborites ja eksamitel jagunevad masinad rollide järgi. Reegel on lihtne: Agendid paigaldatakse alati ohvritele/sihtmärkidele, mitte kunagi ründajale.
2.1 Arhitektuuri skeem
```Plaintext

┌─────────────────────────────────┐
│     RÜNDEMASIN (Kali Linux)     │
│  - Teeb rünnakuid (Nmap, jne)   │
│  - EI OMA Wazuh Agenti          │
└────────────────┬────────────────┘
                 │
                 │ (Rünnakud läbi võrgu)
                 ▼
┌─────────────────────────────────┐       (Saadab logid pordile 1514)     ┌──────────────────────────────────┐
│    OHVIRMASIN / SIHTMÄRK        ├──────────────────────────────────────>│    WAZUH SIEM SERVER (Docker)    │
│  - Jooksevad teenused (SSH, jt) │                                       │  - Kogub, analüüsib ja kuvab     │
│  - OMAB Wazuh Agenti (Aktiivne) │                                       │  - Dashboard veebiliides         │
└─────────────────────────────────┘                                       └──────────────────────────────────┘
```
2.2 Rollide jaotus laboris

    Wazuh Manager / Server (Keskne süsteem): Kogub logisid, teostab korrelatsiooni, 
    kontrollib logisid reeglistiku (Ruleset) vastu ja genereerib häireid (Alerts).

    Jälgitavad masinad (Ohvrid / Serverid): Omavad kergkaalulist Wazuh Agenti. 
    Agent loeb pidevalt kohalikke logisid (nt /var/log/auth.log, Windows Event Logs) 
    ja saadab muudatused krüpteeritult porti 1514 serverile.

    Ründemasin (Kali Linux): Toimib välise ohutegurina. 
    Teda ei jälgita seestpoolt, vaid tema tekitatud anomaaliaid 
    ja rünnakujälgi tuvastatakse läbi ohvri turvakaamerate (agentide).

3. Samm-sammuline Seadistamine Eksamis
Samm 1: IP-aadresside kaardistamine

Enne konfiguratsioonide tegemist tuvasta kõigi masinate IP-d, et vältida valede andmete sisestamist agendi genereerimisel.
```Bash

# Kontrolli võrgukaarte ja aadresse
ip a
```
Samm 2: Serveri käivitamine ja sisselogimine

Käivita keskkond (vastavalt LAB01 juhendile) ja logi sisse. Tuvasta parool vajadusel põhifailist:
```Bash

grep -i "password" docker-compose.yml
```
Samm 3: Uue agendi liitmine (Wazuh veebiliidesest)

Liigu pealehel või menüüs valikule **Add agent** (või **Deploy new agent**).

Vali sihtmärgi operatsioonisüsteem (nt `DEB amd64` Ubuntu puhul või `RPM` CentOS puhul).

Sisesta väljale **Server address** oma unikaalne `Wazuh Serveri IP-aadress`.

Kopeeri veebiliidese poolt genereeritud ametlik **wget / curl käsurida.**

Samm 4: Käsu täitmine sihtmärgis

Sisene ohvirmasina terminali, kleebi kopeeritud käsk (kasutades sudo õigusi) ja käivita teenus:
```Bash

sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```
4. Reaalajas Tõendamise ja Seire Kontroll (Kolmik-test)

Et veenduda süsteemi toimimises enne reaalsete eksamiülesannete lahendamist, soorita kiire funktsionaalsuse test:

**Wireshark (Kali):** Pane käima filter `ip.addr == <Wazuh_Serveri_IP>`, et näha toorest liiklust.

**Nmap (Kali):** Tee kiire pordiskaneering ohvri suunas: `sudo nmap -F <Ohvri_IP>`.

**Wazuh Dashboard:** Ava `Modules -> Security events` ja veendu, et graafikule tekkis reaalajas piik ning sündmuste nimekirja ilmusid kirjed ründemasina IP-aadressiga.

**Selle struktuuri rakendamine eksami esimese 15 minuti jooksul tagab eduka, dokumenteeritud ja automaatselt seirega kaetud eksamisoorituse.**

### 🗺️ Eksami taktikalise ülesehituse ülevaade (faili sisu):

1. **Esmased sammud (0–15 minutit eksamil):** Tuvasta masinate reaalsed IP-aadressid (`ip a`), pane kohe esimese asjana taustale püsti keskne Wazuh SIEM server ja logi veebiliidesesse sisse.
2. **Agentide loogika ja jaotus:** * **Wazuh Server:** Sinu tsentraalne "peamaja", mis võtab logisid vastu pordil `1514`.
   * **Ohvirmasinad/Kliendid:** Kõik masinad, mida sa pead eksamil kaitsma või ründama – neisse kõigisse läheb kergkaaluline **Wazuh Agent**, mis hakkab logisid serverisse saatma.
   * **Ründemasin (Kali Linux):** Toimib välise ohuallikana. **Kalile me agenti külge ei pane**, sest me tahame näha, kuidas ohvrite "turvakaamerad" (agendid) Kali rünnakuid väljastpoolt tuvastavad.
3. **Kolmepoolne verifitseerimine:** Kiire spikker, kuidas kontrollida (Nmap + Wireshark + Wazuh kaudu), kas sinu ülesseatud "püünis" töötab korrektselt enne, kui hakkad põhilisi eksamiülesandeid lahendama.
