# 📑 INFOTURBE KUTSEEKSAM 2026 – TIIM HeRe
## TEHNILINE RAPORT: INTSIDENDIANALÜÜS, VÕRGUFORENSIKA JA ENESEREFLEKSIOON
**Tehniline arhitekt:** Heiki Rebane (*The Might*)  
**E-ITS spetsialist:** Helena Reinhold (*The Mind*)  
**Õppeasutus:** Raplamaa Rakenduslik Kolledž  

---

## 1. Sissejuhatus ja esmased sammud võrgus (Situatsiooniteadlikkus)

Austatud komisjon. Mina vastutasin meie tiimis tehnilise ründeanalüüsi, võrgu kaardistamise, WKS1 Linuxi tööjaama forensika ning intsidentide tõrje automatiseerimise prototüüpimise eest. Minu peamine eesmärk oli kriisiolukorras luua kiiresti situatsiooniteadlikkus, kaardistada ründepind ja tagada digitaalsete tõendite muutumatu säilimine.

Minu esmased taktilised sammud eksamikeskkonda sisenemisel olid järgmised:

1. **Võrguühenduse loomine:** Ühendasin oma Kali Linuxi ründaja/uurija masina (`10.16.140.104`) eksamivõrku.
2. **Liikluse püüdmine (Wireshark):** Käivitasin koheselt taustal **Wiresharki** võrguliikluse püüdmiseks. *Forensilisest vaatest on see kriitiline baaspraktika (Best Practice)* – juhtumi algfaasis ei tea uurija kunagi, kas rünnak on juba lõppenud või reaalajas käimas. Wiresharki käivitamine tagas, et kui ründaja oleks uuesti ühendust võtnud või andmeid välja viinud, oleks meil olemas muutumatu PCAP-salvestis. Tunnistan ausalt: kuna päev kujunes ülimalt intensiivseks ja ajakriitiliseks, ei jõudnud ma seda mahukat püügilehte reaalajas analüüsida ning see töötas passiivselt taustal turvavõrguna. Kuid see tagas meile võimekuse vajadusel kogu liiklust tagantjärele uurida.
3. **Võrgu skaneerimine (Nmap):** Erinevalt graafilistest liidestest (nagu Zenmap), mis võivad suures võrgus kokku joosta või ressursse raisata, kasutasin professionaalset lähenemist ja käivitasin otse terminalist puhta **`nmap`** käsu. Nmapi abil kaardistasin sekunditega võrgus aktiivsed seadmed, tuvastades domeenikontrolleri DC1, failiserveri ja meile uurimiseks antud Linuxi tööjaama **WKS1** aadressil `10.16.140.101`.
4. **Piletisüsteemi takistus (osTicket):** Asudes ülesannete kallale intsidendihaldustarkvaras osTicket, põrkasin kohe kokku esimese pärismaailma takistusega – piletisüsteemi sisestatud ülesande kirjelduses olid märgitud valed IP-aadressid. Pärismaailmas ei ole intsidendiraportid kunagi täiuslikud. Tänu sellele, et mul oli terminalis `nmap`-iga võrk juba reaalselt üle skaneeritud, tuvastasin konfiguratsioonivea koheselt, korrigeerisin aadressid ja asusin viivitamatult lahendama kõige kriitilisemat piletit.

---

## 2. Intsident 1 – Linux WKS1 Süvaanalüüs (Kuidas ründaja tegutses)

Nagu on näha meie osTicketi piletite nimekirjast, oli meie peamiseks fookuseks **Ticket 1 - Kaotatud arvuti**. Kasutaja oli kaotanud oma sülearvuti ajavahemikus 4. mai kuni 11. mai. Minu teostatud Live Response ja logianalüüs tuvastasid järgmise eduka ründeahela:

### A. Esmakordne ligipääs (Initial Access)
Kuna antud Linuxi seadmel puudus täisketta krüpteerimine (mille Helena kaardistas meie E-ITS auditis kriitilise hälbena), oli ründajal seadmele **täielik füüsiline ligipääs**. Ta sai failisüsteemile otse ligi (näiteks kasutades Live-USB-d või ära kasutades lukustamata sessiooni) ja varastas kasutaja privaatse SSH-võtme, mis asus kaustas `audit/.ssh/id_rsa`. See võti oli ründaja jaoks "kuldvõtmeke", mis võimaldas tal hiljem võrgu kaudu legitiimse kasutajana tagasi tulla.

### B. Õiguste laiendamine (Privilege Escalation)
Uurides süsteemi logisid failist `/var/log/syslog.1`, tuvastasin, et vahetult pärast seadme kadumist 4. mail tegi ründaja interaktiivse käsu **`sudo -> su`** abil ülemineku tavakasutaja õigustest kõige kõrgematesse ehk **root-õigustesse**. Nõrga paroolipoliitika ja `sudoers` faili puuduliku seadistuse tõttu ei kohandanud süsteem ründajale piisavalt tõkkeid.

