🕵️‍♂️ Linuxi (WKS1) Forensiline Uurimistee: Metoodika ja Käskude Loogika
Digitaalses forensikas ei tohi käske sisestada suvaliselt. Uurimisel lähtutakse andmete kõdunemise järjekorra reeglist (Order of Volatility). See tähendab, et liigutakse kõige kiiremini kaduvatest tõenditest (võrguliiklus ja reaalajas jooksvad protsessid mälus) kuni püsivamate tõenditeni (kõvakettale salvestatud logid ja failide ajalugu).
Allolev käskude järjekord peegeldab täpselt seda metoodikat, liikudes tuvastamisest kuni raudpolt-kindla tõendusahela lukustamiseni.
🟢 SAMM 1: Situatsiooniteadlikkus ja võrgu kaardistamine
Käivitatud käsud:
1 ⁠wireshark &⁠ (taustale salvestama)
2 ⁠nmap -sV -O 10.16.140.101⁠
🔍 Miks ja kuidas me teadsime seda teha?
 Wiresharki käivitamise põhjus: See on forensika baasreegel (Best Practice). Kui uurija siseneb kompromiteeritud keskkonda, ei tea ta kunagi, kas ründaja on seal reaalajas sees või mitte. Wiresharki taustale püügilehele panemine tagab, et kui ründaja märkab meie tegevust ja üritab andmeid kiiresti kustutada või täiendavat pahavara alla laadida, jääb kogu see võrguliiklus (PCAP-failina) meile muutumatu tõendina alles.
 Nmapi käivitamise põhjus: Kuna piletisüsteemi juhendis oli vale aadress, pidime me esmalt ise reaalselt veenduma, mis seadmed ja teenused võrgus elavad. Nmap kaardistas sekunditega taristu ja kinnitas, et ohvri masin WKS1 asub aadressil ⁠.101⁠ ning sellel on avatud SSH port (22).
🔵 SAMM 2: Esmane Live Response ohvri masinas (Ohtude tuvastamine)
Käivitatud käsud:
1 ⁠top⁠ (või ⁠htop⁠ protsessorikoormuse ja mälu kontrolliks)
2 ⁠netstat -tulpn⁠ (või uuem alternatiiv ⁠ss -tulpn⁠ aktiivsete võrguühenduste tuvastamiseks)
🔍 Miks ja kuidas me teadsime seda teha?
 Põhjendus: Piletisüsteemis oli kasutaja kaebus serveri ebatavalise aegluse ja jõudluskao kohta. ⁠top⁠ käsk näitas meile, mis süsteemi koormab, kuid tõelise vastuse andis võrguporide kontroll ⁠netstat⁠ abil.
 Kuidas me tuvastasime anomaalia? ⁠netstat⁠ väljund näitas, et pordil 5900 kuulas ja võttis ühendusi vastu teenus nimega ⁠x11vnc⁠. Port 5900 on VNC (graafilise kaughalduse) standardport. Tavalisel ja turvatud Linuxi tööjaamal ei tohi graafiline kaughaldus olla avalikult võrku avatud ilma krüpteeritud tunnelita. See oli meie esimene tehniline vihje ehk kompromiteerimise indikaator (IOC - Indicator of Compromise).
🟡 SAMM 3: Püsivuse (Persistence) ja teenuse oleku uurimine
Käivitatud käsk:
 ⁠systemctl status x11vnc.service⁠
🔍 Miks ja kuidas me teadsime seda teha?
 Põhjendus: Küberturvalisuses on teada, et ründajad ei käivita oma tööriistu lihtsalt käsitsi taustale jooksmma, sest arvuti taaskäivitamisel (reboot) nad kaotaksid ligipääsu. Nad üritavad luua püsivust (Persistence).
 Kuidas me veendusime? See käsk näitas meile, et ründaja oli süsteemi loonud reaalse ⁠systemd⁠ teenusefaili. See tähendab, et graafiline tagauks oli seadistatud käivituma automaatselt koos arvutiga ja see jooksis kõige kõrgemates ehk ⁠root⁠ õigustes.
🟠 SAMM 4: Süvitsi minek logidesse ja ründeaja tuvastamine
Käivitatud käsk:
 ⁠less /var/log/syslog.1⁠ (või vastavalt operatsioonisüsteemile ⁠auth.log.1⁠)
