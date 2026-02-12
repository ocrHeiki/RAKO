# Infoturbeintsidendi auditidokument

## 1. Üldandmed

**Auditi nimetus:** Windows võrgu infrastruktuuri sissetungi audit - DC01, INFRA01 ja WIN10-01

**Kuupäev:** 11.02.2026

**Auditi koostaja:** Kübersecurity analüütik

**Auditeeritavad seadmed:**
- DC01 - Server 2019 domeenikontroller (WIN-OLT3UOTFTHC)
- INFRA01 - Server 2016 rakendusserver (WIN-046U9LE098R)
- WIN10-01 - Windows 10 tööjaam (DESKTOP-M3JK4DN)

## 2. Intsidendi kokkuvõte

**Millal intsident avastati:** Intsident avastati 16.11.2025 seoses võrgutegevuse anomaaliatega, kuid logianalüüs näitab, et rünnakutegevus algas juba septembris 2024 ja kestis kuni novembrini 2025.

**Kes avastas:** Süsteemide logianalüüsi käigus tuvastati kahtlased võrgutegevused ja ebaõnnestunud sisselogimiskatsed.

**Lühike kirjeldus, mis juhtus:**
Tegemist oli koordineeritud mitmeetapilise siber-rünnakuga, mille eesmärk oli kompromiteerida kogu Windows domeeni infrastruktuur. Ründaja alustas võrguskannimisega WIN10-01 tööjaamal, jätkas brute-force rünnakutega administraatorikontodele ja õnnestus saada juurdepääs domeenikontrollerile. Rünnakul avastati andmavarastus katseid, sh Active Directory andmebaasi ekspordi katseid ja Robocopy kasutamine andmete kopeerimiseks domeenikontrollerilt. Ründaja kasutas mitmeid tehnilisi tööriistu nagu Rapid7 Nexpose võrguskannimiseks, PowerShell käsklusid süsteemanalüüsiks ja Robocopy andmevarastuseks.

## 3. Intsidendi ulatus ja mõju

**Kas oli ohustatud:**

✅ **Isikuandmed:** Pille.Porgandi kasutaja Documents kaustale tehti üle 50 juurdepääsu katset, mis viitab isikuandmete potentsiaalsele varastamisele.

✅ **Ettevõtte siseandmed:** Domeenikontrolleril kasutati Robocopy-tööriista täielike õigustega, mis viitab suuremahulisele andmevarastusele, sh kõikide kasutajakontode ja volituste varastamise oht.

**Kas intsident mõjutas:**

✅ **Teisi seadmeid:** Kõik kolme peamist süsteemi mõjutati: WIN10-01 (sissekanne), INFRA01 (privileegide eskaleerimine), DC01 (domeeni kompromiteerimine).

✅ **Võrku:** Ründaja kasutas IP-aadresse 10.10.80.16 ja 10.10.80.17, viitades sisemisele võrgule ligipääsule. Võimalik lateraalne liikumine süsteemide vahel.

✅ **Teenuste toimimist:** Tuvestati Remote Desktop lubamise katseid, mis võisid mõjutada kaugteenuste turvalisust.

## 4. Tehnilised leiud

**Operatsioonisüsteem ja tarkvara seis:**
- Windows Server 2019 (DC01)
- Windows Server 2016 (INFRA01)  
- Windows 10 (WIN10-01)
- Rapid7 Nexpose installitud ja aktiivne

**Viirusetõrje logid:**
- Leiti viiteid pahavara skaneerimisele, kuid konkreetseid viirusetõrje toiminguid logides ei tuvastatud

**Tulemüür / võrguühendused:**
- Võimaldatud Remote Desktop ühendused (port 3389)
- Tuvestati netsh käskluseid tulemüüri reeglite muutmiseks
- Anonymous sisselogimised võrgust IP-aadressilt 10.10.80.16

**Kas süsteemi uuendused olid paigaldatud:**
- Logide põhjal ei tuvastatud süsteemi uuenduste paigaldamise kinnitusi
- Vanad protsessid ja käskluste viited viitavad võimalikule uuenduste puudumisele

**Lisaks tuvastatud:**
- Nmap võrguskannimine 1000+ porti
- PowerShell skriptide kasutamine süsteemanalüüsiks
- ntfsutil.exe Active Directory andmebaasi ekspordi katseks
- Robocopy andmete kopeerimiseks domeenikontrolleril

## 5. Põhjuse analüüs

**Kuidas intsident tõenäoliselt alguse sai:**
Rünnak algas võrguskannimisega WIN10-01 tööjaamal, kus Rapid7 Nexpose abil skaneeriti võrku ja identifitseeriti nõrgad kohad. 
Seejärel toimus brute-force rünnak administraatorikontodele, mille käigus õnnestus ründajal saada juurdepääs "jaak-admin" kontole. 
Pärast esmast juurdepääsu alustas ründaja lateraalset liikumist teistesse süsteemidesse.

