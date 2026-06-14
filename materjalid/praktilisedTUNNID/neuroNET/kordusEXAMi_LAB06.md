# Küberkaitse Eksami Täielik Taktikaline Töövoog (LAB06)

Käesolev juhend on meistriklassi kontrollnimekiri ja samm-sammuline töövoog (Workflow), mis seob üheks tervikuks kõik õpitud ja rakendatud küberkaitse tööriistad: **Nmap, Wireshark, UFW, Hayabusa ja Wazuh**. 

Juhend on ehitatud loogilises järjestuses – alates füüsilisest võrguühendusest ja kaardistamisest kuni reaalajas seire ning intsidendijärgse kohtuekspertiisini (Forensics).

---

## 1. Tööriistade Rollide ja Arhitektuuri Ülevaade

| Tööriist | Mis kiht see on? | Peamine ülesanne ja väärtus laboris |
| :--- | :--- | :--- |
| **Nmap** | Rünnak / Luure | Võrgu kaardistamine, elusate masinate leidmine, portide ja haavatavuste tuvastamine. |
| **Wireshark** | Võrgukiht (Network) | Toore võrguliikluse (PCAP) püüdmine ja analüüs. Näeb krüpteerimata paroole ja rünnete sisu. |
| **UFW / IPTables** | Tulemüür (Host Firewall) | Masina esmane võrgutaseme kaitse. Liikluse lubamine/blokeerimine enne serverisse jõudmist. |
| **Wazuh SIEM** | Reaalajas Seire (SOC) | Tsentraalne logide kogumine, reaalajas ohtude tuvastamine (MITRE ATT&CK) ja aktiivne tõrje. |
| **Hayabusa** | Kohtuekspertiis (Forensics) | Süsteemilogide (EVTX/Syslog) tagantjärele kiiranalüüs ohtude ja rünnakute leidmiseks sekunditega. |

---

## 2. SAMM-SAMMULINE TÖÖVOOG EKSAMIL

### SAMM 1: Võrguühenduse Verifitseerimine ja IP Tuvastamine
Enne mis tahes tööriista käivitamist tuleb tagada, et uurija tööjaam on õiges eksami/labori võrgus.

1. Kontrolli oma võrgukaarte ja saadud IP-aadressi:

Koodiväljund

Täielik töövoo fail kordusEXAMi_LAB06.md edukalt genereeritud!

```bash
   ip a
```
Vajadusel võrgu ühendamine: Kui sul pole IP-aadressi (nt eth0 liidesel), küsi ruuterilt uus aadress:
```Bash

    sudo dhclient eth0
```
Tuvasta oma võrgu CIDR vahemik (nt kui näed `inet 192.168.1.50/24`, on sinu võrguvahemik `192.168.1.0/24`).

SAMM 2: Passiivne Seire Käivitamine (Wireshark)

Wireshark peab alati minema käima enne rünnakuid või teste, et ta püüaks kinni kogu toore võrguliikluse algusest lõpuni.

Ava **Wireshark (Kali Linuxis)** ja vali õige võrguliides (nt `eth0`).

Pane käima pakettide püüdmine (Capture).

Kasuta ekraanifiltrit, et eemaldada müra ja keskenduda sihtmärkidele (asenda IP vastavalt vajadusele):
```Plaintext

    ip.addr == 192.168.1.194 || ip.addr == 192.168.1.86
```
SAMM 3: Võrgu Kaardistamine ja Pahalase Otsing (Nmap)

Tee kindlaks, millised masinad on võrgus elus ja milliseid teenuseid nad pakuvad.

Host Discovery (Leia elusad IP-d):
```Bash

sudo nmap -sn 192.168.1.0/24
```
Teenuste ja versioonide tuvastus sihtmärgil:
```Bash

sudo nmap -sV -O 192.168.1.86
```
Kõikide portide kontroll pahalase tagauste leidmiseks:
```Bash

    sudo nmap -p- 192.168.1.86
```
Märkus: Kui leiad pordi `4444` või mõne muu tundmatu kõrge pordi, viitab see aktiivsele tagauksele (reverse shell).

SAMM 4: Reaalajas Seirekeskuse Aktiveerimine (Wazuh SIEM)

Käivita keskne server ja seo kaitstavad masinad (ohvrid) selle külge.

Liigu **Ubuntu serveris** kausta `~/wazuh-docker/single-node` ja käivita SIEM:
```Bash

sudo docker compose up -d
```
Tuvasta administraatori parool:
```Bash

grep -i "password" docker-compose.yml
```
Logi sisse **Kali brauserist** (`https://<SIEM_IP>`).

Vali **Add Agent**, genereeri kood ja kleebi see ohvirmasina terminali, et aktiveerida reaalajas logide edastus:
```Bash

sudo systemctl start wazuh-agent
```
SAMM 5: Võrgutaseme Kaitse Rakendamine (UFW Tulemüür)

Kaitse ohvrimasinat rünnakute eest, seadistades lokaalse tulemüüri.

Kontrolli tulemüüri staatust sihtmärgis:
```Bash

sudo ufw status verbose
```
Määra vaikimisi reeglid (blokeeri sisenev, luba väljuv):
```Bash

sudo ufw default deny incoming
sudo ufw default allow outgoing
```
Luba kriitilised halduspordid (SSH, Wazuh Agent side):
```Bash

sudo ufw allow 22/tcp
sudo ufw allow 1514/tcp
```
Lülita tulemüür sisse:
```Bash

sudo ufw enable
```
SAMM 6: Intsidendijärgne Kohtuekspertiis ja Logianalüüs (Hayabusa)

Kui rünnak on toimunud, kasuta Hayabusat, et teha kindlaks, mis masina sees täpselt juhtus. Hayabusa on asendamatu Windowsi sündmuselogide (.evtx) ja Linuxi logide ülikiireks analüüsiks.

Liigu Hayabusa kausta ja uuenda reegleid:
```Bash

./hayabusa-updater update-rules
```
Jookse analüüs otse masina logikaustale (nt kogutud EVTX failid või Linuxi syslog):
```Bash

./hayabusa csv-timeline -d /tee/logide/kaustani -o /tee/raport.csv
```
Ava genereeritud CSV-fail LibreOffice Calcis või Excelis. Sorteeri veergu Level (otsi Critical ja High ohte). 
Hayabusa kuvab sulle täpsed kellaajad, MITRE ATT&CK tehnikad ja käivitatud pahavaralised käsud.

3. Tööriistade Sünergia Raportis (Kuidas siduda tulemused?)

Täiusliku auditiraporti kirjutamiseks seo intsidendid ajaliselt kokku järgmiselt:

  Tuvastus (Wazuh): "Kell 16:31:05 andis Wazuh SIEM häire (Level 10) - tuvastati paroolide toore jõu rünnak (Brute-Force) SSH pordile."

  Süsteemi sisu (Hayabusa): "Hayabusa logianalüüs kinnitab sama kellaaega, tuvastades Event ID 4625 (Failed Logon) kokku 450 korral ründaja IP-aadressilt."

  Võrgutõend (Wireshark): "Wiresharki PCAP failist nähtub, et ründaja kasutas automaatset skripti, 
  mis pommitas masinat TCP pakettidega sagedusega 20 paketti sekundis (vt lisatud pilt packet_capture.png)."

  Mitigatsioon (UFW): "Ohu tõrjumiseks rakendati tulemüür UFW, mis piiras SSH ühendused ainult autoriseeritud uurija IP-aadressile."

Korduseksami nõuanne: Hoia seda faili eksami ajal teisel ekraanil lahti ja liigu täpselt punkt-punktilt edasi. 
See tagab, et ühtegi etappi ei unustata ja raport on loogiliselt struktureeritud.
**"Master Workflow" (Peatöövoog)**, mis seob punkt-punktilt, samm-sammult ja kronoloogilises järjekorras kokku kõik meie tööriistad. 
See algab täpselt füüsilisest võrgu kontrollist ja liigub läbi reaalajas seire kuni tagantjärele uurimiseni.


### 🗺️ Töövoo loogiline jaotus failis (Sinu eksami strateegia):

1. **Etapp 1: Algus ja võrk (`ip a` ja `dhclient`):** Kuidas kontrollida, kas oled õiges võrgus ja kuidas ruuterilt vajadusel uut IP-d küsida.
2. **Etapp 2: Ennetav seire (Wireshark):** Kuidas panna võrgukaart kohe alguses taustale pakette püüdma, et mitte midagi kaotsi ei läheks.
3. **Etapp 3: Luure ja pahalase otsing (Nmap):** Käsud elusate masinate leidmiseks, versioonide tuvastamiseks ja pahalase peidetud tagaustega portide (nt `4444`) avastamiseks.
4. **Etapp 4: Keskne turvajuhtimine (Wazuh SIEM):** Dockeri käivitamine, parooli leidmine ja agendi sidumine ohvirmasinaga, et SOC tööle hakkaks.
5. **Etapp 5: Host-taseme kaitse (UFW tulemüür):** Kuidas ohvrimasin lukku keerata (vaikimisi `deny incoming`), aga jätta lahti kriitilised pordid (SSH, Wazuh 1514).
6. **Etapp 6: Kohtuekspertiis (Hayabusa):** Kuidas pärast rünnakut tõmmata masinast logid, uuendada Hayabusa reegleid ja luua sekundiga võimas CSV-ajajoon, mis reedab ründaja iga liigutuse.



### 💡 Miks see töövoog raportis maksimumpunktid toob?
Sellepärast, et see näitab **professionaalset intsidentidele reageerimise (Incident Response) elutsüklit**. 
Sa ei tee asju suvalises järjekorras, vaid liigud metoodiliselt: 
*Tuvasta võrk -> Pane käima salvestus -> Leia ohud -> Püstitas seire -> Rakenda kaitse -> Analüüsi logisid*. 