🔍 Miks ja kuidas me teadsime seda teha?
 Põhjendus: Kuna me uurisime juhtumit nimega "Kaotatud arvuti" (Ticket 1), mis leidis aset ajavahemikus 4. mai kuni 11. mai, pidime me leidma üles täpsed kuupäevad ja tegevused logist. Tänane aktiivne logifail (⁠syslog⁠) näitab ainult viimaseid sündmusi. Linux pakib ja roteerib vanemad logid failidesse laiendiga ⁠.1⁠ või ⁠.gz⁠. Seetõttu vaatasimegi just faili ⁠syslog.1⁠.
 Kuidas teadsime, et sündmused on õiged? Logi ajaliselt tagasi kerides jõudsime 4. mai kuupäevani (päev, mil arvuti kadus). Sealt tuvastasime kaks kriitilist sündmust:
1 Käsk ⁠sudo -> su⁠ – ründaja tegi interaktiivse ülemineku tavakasutajalt otse administraatori (⁠root⁠) tasemele.
2 Käsud ⁠useradd admin⁠ ja ⁠useradd johnsmith⁠ – ründaja lõi koheselt süsteemi kaks uut lokaalset kontot ja andis neile administraatori õigused (MITRE T1136.001).
🔴 SAMM 5: Andmete väljaviimise (Exfiltration) tuvastamine
Käivitatud käsk:
 ⁠crontab -l⁠ (või globaalse faili ⁠/etc/crontab⁠ vaatamine)
🔍 Miks ja kuidas me teadsime seda teha?
 Põhjendus: Kui ründaja on loonud kontod ja graafilise tagaukse, on tema järgmine samm tavaliselt andmete vargus. Et andmeid järjepidevalt ja märkamatult välja viia, kasutatakse Linuxis automaatset ajatabelit ehk cron-i.
 Kuidas me veendusime? See käsk paljastas meile ajatabelisse lisatud peidetud skripti, mis käivitas regulaarselt ⁠rsync⁠ käsu. Skriptis oli sihtkohaks märgitud IP-aadress ⁠10.8.0.1⁠, mis viis ründaja hallatavasse VPN-tunnelisse. See tõestas ümberlükkamatult, et masinas toimub automaatne andmete eksfiltratsioon.
🔥 SAMM 6: "Smoking Gun" – Lõplik ümberlükkamatu tõend
Käivitatud käsk:
 ⁠stat /home/audit/.bash_history⁠ (või vastava kasutaja kaustas oleva käsurea ajaloo faili kontroll)
🔍 Miks ja kuidas me teadsime seda tehdä?
 Põhjendus: Et uurimine oleks juriidiliselt ja forensiliselt pädev, peame me suutma tõendada, millal ründaja tegevus masinas lõppes. Linux salvestab kasutaja sisestatud käsud ⁠.bash_history⁠ faili. Käsk ⁠stat⁠ kuvab faili täpsed metaandmed – sealhulgas viimase muutmise aja (Modify time).
 Kuidas me teadsime, et see on õige tõend? Faili viimane muutmisaeg oli 11. mai kell 12:21. See klappis minutipealt kokku hetkega, mil arvuti omanik kooli/tööle naasis ja seadme füüsiliselt tagasi sai. See andis meile raudkindla tõendi, et ründaja omas kontrolli ja tegutses masinas kuni viimase minutini enne selle omanikule tagastamist.
🏁 Kokkuvõte komisjonile: Miks me oleme tulemuses veendunud?
Meie uurimistulemus on ümberlükkamatu, sest kõik kogutud tõendid toetavad üksteist ja moodustavad loogilise ründeahela (Cyber Kill Chain):
1 Initial Access: Ketta krüpteerimise puudumine andis ründajale algse füüsilise ligipääsu.
2 Privilege Escalation: Logi ⁠syslog.1⁠ tõestab õiguste kõrgendamist (⁠sudo -> su⁠) 4. mail.
3 Persistence: Süsteemne teenus ⁠x11vnc.service⁠ pordil 5900 ja uued lokaalsed kontod tagasid püsiva tagaukse.
4 Exfiltration: ⁠crontab⁠ skript tõestab andmete sünkroniseerimist (⁠rsync⁠) suunal ⁠10.8.0.1⁠.
5 Timeline Alignment: ⁠.bash_history⁠ faili muutmisaeg (11.05 kell 12:21) seob ründaja tegevuse sekundipealt arvuti tagastamise hetkega.
See metoodiline lähenemine tagas selle, et me ei tegelenud oletustega, vaid kaardistasime rünnaku algusest lõpuni faktide põhjal.
