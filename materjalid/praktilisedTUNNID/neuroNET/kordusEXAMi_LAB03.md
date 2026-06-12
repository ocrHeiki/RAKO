# Wazuh SIEM Küberturvalisuse Labori Juhend (Korduseksam)

Käesolev juhend on koostatud spetsiaalselt korduseksami praktilise labori läbiviimiseks ja dokumenteerimiseks. 
Juhend sisaldab kogu vajalikku infot Wazuh SIEM keskkonna püstitamise, agendi sidumise ja kolmepoolse turvaanalüüsi **(Nmap + Wireshark + Wazuh)** teostamise kohta.

---

## 1. Laborikeskkonna Arhitektuur ja IP-aadressid

Tööd teostatakse kahes peamises virtuaalmasinas, mis asuvad ühises lokaalses võrgus:
1. **Ründaja / Analüütiku masin (Kali Linux):** * Kasutatakse pordiskaneeringute tegemiseks (Nmap) ja võrguliikluse monitoorimiseks (Wireshark).
2. **Küberkaitse server (Ubuntu):** * **IP-aadress:** `192.168.1.194`
   * Masinas jookseb Dockeris kogu Wazuh SIEM (Indexer, Manager, Dashboard) ning lokaalne Wazuh Agent.

---

## 2. Wazuh SIEM Paigaldamine ja Käivitamine Dockeris

Wazuh stabiilse versiooni `v4.7.2` single-node paigaldus viiakse läbi isoleeritud Dockeri keskkonnas, et vältida operatsioonisüsteemi hoidlate või GPG-võtmete konflikte.

### Samm 1: Indekseerija sertifikaatide genereerimine
Käivita Ubuntu serveris kaustast `~/wazuh-docker/single-node`:

Kinnitus: Konteiner peab edukalt käivituma ja looma vajalikud krüptograafilised võtmed turvaliseks HTTPS-suhtluseks.
Samm 2: SIEM süsteemi käivitamine
```Bash

sudo docker compose up -d
```
Oodatav väljund: Kõik kolm peamist teenust peavad näitama staatust Started:

    Container single-node-wazuh.indexer-1 Started

    Container single-node-wazuh.manager-1 Started

    Container single-node-wazuh.dashboard-1 Started

3. Administreerimine ja Paroolide Tuvastamise Teekond (Troubleshooting)

Kui veebiliidesesse (https://192.168.1.194) sisenemisel viskab süsteem veateadet “Invalid username or password”, on erinevates Dockeri versioonides parooli tuvastamiseks kindel samm-sammuline kontrollteekond.
Samm 1: Automaatselt genereeritud paroolide faili kontroll

Mõnes Wazuh Dockeri alamversioonis luuakse unikaalsed paroolid faili. Seda saab kontrollida käsuga:
```Bash

cat /home/opilane/wazuh-docker/single-node/config/wazuh_indexer/wazuh-passwords.txt
```
Märkus: Kui terminal vastab No such file or directory, liigu järgmise sammu juurde.
Samm 2: Varjatud keskkonnamuutujate (.env) faili kontroll

Kui spetsiaalset tekstifaili pole, võivad paroolid olla peidetud keskkonnamuutujate faili. Liigu kausta ~/wazuh-docker/single-node ja kontrolli selle sisu:
```Bash

cat .env
```
Märkus: Kui ka seda faili selles konfiguratsioonis ei eksisteeri, tähendab see, et paroolid on määratud otse konteinerite põhilises käivitusfailis.
Samm 3: Konfiguratsiooni (docker-compose.yml) seest otsimine (Edukas meetod)

Kõige kindlam viis paroolide must valgel leidmiseks on filtreerida põhilist konfiguratsioonifaili PASSWORD märksõna järgi:
```Bash

grep -i "password" docker-compose.yml
```
Selle tulemusena tuvastatud ja reaalset laborit avavad vaikeandmed:

Kasutajatunnus (Username): `admin`

Parool (Password): `SecretPassword` (Märkus: Täpselt sellisel kujul, ilma hüumärgita lõpus, suure S- ja P-tähega).

(Tuleb aktsepteerida ka brauseri SSL sertifikaadi hoiatus: Advanced -> Accept the Risk and Continue)

4. Lokaalse Wazuh Agendi Paigaldus

Agendi paigaldamiseks Ubuntu põhimasinasse laetakse stabiilne .deb pakett alla otse failina, möödes apt-hoidlate võimalikest vigadest:
Samm 1: Paketi allalaadimine ja paigaldus
Bash

wget [https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.7.2-1_amd64.deb](https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.7.2-1_amd64.deb) && sudo WAZUH_MANAGER='192.168.1.194' dpkg -i ./wazuh-agent_4.7.2-1_amd64.deb

Samm 2: Teenuse käivitamine
```Bash

sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```
Samm 3: Verifitseerimine

Käsu sudo systemctl status wazuh-agent tulemusena peab teenus olema roheline ehk active (running). Wazuh Dashboardil ilmub pealehele Active agents: 1 (wazuh-server olek on active 🟢).
5. Kolmepoolne Turvaanalüüs (Nmap + Wireshark + Wazuh)

Labori põhiosa eesmärk on rünnaku tuvastamine ja visualiseerimine kolmes erinevas kihis.
1. Võrgukiht: Wireshark (Kali Linux)

Käivita Wireshark Kali Linuxis ja pane see kuulama liidest (nt eth0 või ens33). Rakenda ekraanifilter:
```Plaintext

ip.addr == 192.168.1.194
```
See tagab, et nähtaval on vaid Kali ja Wazuh vaheline puhas võrguliiklus.
2. Rünnakukiht: Nmap Skaneering (Kali Terminal)

Käivita Kali terminalist agressiivne versioonituvastusega skaneering sihtmärgi pihta:
```Bash

sudo nmap -sV -p 22,80,443,1514 192.168.1.194
```
See kontrollib serveri põhilisi teenuseid ning tuvastab pordid, luues võrku selge anomaalia.
3. Tuvastuskiht: Wazuh SIEM Dashboard

Wazuh agent märkab võrgupakettide laviini ning süsteemilogide järsku muutust ja edastab selle reaalajas kesksüsteemile.

    Security Events: Veebiliideses (Modules -> Security events) tekib graafikule järsk piik (Alert level evolution).

    MITRE ATT&CK: Wazuh tuvastab tegevuse ja kaardistab selle ründetehnikate vastu (nt Valid Accounts või Sudo and Sudo Caching).

    Events nimekiri: Vahekaardil Events on näha detailsed kirjed juhtunud intsidendist koos ründaja IP-aadressi ja ohutasemega.

Eksami sooritamiseks kohustuslikud kuvatõmmised: Nmap käsk Kali terminalis, Wiresharki püütud TCP paketid ja Wazuh Dashboardi aktiivne agent koos Security Events graafiku piigiga.
