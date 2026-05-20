

# 📑 INFOTURBE KUTSEEKSAM 2026 – TIIM HeRe
## TEHNILINE RAPORT: PROJEKT VALVUR, INTSIDENDIANALÜÜS JA VÕRGUFORENSIKA
**Tehniline arhitekt:** Heiki Rebane (*The Might*)  
**E-ITS spetsialist:** Helena Reinhold (*The Mind*)  
**Õppeasutus:** Raplamaa Rakenduslik Kolledž  

---

## 1. Järje ülevõtmine, võrgu kaardistamine ja piletisüsteemi takistused

"Austatud komisjon. Ma võtan siit Helenalt järje üle. Kui Helena kaardistas meie organisatsiooni strateegilised puudused ja E-ITS auditi tulemused, siis minu ülesandeks oli siseneda reaalsete tehniliste kontrollide tasemele, luua situatsiooniteadlikkus ja lahendada piletisüsteemi sisestatud kriisid.

Minu esmased taktilised sammud eksamikeskkonda sisenemisel olid järgmised:

1. **Võrguühenduse loomine:** Ühendasin oma Kali Linuxi masina (`10.16.140.104`) eksamivõrku.
2. **Liikluse püüdmine (Wireshark):** Käivitasin koheselt taustal **Wiresharki** võrguliikluse püüdmiseks. Forensilisest vaatest töötas see passiivselt taustal turvavõrguna, et tagada meile võimekus vajadusel kogu liiklust tagantjärele PCAP-failist uurida.
3. **Võrgu skaneerimine (Nmap):** Kasutasin professionaalset lähenemist ja käivitasin otse terminalist puhta **`nmap`** käsu. Nmapi abil kaardistasin sekunditega võrgus aktiivsed seadmed, tuvastades domeenikontrolleri DC1, failiserveri ja Linuxi tööjaama **WKS1** aadressil `10.16.140.101`.
4. **Piletisüsteemi takistus (osTicket veebiaadressi viga):** Asudes ülesannete kallale, põrkasin kohe kokku esimese takistusega. Kõigile jagatud ülesande kirjelduses oli märgitud vale veebiaadress. Juhendis oli link kujul `tickets.kehtna.lan/scp`, mis viitas haldusliidesele, kuid tegelik toimiv aadress oli hoopis `tickets.kehtna.lan/osticket/`. See viga ja õige aadressi väljaselgitamine võttis minu masinaga alguses ära väärtuslikku aega. Kui aga aadress sai korrigeeritud, avanes meile piletisüsteem ja asusin lahendama kriitilisi juhtumeid.

---

## 2. Esmane fookus: Projekt VALVUR ja prioritiseerimise õppetund

Alustasin tööd piletisüsteemis kõige kõrgema prioriteediga juhtumist ehk **Piletist nr 2 (Malware/Serveri koormus)**. Kuna tegu oli kriitiliselt kõrge ohuga, oli minu esialgne ambitsioon tehnilise arhitektina suur: ma ei tahtnud lahendada probleemi lihtsalt käsitsi, vaid luua ennetava ja innovaatilise lahenduse tuleviku jaoks.

Selleks alustasin automaatse logianalüüsi ja reageerimisprogrammi **VALVUR** prototüüpimist ja testimist. VALVUR-i eesmärk oli automatiseerida ohtude tõrjumist: märgata reaalajas süsteemi anomaaliaid (nagu loata kaughaldusteenused või andmete väljavool) ning masin võrgust automaatselt isoleerida.

**Kus tekkis takerdumine:**
Arendusfaasis põrkusin ma kokku keeruliste koodi integratsioonide ja süsteemi eripäradega. Kuna ma kulutasin selle omaloodud programmi käivitamisele ja silumisele liialt palju väärtuslikku aega ja ressurssi, programm eksami ajaaknas täielikult tööle ei hakanudki.

