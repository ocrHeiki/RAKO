# Täielik Juhend: Linux (Ubuntu) Logianalüüs (Hayabusa) ja Tulemuste Uurimine (VisiData) Läbi Kali Linuxi

See dokument on terviklik samm-sammuline juhend digitaalse ekspertiisi ja intsidentide lahendamise (DFIR) läbiviimiseks Linuxi (Ubuntu/Debian) sihtmärgi vastu.

---

## 1. SAMM: Ubuntu Ettevalmistus, SSH Kontroll ja IP Tuvastamine

Seda teed kooli rünnatavas või uuritavas Ubuntu (sihtmärgi) masina terminalis.

Selleks, et saaksid logifaile kopeerida otse Kali Linuxi masinasse, peab Ubuntus töötama SSH teenus.

1. Kontrolli, kas OpenSSH server on paigaldatud ja töötab (peab kuvama staatuseks "`active` (**running**)")

```bash
sudo systemctl status ssh
```
Märkus: Kui SSH pole paigaldatud, käivita: 
```
sudo apt update && sudo apt install -y openssh-server && sudo systemctl start ssh
```

TUVASTA UBUNTU IP-AADRESS
Otsi aktiivse võrguliidese (nt `eth0` või `ens33`) alt rida "`inet`" (nt. `192.168.1.150`)

```Bash
ip a
```
## 2. SAMM: Tööriistade Allalaadimine ja Seadistamine Kali Linuxis

**Seda teed Kali Linuxi kohalikus terminalis.**

Kuna **Hayabusa** on ülikiire, **paigaldame** selle **otse uurija masinasse (Kalis)**, **et** mitte raisata ohvrimasina ressursse ja **vältida jälgede rikkumist**.

Liigu kasutaja Downloads (Allalaadimised) kausta

```Bash
cd ~/Downloads
```
Laadi alla Hayabusa stabiilne Linuxi 64-bitine versioon (v3.9.0 GNU-versioon) otse GitHubist:

```Bash
wget [https://github.com/Yamato-Security/hayabusa/releases/download/v3.9.0/hayabusa-3.9.0-lin-x64-gnu.zip](https://github.com/Yamato-Security/hayabusa/releases/download/v3.9.0/hayabusa-3.9.0-lin-x64-gnu.zip)
```
Paki arhiiv lahti ja liigu uude kausta

```Bash
unzip hayabusa-3.9.0-lin-x64-gnu.zip -d hayabusa_lin
cd hayabusa_lin
```
Anna Hayabusa põhifailile käivitusõigused ning mugavuse huvides nimeta fail kohe ümber lühemaks:

```Bash
sudo chmod +x hayabusa-3.9.0-lin-x64-gnu
mv hayabusa-3.9.0-lin-x64-gnu hayabusa
```
(Märkus: Selles versioonis on reeglite uuendaja funktsioon otse põhifaili sees, eraldi hayabusa-updater faili pole vaja otsida).

Laadi alla kõige uuemad Sigma tuvastusreeglid (sh Linuxi ründereeglid) GitHubist

```Bash
./hayabusa-updater update-rules
```
Veendu, et VisiData on Kalis olemas (kui tegid juba Windowsi juhendit, on see olemas)

```Bash
sudo apt update && sudo apt install -y python3-pip && pip install visidata --break-system-packages
```
## 3. SAMM: Universaalne Logide ja Tõendite Kogumine (Käivita Ohvri Masinas!)

Selleks, et sa ei peaks eksamil mööda sihtmärgi masinat käsitsi ringi seiklema, kasutame universaalset koodiplokki. See pakib lollikindlalt kokku põhilogid, veebiserverite logid (Apache/Nginx) ja kasutajate käsurea ajalood (.bash_history). Kui mõnda teenust masinas pole, liigub skript veateadeteta edasi.

Käivita see plokk UBUNTU (ohvri) terminalis:

### 1. Pakime kokku KÕIK võimalikud logid, veebikaustad ja ajalood ühte superfaili

```Bash
sudo tar -czf /tmp/koik_logid.tar.gz \
  /var/log/auth.log* \
  /var/log/syslog* \
  /var/log/messages* \
  /var/log/apache2/ \
  /var/log/nginx/ \
  /home/*/.bash_history \
  /root/.bash_history \
  2>/dev/null
```
### 2. Saadame pakitud faili turvaliselt oma Kali masina Downloads kausta
# (MÄRKUS: Asenda 'kali' ja '192.168.1.X' oma KALI tegeliku kasutajanime ja IP-ga!)