**Inimlik eksimus / tehniline puudujääk:**
- Nõrkade paroolide kasutamine administraatorikontodel
- Võimalik puudulik viirusetõrje konfiguratsioon
- Puudulikud võrguliikluse monitorimis mehhanismid
- Administraatori õigustega liigne kasutamine tavapärastes operatsioonides

**Peamised rünnakuvektorid:**
1. Võrgureconnaissance (Nmap skaneerimine)
2. Brute-force rünnakud (61 nurjunud katset DC01-l, 56 INFRA01-l)
3. Privileegide eskaleerimine (ntdsutil kasutamine)
4. Andmevargus (Robocopy, ZIP-arhiivimine)

## 6. Riskide hinnang

| Risk | Tõenäosus | Mõju | Riskitase | Kirjeldus |
|------|-----------|------|-----------|-----------|
| Andmavargus (isikuandmed) | Kõrge | Kõrge | KRIITILINE | Pille.Porgandi Documents kausta massiivne ligipääs |
| Domeeni kompromiteerimine | Kõrge | KRIITILINE | KRIITILINE | AD andmebaasi ekspordi katse |
| Hilisemad rünnakud | Kõrge | Kõrge | KÕRGE | Ründaja omab täielikku kontrolli |
| Business continuity | Keskmine | Keskmine | KESKMINE | Võimalikud teenuste katkestused |
| Reputatsioonikahju | Keskmine | Kõrge | KÕRGE | Kliendi andmete lekke risk |

## 7. Parandus- ja ennetusmeetmed

### Kohesed tegevused:
1. **Isoleeri kõik mõjutatud süsteemid võrgust** (DC01, INFRA01, WIN10-01)
2. **Muuda kõik domeenikontode paroolid** ja keela eelmised paroolid
3. **Blokeeri kompromiteeritud IP-aadressid** (10.10.80.16, 10.10.80.17)
4. **Eemalda Rapid7 Nexpose** kui see pole volitatud tööriist
5. **Kogu forensilised tõendid** ja mälusälvestused enne süsteemide taastamist
6. **Kontrolli kõiki administraatorkontosid** ja eemalda volitamatu juurdepääs

### Soovitused tulevikuks:
1. **Implementeeri mitme-faktor autentimine** kõigile administraatorikontodele
2. **Paigalda ja konfigureeri SIEM** süsteem reaalajaliseks logide monitoorimiseks
3. **Rakenda paroolipoliitika** - kompleksed paroolid, regulaarne vahetus
4. **Vähenda administraatorite õigusi** - kasuta just-in-time (JIT) põhimõtet
5. **Segmenteeri võrk** - erista kriitilised süsteemid tavakasutajatest
6. **Rakenda võrguliikluse analüüs** tuvasta anomaalsed ühendused
7. **Koolita kasutajad** infoturbeküsimustes ja tehniliste ohtude eest
8. **Regulaarne auditeerimine** ja penetreerimistestid
9. **Varundussüsteemide parandamine** ja regulaarne testimine
10. **Incident Response protokolli** koostamine ja meeskonna treenimine

## 8. Kokkuvõte ja järeldused

**Kas intsident oli tõsine?**
Jah, intsident oli äärmiselt tõsine, kuna see viis domeenikontrolleri potentsiaalse kompromiteerimiseni, 
mis mõjutab kogu organisatsiooni IT infrastruktuuri ja võib põhjustada täieliku andmelekke.

**Kas protseduurid olid piisavad?**
Ei, olemasolevad protseduurid ei olnud piisavad. Logide analüüs näitas, et rünnak kestis mitmeid kuid enne avastamist, mis viitab puudulikule monitoorimisele ja reageerimisele. 
Võrguliikluse ja sisselogimise katsete monitorimis puudusid tõhusad mehhanismid.

**Kas on vaja muudatusi infoturbe poliitikas?**
Kindlasti on vaja põhjalikke muudatusi:
- Võimalikult kiiresti implementeerida kõrgema turvatase (null trust)
- Kohustuslik mitme-faktor autentimine kõigile süsteemidele
- Reaalajas logide kogumine ja analüüs
- Regulaarsed turvaauditid ja penetreerimistestid
- Personali pidev infoturbe koolitus

**Prioriteetne järeldus:** Domeenikontrolleri kompromiteerimise risk nõuab kohest täielikku süsteemide taastamist puhtatelt varukoopiatelt ja kõigi kasutajakontode läbivaatamist. 
Kuni süsteemide taastamiseni peaks kogu võrkutöö olema piiratud ja kriitilised operatsioonid viia läbi eraldiseisvate turvaliste kanalite kaudu.
