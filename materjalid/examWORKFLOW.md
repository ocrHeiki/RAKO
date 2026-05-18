# 🚀 EKSAMI TÖÖVOOG & SPRIKKER — TEAM 10 (Kaughalduse võimekusega)

See töövoog on optimeeritud nii, et esmalt jäädvustatakse puhta võrgu seisund ning seejärel rakendatakse automatiseeritud ja käsitsi forensikat, kahjustamata olemasolevaid ründetõendeid. Kõik uuritavate masinate tulemused saadetakse automaatselt üle SCP tagasi Kali töölauale.

---

## 📅 ETTEVALMISTUSKORD (Tee kohe laboris hommiku alguses / kloonimise ajal)

Kuna kooliserveri ligipääs oli piiratud, käivita need käsud oma Kali terminalis **kohe laboris esimese asjana** (sel ajal kui masinad vSphere'is kloonivad). See võtab aega vaid hetke:

```bash
# 1. Uuenda pakette ja paigalda põhitööriistad + FreeRDP (Windowsi kaughalduseks)
sudo apt update
sudo apt install -y mc nmap zenmap-kbx net-tools iproute2 freerdp2-x11

# 2. Käivita Kali enda SSH server (Vajalik, et VALVUR master saaks raportid Kalisse saata)
sudo systemctl enable ssh
sudo systemctl start ssh

# 3. Vaata ja kirjuta üles oma Kali täpne labori-IP (Seda on vaja VALVUR-i seadistamiseks)
ip a | grep "inet "

🏁 SAMM-SAMMULINE TÖÖVOOG LABORIS
SAMM 1: Virtuaaltaristu Kaitse (Kloonimine)

    Tegevus: Enne kui puutud ühtegi masinat, tee vSphere keskkonnas kõigist itskteam10 masinatest Kloon või Snapshot.

    Miks? Kui kaughaldus või tulemüür su välja lukustab, saad sekundiga puhta seisu tagasi.

SAMM 2: Võrgu Baasjoone Kaardistamine (Zenmap)

    Tegevus: Käivita kohe oma Kali masinas Zenmap või käsurida ja pane võrk skaneerima:
    Bash

    sudo nmap -sV -O 192.168.10.0/24

    Eesmärk: Tuvastada ründaja avatud pordid enne meie sekkumist. Jäta see taustale jooksma, et hiljem eraldada VALVUR-i liiklus ründaja omast.

SAMM 3: Ühendumine Uuritavatesse Masinatesse (Kaughaldus)

Kui Zenmap näitab, et pordid on lahti, logi Kali masinast otse sisse (eeldusel, et sul on õpetaja jagatud või leitud mandaadid):

    A. Linuxi serverisse logimine (SSH):
    Bash

ssh kasutaja@192.168.10.X

B. Windowsi masinasse logimine (RDP kasutades FreeRDP-d):
Bash

    # /v: määrab sihtmärgi IP, /u: kasutaja, /p: parool, /dynamic-resolution lubab akna suurust muuta
    xfreerdp /v:192.168.10.Y /u:Administrator /p:Parool123 /dynamic-resolution +clipboard

SAMM 4: VALVUR Masterskripti Rakendamine (E-ITS Audit)

Nüüd, mil oled kaughalduse kaudu masinas sees, käivita VALVUR_master.py.

    Märkus: Veendu, et masterskripti alguses on märgitud sinna eelseadistuse sammu ajal üles kirjutatud KALI_IP.

    Masterskript teeb auditi ja saadab kõik tulemused automaatselt zip-pakina tagasi sinu Kali töölauale.

SAMM 5: Intsidentide Haldus (Ticketid)

    Registreeri VALVUR-i ja Zenmapi leitud hälbed koheselt piletisüsteemis (TicketingServer-itskteam10).

SAMM 6: Linuxi Serveri Süvaanalüüs (INTRAWEB1)

Kui oled SSH sessioonis, jahti ründajat nendega:

    Kasutajad: w ja who -a (Kes on sees ja mis käsku jooksutab?).

    Võrk reaalajas: sudo netstat -nputw (Leia ründaja ühenduse PID).

    Pahavara asukoht: sudo ls -l /proc/[PID]/exe.

    Püsivus: sudo crontab -e.

    Logide lappamine: sudo mc (Võrdle veebiloge /var/log/nginx/ ja rakenduse siseseid logisid /var/www/html/).

    Tulemüüri esmaabi (SSH elupäästja!):
    Bash

    sudo ufw allow from [Sinu_Kali_IP] to any port 22 proto tcp
    sudo ufw enable

SAMM 7: Windowsi Masina Süvaanalüüs (DC1)

RDP sessiooni kaudu ava administraatori käsurida või tööriistad:

    Võrk: netstat -fano -> Tuvasta C2 ühenduste PID-d.

    Sessioonid: compmgmt.msc -> Shared Folders -> Sessions.

    Püsivus: By Autoruns64.exe (Kontrolli ajastatud toiminguid).

    Logi-analüüs: Käivita VALVUR-i 11_turvafiltreering.py.


---

### 🗣️ Kuidas sa seda esitlusel komisjonile serveerid:

> *"Meie meeskonna metodoloogia laboris oli rangelt forensiline ja tsentraliseeritud. **Esimene samm oli keskkonna kloonimine vSphere'is**, tagamaks andmete puutumatuse. Samal ajal seadistasime oma Kali masinas valmis kaughaldusliidesed ja SSH serveri vastuvõtuks.
>  
> **Teise sammuna käivitasime Zenmapi**, et fikseerida võrgu puhas baasjoon. Kui perimeeter oli kaardistatud, sisenesime masinatesse kaughalduse teel – **Linuxisse üle SSH ja Windowsi serveritesse üle RDP, kasutades FreeRDP-d**. See võimaldas meil käivitada oma **VALVUR Master Launcheri** otse terminalist, mis pärast analüüsi lõpetamist pakkis kõik vastused kokku ja saatis need üle SCP võrgu kaudu turvaliselt tagasi meie Kali töölauale, hoides uuritavad masinad kõrvalise prügiga saastamata."*