`scp /tmp/koik_logid.tar.gz kali@192.168.1.X:~/Downloads/`

### 3. Kustutame ohvri masina ajutisest kaustast jäljed

`rm /tmp/koik_logid.tar.gz`

Nüüd liigu tagasi KALI terminali, loo uus kaust ja paki fail lahti:

```Bash
cd ~/Downloads/hayabusa_lin
mkdir target_logs
tar -xzf ~/Downloads/koik_logid.tar.gz -C ./target_logs/
```
## 4. SAMM: Linuxi Logianalüüs Hayabusaga (JSON Konvertimine)

Seda teed Kali Linuxi terminalis (kaustas `~/Downloads/hayabusa_lin`).

TÄHTIS MÄRKUS: Hayabusa põhimootor ootab vaikimisi Windowsi `.evtx` binaarfaile. Tavapäraseid Linuxi tekstilogisid sööb ta ainult JSON-formaadis. 
Kui uuritavas süsteemis on kasutusel `systemd-journald`, konverdi logi enne puhtaks JSON-iks.

Konverdi autentimise ja sudo sündmused puhtaks JSON-logiks:

```Bash
journalctl _SYSTEMD_UNIT=ssh.service + _COMM=sudo + _COMM=su + _COMM=sshd -o json > target_logs/minu_auth.json
```
Käivita Hayabusa analüüs, andes ette loodud JSON-faili ja lisades kindlasti spetsiaalse JSON-i lipu `-J`:

```Bash
./hayabusa csv-timeline -f target_logs/minu_auth.json -J -o linux_tulemus.csv
```
Terminali kuvatakse Scan wizard. Vali nooleklahvidega variant `4` või `5` (`All alert rules` või `All event and alert rules`) ja vajuta **Enter**, et analüüs käivituks.

## 5. SAMM: Tulemuste Uurimine VisiData-s

Oled Kali Linuxi terminalis ja avad värskelt genereeritud CSV-raporti.

Ava raport interaktiivse tabelina:

```Bash
vd linux_tulemus.csv
```
## 💡 Taktikaline Spikker: Mida otsida Linuxi logidest VisiData-s?

Klahvikäsud töötavad täpselt samamoodi nagu Windowsi juhendis.

Sorteeri veerg "**Level**" kahanevalt (liigu noolega veeru peale ja vajuta `[`), et tuua etteotsa `Critical` ja `High` ohud.

Vajuta `/` (interaktiivne otsing) ja trüki otsitav märksõna:

Otsingusõna VisiData-s (/)	Mida see tuvastab?
`SSH Login Failed` või `Failed password`	Näitab paroolide rüüstamise (Brute-Force) rünnakute laineid ja ründaja IP-sid.
`Accepted password` või `Accepted publickey`	Ülikriitiline! Näitab täpsed sekundid, millal ründaja sisse sai, mis kasutajaga ja mis IP-lt.
`sudo` või `COMMAND=`	Otsi, milliseid administraatori käske ründaja pärast sissesaamist jooksu pani (privileegide eskaleerimine).
`cleared`, `shrunk` või `rm -rf`	Tuvastab, kas ründaja üritas käskudega logisid kustutada või teenuseid peatada (Defense Evasion).

# 💡 Miks see Linuxi meetod on eksamil parem ja kiirem?

Selle asemel, et kopeerida Hayabusa suurt zip-faili aeglasesse sihtmärgi masinasse, seda seal lahti pakkida 
ja kohapeal vigadega võidelda, korjad sa ühe universaalse käsuga kõik võimalikud logid (sh veebi ja ajaloo) kokku ning tõmbad need sekundiga oma Kalisse.

Kuna Hayabusa on sul uurija masinas (Kalis) juba valmis seadistatud ja reeglid uuendatud, võtab terve analüüs ja VisiData tabeli avamine aega vähem kui pool minutit. Kui sul on vaja kiiresti kontrollida puhtaid tekstilogisid või veebiserveri faile (näiteks kahtlaste Webshellide leidmiseks kaustast `target_logs/var/www/html/`), on sul kogu süsteemi struktuur mugavalt oma masinas käepärast!
