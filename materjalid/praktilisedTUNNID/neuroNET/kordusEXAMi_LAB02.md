# Võrguliikluse Analüüs ja Pakettide Jälitus Wiresharkiga

Käesolev dokument koondab **LAB 02** raames teostatud sammud: Wiresharki paigalduse ja käivitamise ründemasinas, võrguliikluse filtreerimise taustamüra eemaldamiseks, reaalajas TCP kolmepoolse kätlemise ja Nmap salajase skaneeringu (*SYN Stealth Scan*) tuvastamise ning tulemüüri poolt blokeeritud pakettide (*DROP/DENY*) käitumise analüüsi.

---

## 1. Labori Lähtepunkt ja Võrgumuudatused

Kuna laborit jätkati uues asukohas (koduses Wi-Fi võrgus), muutusid masinate IP-aadressid. Sildatud režiim (*Bridged Adapter*) uuendas aadressid automaatselt ruuteri DHCP kaudu.

### Uued IP-aadressid võrgus:
* **Sihtmärk (Ubuntu Server):** `192.168.1.86`
* **Ründaja (Kali Linux):** `192.168.1.85`
* **Ühendus:** Haldus viidi üle Kali terminali käsuga `ssh opilane@192.168.1.86`.

---

## 2. Wiresharki Käivitamine ja Efektiivne Filtreerimine

Võrguliikluse pealtkuulamiseks ja analüüsiks käivitati Kali Linuxis graafiline pakettide püüdmise tarkvara Wireshark.

### Samm 1: Käivitamine administraatori õigustes
Kuna võrgukaardi otse jälgimine (**Promiscuous Mode**) nõuab süsteemseid õigusi, käivitati programm Kali terminalist:

Liideseks valiti aktiivne juhtmevaba võrgukaart wlan0.
Samm 2: Taustamüra filtreerimine (Kriitiline samm)

Kuna sildatud režiimis virtuaalmasin on otseühenduses internetiga, tekkis ekraanile massiivne taustamüra (IPv6 paketid, Ubuntu süsteemsed HTTP uuenduste päringud /ubuntu/dists/...).

Selleks, et isoleerida ainult ründaja ja ohvri vaheline liiklus, rakendati Wiresharki ülemisel rohelisel ribal spetsiaalsed filtrid:

Baasfilter (kogu pordi 80 liiklus):
```Plaintext

tcp.port == 80
```
Kõrgtaseme filter (isoleerib ainult Kali masinast lähtuvad rünnakupaketid):
```Plaintext

ip.src == 192.168.1.85 and tcp.port == 80
```
3. Avatud Pordi Võrguanalüüs (Olek: open)

Ubuntu serveris veenduti, et port 80 on tulemüüris avatud: sudo ufw allow 80/tcp. Seejärel sooritati Kalist pordi kontroll: sudo nmap -p 80 192.168.1.86.
Tulemus Wiresharkis (Nmap SYN Stealth Scan -sS mehaanika):

Kuigi tavapärane TCP ühendus lõpetatakse [ACK] paketiga, tuvastati Wiresharki logis järgmine kaval kronoloogia:

    [SYN] (Kali → Ubuntu): Port 51163 koputab sihtmärgi pordile 80.

    [SYN, ACK] (Ubuntu → Kali): Server vastab, kinnitades pordi avatust.

    [RST] (Kali → Ubuntu): Reset pakett (Wiresharkis kuvatud punase/musta reana).

🧠 Eksamiõpetus: Miks ründaja saadab [RST] paketi?

Kuna Nmap käivitati sudo õigustes, kasutas see vaikimisi SYN Stealth režiimi. Nmap ei loo ohvriga täielikku TCP ühendust. 
Niipea, kui ta kuuleb serverilt vastust [SYN, ACK], saab ta kinnituse, et port on avatud, ning katkestab ühenduse koheselt [RST] paketiga. 
See hoiab skaneeringu kiirena ja ei jäta jälgi vanemate veebiserverite rakenduslogidesse.

4. Filtreeritud Pordi Võrguanalüüs (Olek: filtered)

Ubuntu serveris suleti port 80 reaalajas käsuga:
Bash

`sudo ufw deny 80/tcp`

Pärast pordi sulgemist korrati Kali masinast täpselt sama Nmap käsku.
Tulemus Wiresharkis (Tulemüüri vaikiv blokeering):

Filtriga `ip.src == 192.168.1.85 and tcp.port == 80` tuvastati ekraanil järgmine pilt:

    Ekraanile ilmusid ainult korduvad eraldiseisvad [SYN] paketid erinevatelt lähteportidelt (nt 51163, 51165).

    Sihtmärgi poolt (Ubuntu IP 192.168.1.86) ei tulnud mitte ühtegi vastust (täielik raadiovaikus).

🧠 Eksamiõpetus: Kuidas käitub UFW DENY reegel võrgus?

Erinevalt REJECT reeglist, mis saadab ründajale viisaka vastuse tagasi, et port on suletud, toimib UFW DENY vaikiva seina ehk filtrina. Tulemüür püüab Kali [SYN] paketid kinni ja viskab need prügikasti (DROP). Ründaja jääb vastust ootama, mis põhjustab Nmap-i terminalis pika viivituse (timeout) ja märgib pordi staatuseks filtered.

Aruande versioon: 1.0 (LAB 02 kordusspikker)

Labori kuupäev: 2026-06-12

Tehniline fookus: Pakettide püüdmine (Packet Capturing), TCP flags (SYN, RST), Display Filters.

