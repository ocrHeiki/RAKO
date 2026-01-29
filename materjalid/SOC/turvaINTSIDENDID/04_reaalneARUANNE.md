Reaalse intsidendi näidisaruanne
1. Kokkuvõte juhtkonnale (Executive Summary)

Intsidendi ID: INC2019-0422-022

Kriitilisus: Kõrge (P2)

Staatus: Lahendatud

Ülevaade: 22. aprilli öösel 2019, täpselt kell 01:05:00, tuvastas SampleCorp’i turvakeskus (SOC) sisevõrgus autoriseerimata tegevuse. See ilmnes anomaalsete protsesside käivitamise ja kahtlaste PowerShell-käskude kaudu. Kasutades ära nõrka võrgupääsu kontrolli ja kahte turvahaavatavust, saavutas ründaja kontrolli järgmiste sõlmede üle:

    WKST01.samplecorp.com: Tarkvaraarenduseks kasutatav süsteem.

    HR01.samplecorp.com: Töötajate ja partnerite andmete töötlemiseks kasutatav süsteem.

SOC koostöös DFIR (digitaalne kohtuekspertiis ja intsidentidele reageerimine) üksusega isoleeris ohu, eemaldas pahavara, parandas turvaaugud ja taastas süsteemide algse oleku.

Peamised leiud: Puuduliku võrgupääsu kontrolli tõttu sai ründaja sisevõrgu IP-aadressi, ühendades oma arvuti lihtsalt SampleCorp’i kontori Etherneti porti. Uurimine näitas, et esmane sisenemispunkt oli WKST01, kus kasutati ära Acrobat Readeri vana versiooni haavatavust. Edasi liiguti HR01 serverisse, kasutades ära puhvri ületäitumise haavatavust SampleCorp’i enda arendatud rakenduses. Kuigi massiivset andmete väljaviimist ei tuvastatud, on mõlema süsteemi kompromiteerimise tõttu põhjust pidada kliendi- ja töötajate andmeid potentsiaalselt ohustatuks.

Kohesed tegevused: Süsteemid isoleeriti VLAN-segmenteerimise abil. Uurimiseks koguti võrguliikluse püüdmise faile (PCAP), rakendati hosti turvalahendus ja sündmuste logid koondati Elastic SIEM-i.
2. Mõjuanalüüs huvigruppidele

    Kliendid: Mõnede teenuste ajutine katkestus ja API-võtmete tühistamine. Võimalik usalduse kaotus.

    Töötajad: HR01 sisaldas isikukoode ja pangakontode andmeid. Esineb identiteedivarguse oht.

    Partnerid: Arenduskeskkonnas viibimine tähendab, et intellektuaalne omand (lähtekood) võis paljastuda.

    Regulaatorid: Võimalikud trahvid andmekaitse nõuete puuduliku täitmise eest.

3. Tehniline analüüs
Mõjutatud süsteemid ja andmed

    WKST01.samplecorp.com: Sisaldab tulevaste tarkvaraversioonide lähtekoodi ja kolmandate osapoolte API-võtmeid. Ründaja sirvis erinevaid katalooge.

    HR01.samplecorp.com: Personalijuhtimise süsteem. Kõige murettekitavam on ligipääs krüpteerimata andmebaasile, mis sisaldas töötajate isikukoode ja panganduse detaile.

Tõendusmaterjalide analüüs (WKST01)

Tuvastati PowerShell-käsk, mis käivitati cmd.exe kaudu ja mis laadis alla skripti siseaadressilt 192.168.220.66. See kinnitas, et ründaja oli füüsiliselt võrgus kohal.

    Sisenemisvektor: Kasutaja avas Mozilla Thunderbirdis faili cv.pdf, mis käivitas haavatava Adobe Reader 10.0 kaudu pahaloomulised käsud.

Analüüs: 192.168.220.66 (Ründaja seade)

SIEM päring tuvastas, et ründaja kasutas seda aadressi WKST01 ja HR01 ründamiseks. HR01 puhul kasutati porti 31337 ja teostati puhvri ületäitumise rünnak.

Kompromiteerimise indikaatorid (IoC):

    C2 IP: 192.168.220.66

    cv.pdf (SHA256): ef59d7038cfd565fd65bae12588810d5361df938244ebad33b71882dcf683011

4. Algpõhjuse analüüs (Root Cause)

    Puudulik võrgupääsu kontroll (NAC): Võimaldas võõra seadme ühendamist füüsilisse porti.

    Vananenud tarkvara: Acrobat Readeri paikama jäetud versioon.

    Turvaauk omatootes: Puhvri ületäitumise viga HR-rakenduses.

    Puudulik segmenteerimine: Võimaldas vaba liikumist arendusmasinast HR-serverisse.

5. Tehniline ajajoon (Technical Timeline)
Aeg (22. aprill 2019)	Tegevus
00:27:27	Töötaja avas cv.pdf, ründaja sai esmase ligipääsu (WKST01).
00:50:18	Ründaja tegi sisevõrgu luuret ja leidis HR01 haavatavuse.
01:30:12	Juurdepääs krüpteerimata andmebaasile ja andmete pakkimine väljaviimiseks.
02:30:11	SOC tuvastas tegevuse ja isoleeris süsteemid VLAN-i abil.
03:43:34	Tulemüüri reeglid uuendatud, ründaja C2 aadress blokeeritud.
04:30:00	Süsteemide paikamine (Adobe Readeri uuendus).
06:33:44	HR-rakenduse erakorralise paiga (patch) juurutamine.
6. Rünnaku olemus ja Metasploiti tuvastamine

SOC analüüsis PowerShell-käske ja tuvastas kahekordse kodeeringu (double encoding), mida kasutatakse tavaliselt tuvastusmehhanismidest mööda hiilimiseks. Dekodeeritud koodi võrdlemisel avatud lähtekoodiga luureandmetega (OSINT) selgus, et tegemist on Metasploit raamistikuga. VirusTotal kinnitas, et shellcode sisaldas shikata_ga_nai kooderit, mis on Metasploitile omane.
7. Taastamine ja edasised sammud

    Võrgupääsu tühistamine: Kasutaja sisselogimised tühistati ja paroolid lähtestati. API-võtmed genereeriti uuesti.

    Andmete taastamine: Süsteemid taastati kontrollitud varukoopiatest pärast pahavara täielikku eemaldamist.

    Seire: Rakendati käitumisanalüütika, et märgata kõrvalekaldeid tavapärasest võrguliiklusest.

    Tuleviku strateegia: Üleminek Zero-Trust mudelile ja töötajate küberhügieeni koolituste tõhustamine.