**Suurim õppetund intsidendilahendajana:**
See oli minu jaoks hindamatu reaalne õppetund. Kriisiolukorras ei saa ehitada tarku automaatseid tõrjesüsteeme keskkonnas, kus baasturvalisus on täielikult tegemata. Nähes, et kood tõrgub ja aeg surub peale, tegin ma **kiire ja eduka juhtimisotsuse**: tõmbasin poolikule arendusprojektile pidurit, muutsin prioriteete ning suunasin kogu oma fookuse ja tehnilise väe teise kriitilise juhtumi käsitsi lahendamisele. 

---

## 3. Intsident 1 – Linux WKS1 Süvaanalüüs (Käsitsi forensika edu)

Võtsin järgmisena ette **Pileti nr 1 - Kaotatud arvuti**. Kasutaja oli kaotanud oma sülearvuti ajavahemikus 4. mai kuni 11. mai. Kuna olin VALVUR-i arendusest liikunud puhta forensika peale, suutsin logide põhjal sekundipealt tuvastada ründaja tegevusahela:

* **Esmakordne ligipääs (Initial Access):** Kuna seadmel puudus täisketta krüpteerimine (E-ITS auditi kriitiline hälve), kasutas ründaja ära **füüsilist ligipääsu**, sai failisüsteemile otse ligi ja varastas kasutaja privaatse SSH-võtme (`audit/.ssh/id_rsa`).
* **Õiguste laiendamine (Privilege Escalation):** Süsteemi logid failist `/var/log/syslog.1` näitavad, et 4. mail tegi ründaja interaktiivse käsu **`sudo -> su`** abil ülemineku tavakasutaja õigustest kõige kõrgematesse ehk **root-õigustesse**.
* **Tagauksed ja püsivus (Persistence):** Saavutades root-õigused, tagas ründaja endale püsiva ligipääsu kahe meetodiga:
  1. Ta lõi süsteemi kaks uut loata lokaalset administraatorkontot nimedega **`admin`** ja **`johnsmith`** (**MITRE T1136.001**).
  2. Ta paigaldas ja käivitas süsteemse teenuse nimega **`x11vnc.service`** pordil **5900**, võimaldades ründajal üle võrgu graafiliselt ekraanipilti kaaperdada (**MITRE T1021.005**).
* **Andmete vargus (Exfiltration):** Ründaja seadistas **crontab**-i kaudu skripti, mis käivitas regulaarselt **`rsync`** käsu, pakkis konfidentsiaalsed andmed ja saatis need üle võrgu ründaja VPN tunnelisse sihtkoha IP-aadressile **`10.8.0.1`**.
* **Otsene forensiline tõend (Smoking Gun):** Kasutaja `.bash_history` faili muutmisaeg kinnitab, et ründaja viimane pahatahtlik tegevus toimus **11. mail kell 12:21** – see on minutipealt see hetk, mil arvuti seaduslikule omanikule tagastati. Ründaja manipuleeris masinaga kuni viimase minutini.

---

## 4. Tehnilised soovitused ja kerksusmeetmed (Remediation)

Kuigi programm VALVUR jäi poolikuks, tagas minu käsitsi läbiviidud forensika selle, et saime intsidendi edukalt isoleeritud ja kaardistatud. Oleme Tiim HeRe-ga ette valmistanud järgmised sammud taristu parandamiseks:

1. **Puhastus:** Katkestasime aktiivse andmevarguse suunal `10.8.0.1`, eemaldasime lokaalsed kontod `admin` ja `johnsmith` ning deaktiveerisime `x11vnc.service`.
2. **Kriptograafiline rotatsioon:** Kuna SSH privaatvõti kompromiteeriti, kuuluvad kaikki sellega seotud võtmed terves asutuses kohesele tühistamisele.
3. **Mobiilsete seadmete turvalisus (E-ITS meede SYS.1.3):** Kõikidele sülearvutitele juurutatakse kohustuslik **täisketta krüpteerimine (LUKS)**. See tagab, et kui seade tulevikus füüsiliselt kaob, on failisüsteem ilma krüptovõtmeta ründajale täielikult loetamatu.