### C. Tagauksed ja püsivus (Persistence)
Saavutades piiramatud root-õigused, tagas ründaja endale püsiva ligipääsu kahe meetodiga:
1. **Lokaalsed kontod (MITRE T1136.001):** Ta lõi süsteemi kaks uut loata lokaalset administraatorkontot nimedega **`admin`** ja **`johnsmith`**.
2. **Graafiline tagauks (MITRE T1021.005):** Ta paigaldas ja käivitas süsteemse teenuse nimega **`x11vnc.service`**, mis kuulas pordil **5900**. See graafiline kaughaldustööriist (VNC) töötas taustal varjatult root-õigustes, võimaldades ründajal üle võrgu reaalajas ekraanipilti kaaperdada ja hiirt/klaviatuuri juhtida.

### D. Andmete vargus ja võrgu koormus (Exfiltration)
Ründaja seadistas **crontab**-i (automaatse ajatabeli) kaudu skripti, mis käivitas regulaarselt **`rsync`** käsu. See skript pakkis masinas olevad konfidentsiaalsed andmed ja saatis need üle võrgu ründaja hallatavasse VPN tunnelisse sihtkoha IP-aadressile **`10.8.0.1`**.

### E. Otsene forensiline tõend (Smoking Gun)
Kasutaja `.bash_history` faili muutmisaeg ja logid kinnitavad, et ründaja viimane pahatahtlik tegevus toimus **11. mail kell 12:21** – see on minutipealt see hetk, mil arvuti seaduslikule omanikule koolis/tööl tagastati. See on ümberlükkamatu tõend, et ründaja manipuleeris masinaga kuni viimase hetkeni.

---

## 3. VALVUR-i arendusprojekt ja intsidendilahendaja õppetund

Nüüd soovin ma komisjonile jagada selle eksami kõige olulisemat strateegilist ja arhitektuurset õppetundi. 

Tehnilise arhitektina oli mu esialgne ambitsioon suur: ma tahtsin ehitada midagi ennetavat, innovaatilist ja skaleeritavat. Alustasin automaatse logianalüüsi ja reageerimisprogrammi **VALVUR** prototüüpimist. VALVUR-i eesmärk oli automatiseerida protsessi: märgata reaalajas selliseid anomaaliaid nagu `x11vnc` teenuse käivitus või loata `rsync` päringud ning masin võrgust automaatselt isoleerida.

Arendusfaasis põrkusin ma kokku reaalsete koodi integratsioonide ja ajaakna piirangutega. Kuna ma alustasin kohe kõige keerulisemast ja ajamahukamast ülesandest, jooksin ma **ajahätta**. Programm ei saavutanud eksami lõpuks täielikku töökindlust (jäi nn "katkiseks programmiks").

**Kuid intsidendilahendajana andis see mulle hindamatu elulise õppetunni:**
Kriisiolukorras ei saa ehitada tarku automaatseid tõrjesüsteeme (SOAR) keskkonnas, kus baasturvalisus ja süsteemide hardening on täielikult tegemata. Kui nägin, et kood tõrgub ja aeg surub peale, tegin ma **kiire ja eduka juhtimisotsuse (Prioritiseerimise muudatuse)**: ma tõmbasin pidurit poolikule arendusprojektile ja suunasin kogu oma tehnilise väe esimese, kõige kriitilisema intsidendi käsitsi lahendamisele ja tõendite kogumisele. 

Tulemusena jäi programm küll poolikuks, kuid kriitiline pilet sai täielikult lahendatud, tõendid on koos ja ründaja tegevus sekundipealt kaardistatud. Küberturbes tuleb alati esimesena lappida kohad, mis reaalajas veritsevad, mitte üritada keset põlengut uut tulekustutisüsteemi programmeerida.

---

## 4. Tehnilised soovitused ja kerksusmeetmed (Remediation)

Selleks, et tagada organisatsiooni IT-taristu kerksus ja vältida sarnaseid ründeid tulevikus, oleme Tiim HeRe-ga rakendanud ja ette valmistanud järgmised sammud:

1. **Kohene isoleerimine ja puhastus:** Katkestasime aktiivse andmevarguse ründaja serverisse `10.8.0.1`. Eemaldasime volitusteta kasutajad `admin` ja `johnsmith` ning deaktiveerisime pahatahtliku `x11vnc.service`.
2. **Kriptograafiline rotatsioon:** Kuna SSH privaatvõti (`id_rsa`) kompromiteeriti, kuuluvad kõik sellega seotud võtmed ja sertifikaadid terves asutuses kohesele tühistamisele ning väljavahetamisele.
3. **Mobiilsete seadmete turvalisus (E-ITS meede SYS.1.3):** Kõikidele sülearvutitele juurutatakse kohustuslik **täisketta krüpteerimine (LUKS)**. See tagab, et kui seade tulevikus füüsiliselt kaob, on failisüsteem ilma krüptovõtmeta ründajale täielikult loetamatu ning SSH võtmete või logide kättesaamine on välistatud.

*Nüüd annan sõna Helenale, kes selgitab lähemalt, kuidas E-ITS standardi abil viia organisatsiooni juhtimine ja paroolipoliitika tasemele, mis sellised ründed juba baastasemel blokeerib.*
