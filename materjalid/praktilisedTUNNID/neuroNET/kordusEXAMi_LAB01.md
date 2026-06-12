# Võrguturbe ja Tulemüüri Labori Kokkuvõte

Käesolev dokument koondab **LAB A** raames teostatud sammud: virtuaalmasina eelhäälestuse, operatsioonisüsteemi paigalduse, SSH-ühenduse loomise, korduvad `nmap` pordiskaneeringud ning `ufw` tulemüüri reeglite rakendamise koos tulemuste võrgutaseme analüüsiga.

---

## 1. Virtuaalmasina Eelhäälestus & Paigaldus

Enne masina esmakordset käivitamist seadistati võrgukaart tagamaks otsesuhtlus füüsilise ründemasina (Kali Linux) ja virtuaalse sihtmärgi (Ubuntu Server) vahel.

### Võrgukaardi seadistus (VirtualBox)
* **Režiim:** `Bridged Adapter` (Sildatud režiim).
* **Võrgukaardi nimi (Name):** Arvuti füüsiline Wi-Fi/juhtmevaba kaart (nt `wlan0`), kuna laborit viidi läbi jagatud iPhone'i kuumkoha (*Personal Hotspot*) võrgus.
* **Miks mitte NAT?** NAT režiim peidab virtuaalmasina VirtualBoxi sisevõrgu ja tulemüüri taha, mistõttu Kali Linux ei saaks sihtmärki võrgus skaneerida ega rünnata (host paistaks suletuna).

### Ubuntu Serveri paigaldamise spikker
Paigaldusprogrammi (Installer) kohustuslikud sammud ja parameetrid:
1.  **Server's name (Hostname):** `ubuntu-target`
2.  **Username:** `opilane`
3.  **Password:** `Kuber123!`
4.  **SSH Setup:** Valiti tühikuklahviga **`[X] Install OpenSSH server`**. *Kriitiline samm pordi 22 avamiseks!*
5.  **Featured Server Snaps:** Lisatarkvara ei valitud, liiguti otse nupule `Done`.
6.  Pärast installi lõppu teostati taaskäivitus (`Reboot Now`).

---

## 2. SSH Ühenduse Loomine ja IP Tuvastus

Pärast süsteemi taaskäivitust tuvastati masina IP-aadress ja viidi haldus üle Kali Linuxi terminali, et võimaldada mugavat käskude kopeerimist ja reaalajas logide jälgimist.

### IP-aadressi tuvastamine sihtmärgis
Ubuntu serveri konsoolis käivitati käsk:
