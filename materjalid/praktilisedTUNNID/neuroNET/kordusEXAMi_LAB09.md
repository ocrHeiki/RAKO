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
Märkus: Kui SSH pole paigaldatud, käivita: `sudo apt update && sudo apt install -y openssh-server && sudo systemctl start ssh`

TUVASTA UBUNTU IP-AADRESS
Otsi aktiivse võrguliidese (nt `eth0` või `ens33`) alt rida "`inet`" (nt. `192.168.1.150`)

```Bash
ip a
```
2. SAMM: Tööriistade Allalaadimine ja Seadistamine Kali Linuxis

**Seda teed Kali Linuxi kohalikus terminalis.**

Kuna **Hayabusa** on ülikiire, **paigaldame** selle **otse uurija masinasse (Kalis)**, **et** mitte raisata ohvrimasina ressursse ja **vältida jälgede rikkumist**.

Liigu kasutaja Downloads (Allalaadimised) kausta

```Bash
cd ~/Downloads
```
Laadi alla Hayabusa stabiilne Linuxi 64-bitine versioon (v3.9.0) otse GitHubist

```Bash
wget [https://github.com/Yamato-Security/hayabusa/releases/download/v3.9.0/hayabusa-3.9.0-lin-x64.zip](https://github.com/Yamato-Security/hayabusa/releases/download/v3.9.0/hayabusa-3.9.0-lin-x64.zip)
```
Paki arhiiv lahti ja liigu uude kausta

```Bash
unzip hayabusa-3.9.0-lin-x64.zip -d hayabusa_lin
cd hayabusa_lin
```
Anna Hayabusa põhifailile ja uuendajale käivitusõigused

```Bash
chmod +x hayabusa-3.9.0-lin-x64 hayabusa-updater
```
Mugavuse huvides nimeta pikk käivitatav fail ümber lühemaks

```Bash
mv hayabusa-3.9.0-lin-x64 hayabusa
```
Laadi alla kõige uuemad Sigma tuvastusreeglid (sh Linuxi ründereeglid) GitHubist

```Bash
./hayabusa-updater update-rules
```
Veendu, et VisiData on Kalis olemas (kui tegid juba Windowsi juhendit, on see olemas)

```Bash
sudo apt update && sudo apt install -y python3-pip && pip install visidata --break-system-packages
```
3. SAMM: Logifailide Tõmbamine Ubuntust Kalisse (SCP)

Seda teed Kali Linuxi kohalikus terminalis (kaustas `~/Downloads/hayabusa_lin`).

Kuna me uurime Linuxit, huvitavad meid peamiselt kaks logifaili: `/var/log/auth.log` (autentimised, sudo, SSH) ja `/var/log/syslog` (üldised süsteemi sündmused). 
Loome Kalisse ajutise kausta ja tõmbame logid turvaliselt üle võrgu.

Loo Hayabusa kausta sisse uus kataloog ohvri logide jaoks

```Bash
mkdir target_logs
```
Kopeeri turvaliselt Ubuntust kriitilised logifailid kohalikku kausta
MÄRKUS: Asenda 'kasutaja' ja '192.168.1.150' Ubuntu tegeliku kasutajanime ja IP-ga!

```Bash
scp kasutaja@192.168.1.150:/var/log/auth.log ./target_logs/
scp kasutaja@192.168.1.150:/var/log/syslog ./target_logs/
```
Küsimisel sisesta Ubuntu kasutaja parool.

4. SAMM: Linuxi Logianalüüs Hayabusaga

Seda teed Kali Linuxi terminalis (kaustas `~/Downloads/hayabusa_lin`).

Nüüd paneme Hayabusa tõmmatud Linuxi logisid purema. Hayabusa kasutab integreeritud Sigma reegleid, et tuvastada automaatselt SSH brute-force rünnakud, kahtlased sudo käsud ja jälgede kustutamised.

Käivita analüüs kogutud logide kaustale

```Bash
./hayabusa csv-timeline -d target_logs/ -o linux_tulemus.csv
```
5. SAMM: Tulemuste Uurimine VisiData-s

Oled Kali Linuxi terminalis ja avad värskelt genereeritud CSV-raporti.

Ava raport interaktiivse tabelina

```Bash
vd linux_tulemus.csv
```

# 💡 Taktikaline Spikker: Mida otsida Linuxi logidest VisiData-s?
Klahvikäsud töötavad täpselt samamoodi nagu su Windowsi juhendis, kuid Linuxi puhul otsi neid spetsiifilisi ründeid:

Sorteeri veerg "**Level**" kahanevalt (liigu veeru peale ja vajuta `[`), et tuua etteotsa `Critical` ja `High` ohud.

Vajuta / (otsing) ja trüki:

`SSH Login Failed` -> Näitab toore jõu (Brute-Force) rünnakute laineid ja ründaja IP-sid.

`Accepted password` -> Ülikriitiline! Näitab täpsed sekundid, millal ründaja parooli ära arvas ja sisse sai.

`sudo` -> Otsi, milliseid administraatori käske ründaja pärast sissesaamist jooksu pani.

`cleared` või `shrunk` -> Tuvastab, kas ründaja üritas käskudega nagu `echo "" > auth.log` logisid kustutada (Defense Evasion).


### 💡 Miks see Linuxi meetod on eksamil parem ja kiirem?
Selle asemel, et kopeerida Hayabusa zip-faili aeglasesse sihtmärgi masinasse, seda seal lahti pakkida ja terminalis vigadega võidelda, 
**tõmbad sa kahe kiire scp käsuga puhtad tekstilogid oma Kalisse**. 

Kuna Hayabusa on sul Kalis juba valmis seadistatud ja uuendatud, võtab terve analüüs ja VisiData tabeli avamine aega vähem kui 30 sekundit. See säästab eksamil tohutult aega!
