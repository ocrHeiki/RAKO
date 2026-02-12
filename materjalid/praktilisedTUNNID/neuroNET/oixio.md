# Oixio LIVIO häkk masina uurimine
Mida teha, et leida liiklust, mis rünnaku saanud arvuti teha üritab

## Wireshark

Kindlasti peaksid olema teised masinad kinni ja ka ruuter kinni

### Filtrid

Hüümärk `!` filtri ees keelab seda otsingut

Microsoft:
```
!(ip.geoip.dst_org == "MICROSOFT-CORP-MSN-AS-BLOCK")
```
Kerberose filter:
```
!(nbns) && !(llmnr) && !(kerberos) && !(svcctl) && !(msrpc)
```
Mõlemad koos:
```
!(ip.geoip.dst_org == "MICROSOFT-CORP-MSN-AS-BLOCK") && !(nbns) && !(llmnr) && !(kerberos)
```
# Harjutus

## Kali VM masinas
```
sudo netdiscover -r 192.168.1.0/24
```
Arpspoof:
```
sudo arpspoof -i eth0 -t 192.168.1.2 192.168.1.1
```
Split view terminalis - terminali aknal parem hiireklõps ja sama käsk vastupidise ssuunas
```
sudo arpspoof -i eth0 -t 192.168.1.1 192.168.1.2
```
Uuendame süsteemi
```
sudo apt update
```
Paigaldame Bettercap tarkvara:
```
sudo apt install bettercap -y
```
Käivitame Bettercapi
```
sudo bettercap
```
sisestame alumisel real:
```
help net.probe
exit
```
Paneme uuesti tööle:
```
sudo bettercap -eval "caplets.update; ui.update; q
sudo bettercap -eval "ui on"
```
Parem klõps "web ui http://127.0.0.1:8080" peal ja open link
ja se avab graafilise liidese

U: `user`

P: `pass`







## Seletus..
Mida me täpsemalt kasutasime, millegi jaoks

### ARP spoofing ...
tuntud ka kui ARP poisoning on küberründe tüüp, kus ründaja saadab kohalikku võrku võltsitud ARP-teateid.

Selle eesmärk on "petta" sinu arvutit ja ruuterit arvama, et ründaja seade on keegi teine (tavaliselt on ründaja eesmärk teeselda väravat ehk ruuterit).

**Kuidas see toimib?**

- Tavapärases olukorras seob ARP-protokoll IP-aadressi õige MAC-aadressiga.
  Ründe puhul toimub järgmine:
- Võltsimine: Ründaja saadab sinu arvutile sõnumi: "Mina olen ruuter (IP 192.168.1.1) ja minu MAC-aadress on [Ründaja MAC]".
- Uuendamine: Sinu arvuti usub seda ja uuendab oma ARP-tabelit.
- Vahele sekkumine: Nüüd, kui sa tahad minna internetti, saadab sinu arvuti andmed ruuteri asemel otse ründajale.
- Edastamine: Ründaja loeb andmed üle ja saadab need edasi päris ruuterile, et sa midagi kahtlast ei märkaks.

**Mis on ründe tagajärjed?**

Kui ründaja on end sinu ja interneti vahele "kiilunud" (Man-in-the-Middle rünnak), saab ta teha järgmist:

- Andmete pealtkuulamine: Ta näeb kogu krüpteerimata liiklust (nt vanad HTTP lehed, paroolid).
- Andmete muutmine: Ta võib veebilehtede sisu reaalajas muuta või suunata sind võltsitud lehtedele.
- Teenuse tõkestamine (DoS): Ta võib sinu andmepaketid lihtsalt "ära visata", katkestades sinu internetiühenduse.

**Kuidas end kaitsta?**

- Kasuta HTTPS-i: Isegi kui keegi liiklust pealt kuuleb, on andmed krüpteeritud ja loetamatud.
- VPN: Tekitab turvalise tunneli, millest ründaja läbi ei näe.
- Staatilised ARP-kirjed: Väga turvalistes võrkudes määratakse oluliste seadmete (nagu ruuter) aadressid käsitsi, et neid ei saaks dünaamiliselt muuta.
- Tuvastustarkvara: On olemas tööriistad (nt Arpwatch), mis annavad märku, kui ühe IP-aadressiga seotud MAC-aadress ootamatult muutub.

### Bettercap.. 
on võimas ja kaasaegne avatud lähtekoodiga tööriist, mida kasutatakse võrkude turvatestimiseks (penetratsioonitestimiseks). 
Kui varem oli sarnaste rünnete (nagu ARP spoofing) läbiviimiseks populaarseim tööriist Ettercap, 
siis Bettercap on selle kiirem, stabiilsem ja tunduvalt funktsionaalsem järglane.

See on nagu "Šveitsi armee nuga" häkkerile või süsteemiadministraatorile, kes soovib testida võrgu vastupidavust rünnakutele.

**Mida Bettercap teha suudab?**

https://github.com/bettercap/bettercap

Bettercap ei piirdu ainult ARP-tabelite mürgitamisega. 
Selle võimalused on väga laialdased:
- Võrgu skaneerimine: See tuvastab automaatselt kõik võrgus olevad seadmed, nende operatsioonisüsteemid ja avatud pordid.
- WiFi ründed: See suudab rünnata WiFi-võrke, püüda kinni "kätlemisi" (handshakes) paroolide murdmiseks või luua võltsitud pääsupunkte (rogue access points).
- Andmete pealtkuulamine (Sniffing): See suudab jälgida võrguliiklust ja automaatselt välja noppida sealt sisselogimisandmed, küpsised ja külastatud veebilehed.
- DNS Spoofing: See võib suunata kasutaja õigelt veebilehelt (nt pank.ee) ründaja kontrolli all olevale võltslehele.
- Bluetooth (BLE) ründed: Bettercap suudab skaneerida ja manipuleerida ka Bluetooth-seadmete vahelist suhtlust.

**Kuidas see töötab?**

Bettercap loob interaktiivse keskkonna (või veebiliidese), kus ründaja saab sisse lülitada erinevaid "mooduleid". 
Näiteks:
- Käivitatakse net.probe, et leida seadmed.
- Käivitatakse arp.spoof, et suunata liiklus läbi ründaja arvuti.
- Käivitatakse net.sniff, et hakata andmeid salvestama.

**Miks see ohtlik on?**

Tööriist on disainitud olema väga kasutajasõbralik. Kui vanasti nõudis selliste rünnakute tegemine sügavaid teadmisi käsureast ja protokollist, 
siis Bettercap automatiseerib suure osa tööst. 
See tähendab, et isegi vähesemate teadmistega ründaja võib avalikus kohvikuvõrgus teiste kasutajate andmeid varastada.

**Oluline märkus:** Bettercapi kasutamine võrkudes, mille omanik sa ei ole või kus sul puudub luba testimiseks,
on ebaseaduslik ja karistatav.
See on mõeldud eetilistele häkkeritele oma süsteemide kaitsmiseks.
