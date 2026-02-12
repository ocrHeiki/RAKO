# Oixio LIVIO häkk masina uurimine

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





### Seletus
ARP spoofing (tuntud ka kui ARP poisoning) on küberründe tüüp, kus ründaja saadab kohalikku võrku võltsitud ARP-teateid.

Selle eesmärk on "petta" sinu arvutit ja ruuterit arvama, et ründaja seade on keegi teine (tavaliselt on ründaja eesmärk teeselda väravat ehk ruuterit).
Kuidas see toimib?

Tavapärases olukorras seob ARP-protokoll IP-aadressi õige MAC-aadressiga. Ründe puhul toimub järgmine:

    Võltsimine: Ründaja saadab sinu arvutile sõnumi: "Mina olen ruuter (IP 192.168.1.1) ja minu MAC-aadress on [Ründaja MAC]".

    Uuendamine: Sinu arvuti usub seda ja uuendab oma ARP-tabelit.

    Vahele sekkumine: Nüüd, kui sa tahad minna internetti, saadab sinu arvuti andmed ruuteri asemel otse ründajale.

    Edastamine: Ründaja loeb andmed üle ja saadab need edasi päris ruuterile, et sa midagi kahtlast ei märkaks.

Mis on ründe tagajärjed?

Kui ründaja on end sinu ja interneti vahele "kiilunud" (Man-in-the-Middle rünnak), saab ta teha järgmist:

    Andmete pealtkuulamine: Ta näeb kogu krüpteerimata liiklust (nt vanad HTTP lehed, paroolid).

    Andmete muutmine: Ta võib veebilehtede sisu reaalajas muuta või suunata sind võltsitud lehtedele.

    Teenuse tõkestamine (DoS): Ta võib sinu andmepaketid lihtsalt "ära visata", katkestades sinu internetiühenduse.

Kuidas end kaitsta?

    Kasuta HTTPS-i: Isegi kui keegi liiklust pealt kuuleb, on andmed krüpteeritud ja loetamatud.

    VPN: Tekitab turvalise tunneli, millest ründaja läbi ei näe.

    Staatilised ARP-kirjed: Väga turvalistes võrkudes määratakse oluliste seadmete (nagu ruuter) aadressid käsitsi, et neid ei saaks dünaamiliselt muuta.

    Tuvastustarkvara: On olemas tööriistad (nt Arpwatch), mis annavad märku, kui ühe IP-aadressiga seotud MAC-aadress ootamatult muutub.