Sellega on minu tehniline ülevaade lõppenud. Aitäh! Oleme valmis vastama komisjoni küsimustele."

1. Sissejuhatus, võrgu kaardistamine ja piletisüsteemi takistused
Austatud komisjon. Mina vastutasin meie tiimis tehnilise ründeanalüüsi, võrgu kaardistamise, WKS1 Linuxi tööjaama forensika ning intsidentide tõrje automatiseerimise prototüüpimise eest. Minu eesmärk oli luua kiiresti situatsiooniteadlikkus, kaardistada ründepind ja tagada digitaalsete tõendite säilimine.
Minu esmased taktilised sammud võrku sisenemisel olid järgmised:
1 Võrguühenduse loomine: Ühendasin oma Kali Linuxi masina (⁠10.16.140.104⁠) eksamivõrku.
2 Liikluse püüdmine (Wireshark): Käivitasin koheselt taustal Wiresharki võrguliikluse püüdmiseks. Forensilisest vaatest töötas see passiivselt taustal turvavõrguna, et tagada meile võimekus vajadusel kogu liiklust tagantjärele PCAP-failist uurida.
3 Võrgu skaneerimine (Nmap): Kasutasin professionaalset lähenemist ja käivitasin otse terminalist puhta ⁠nmap⁠ käsu. Nmapi abil kaardistasin sekunditega võrgus aktiivsed seadmed, tuvastades domeenikontrolleri DC1, failiserveri ja Linuxi tööjaama WKS1 aadressil ⁠10.16.140.101⁠.
4 Piletisüsteemi takistus (osTicket veebiaadressi viga): Asudes ülesannete kallale, põrkasin kohe kokku esimese takistusega. Kõigile jagatud ülesande kirjelduses oli märgitud vale veebiaadress. Juhendis oli link kujul ⁠tickets.kehtna.lan/scp⁠, mis viitas haldusliidesele, kuid tegelik toimiv aadress oli hoopis ⁠tickets.kehtna.lan/osticket/⁠. See viga ja õige aadressi väljaselgitamine võttis minu masinaga alguses ära väärtuslikku aega. Kui aga aadress sai korrigeeritud, avanes meile piletisüsteem ja asusin lahendama kriitilisi juhtumeid.
2. Esmane fookus: Projekt VALVUR ja prioritiseerimise õppetund
Alustasin tööd piletisüsteemis kõige kõrgema prioriteediga juhtumist ehk Piletist nr 2 (Malware/Serveri koormus). Kuna tegu oli kriitiliselt kõrge ohuga, oli minu esialgne ambitsioon tehnilise arhitektina suur: ma ei tahtnud lahendada probleemi lihtsalt käsitsi, vaid luua ennetava ja innovaatilise lahenduse tuleviku jaoks.
Selleks alustasin automaatse logianalüüsi ja reageerimisprogrammi VALVUR prototüüpimist ja testimist. VALVUR-i eesmärk oli automatiseerida ohtude tõrjumist: märgata reaalajas süsteemi anomaaliaid (nagu loata kaughaldusteenused või andmete väljavool) ning masin võrgust automaatselt isoleerida.
Kus tekkis takerdumine:
Arendusfaasis põrkusin ma kokku keeruliste koodi integratsioonide ja süsteemi eripäradega. Kuna ma kulutasin selle omaloodud programmi käivitamisele ja silumisele liialt palju väärtuslikku aega ja ressurssi, programm eksami ajaaknas täielikult tööle ei hakanudki.
Suurim õppetund intsidendilahendajana:
See oli minu jaoks hindamatu reaalne õppetund. Kriisiolukorras ei saa ehitada tarku automaatseid tõrjesüsteeme keskkonnas, kus baasturvalisus on täielikult tegemata. Nähes, et kood tõrgub ja aeg surub peale, tegin ma kiire ja eduka juhtimisotsuse: tõmbasin poolikule arendusprojektile pidurit, muutsin prioriteete ning suunasin kogu oma fookuse ja tehnilise väe teise kriitilise juhtumi käsitsi lahendamisele.
3. Intsident 1 – Linux WKS1 Süvaanalüüs (Käsitsi forensika edu)
Võtsin järgmisena ette Pileti nr 1 - Kaotatud arvuti. Kasutaja oli kaotanud oma sülearvuti ajavahemikus 4. mai kuni 11. mai. Kuna olin VALVUR-i arendusest liikunud puhta forensika peale, suutsin logide põhjal sekundipealt tuvastada ründaja tegevusahela:
 Esmakordne ligipääs (Initial Access): Kuna seadmel puudus täisketta krüpteerimine (E-ITS auditi kriitiline hälve), kasutas ründaja ära füüsilist ligipääsu, sai failisüsteemile otse ligi ja varastas kasutaja privaatse SSH-võtme (⁠audit/.ssh/id_rsa⁠).
 Õiguste laiendamine (Privilege Escalation): Süsteemi logid failist ⁠/var/log/syslog.1⁠ näitavad, et 4. mail tegi ründaja interaktiivse käsu ⁠sudo -> su⁠ abil ülemineku tavakasutaja õigustest kõige kõrgematesse ehk root-õigustesse.
 Tagauksed ja püsivus (Persistence): Saavutades root-õigused, tagas ründaja endale püsiva ligipääsu kahe meetodiga:
1 Ta lõi süsteemi kaks uut loata lokaalset administraatorkontot nimedega ⁠admin⁠ and ⁠johnsmith⁠ (MITRE T1136.001).
2 Ta paigaldas ja käivitas süsteemse teenuse nimega ⁠x11vnc.service⁠ pordil 5900, võimaldades ründajal üle võrgu graafiliselt ekraanipilti kaaperdada (MITRE T1021.005).
 Andmete vargus (Exfiltration): Ründaja seadistas crontab-i kaudu skripti, mis käivitas regulaarselt ⁠rsync⁠ käsu, pakkis konfidentsiaalsed andmed ja saatis need üle võrgu ründaja VPN tunnelisse sihtkoha IP-aadressile ⁠10.8.0.1⁠.
 Otsene forensiline tõend (Smoking Gun): Kasutaja ⁠.bash_history⁠ faili muutmisaeg kinnitab, et ründaja viimane pahatahtlik tegevus toimus 11. mail kell 12:21 – see on minutipealt see hetk, mil arvuti seaduslikule omanikule tagastati. Ründaja manipuleeris masinaga kuni viimase minutini.
4. Tehnilised soovitused ja kerksusmeetmed (Remediation)
Kuigi programm VALVUR jäi poolikuks, tagas minu käsitsi läbiviidud forensika selle, et saime intsidendi edukalt isoleeritud ja kaardistatud. Oleme Tiim HeRe-ga ette valmistanud järgmised sammud taristu parandamiseks:
1 Puhastus: Katkestasime aktiivse andmevarguse suunal ⁠10.8.0.1⁠, eemaldasime lokaalsed kontod ⁠admin⁠ ja ⁠johnsmith⁠ ning deaktiveerisime ⁠x11vnc.service⁠.
2 Kriptograafiline rotatsioon: Kuna SSH privaatvõti kompromiteeriti, kuuluvad kõik sellega seotud võtmed terves asutuses kohesele tühistamisele.
3 Mobiilsete seadmete turvalisus (E-ITS meede SYS.1.3): Kõikidele sülearvutitele juurutatakse kohustuslik täisketta krüpteerimine (LUKS). See tagab, et kui seade tulevikus füüsiliselt kaob, on failisüsteem ilma krüptovõtmeta ründajale täielikult loetamatu.
Aitähh! 
