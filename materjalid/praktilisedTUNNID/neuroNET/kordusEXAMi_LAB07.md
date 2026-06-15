# WAZUH + WIRESHARK FILTRITE KOONDJUHEND (LAB07)

## SAMM 1: Eelluure ja võrgu skaneerimine (Reconnaissance)
Ründaja püüab kaardistada võrku ja leida avatud porte.

**1. Wazuh filter (Otsi rünnaku algust):**
 Kopeeri otsinguribale: ```⁠rule.id: (31101 OR 31103 OR 31533) OR rule.description: "Port scanning"```
 Mida jälgida: Otsi ründaja IP-aadressi (`⁠data.srcip`⁠) ja täpset kellaaega, millal pakettide laviin algas.

**2. Wireshark filter (Võta võrgutõend):**
 Kirjuta filtriribale: `⁠ip.src == <Ründaja_IP> && tcp.flags.syn == 1 && tcp.flags.ack == 0`⁠
 Mida eriliselt jälgida: Kui näed, et ühelt IP-lt lendab sekundis sadu pakette erinevatele portidele, on see kuulikindel tõend Nmap skaneeringust.

## SAMM 2: Paroolirünnakud ja sissemurd (Brute-Force & Initial Access)
Ründaja proovib automaatsete tööriistadega (Hydra, Medusa jne) paroolidest läbi murda.

**1. Wazuh filter (Otsi rünnakut ja õnnestumist):**
 Kopeeri otsinguribale: `⁠rule.id: (5712 OR 5715 OR 5720 OR 18152)`⁠
 Mida jälgida: ⁠`5712`⁠ näitab rünnakut ennast. **Kõige kriitilisemalt otsi reeglit `⁠5715`⁠ (Successful SSH login)** – see annab sulle sekundipealt teada, millal ründaja sisse sai.

**2. Wireshark filter (Vaata rünnaku sagedust):**
 Kirjuta filtriribale: `⁠ip.addr == <Ohvri_IP> && tcp.port == 22`⁠ (või port `⁠3389`⁠ Windowsi RDP puhul).
 Mida eriliselt jälgida: Jälgi ühenduste tihedust. Kui näed suurt hulka ⁠SSHv2⁠ pakette ilma pikemate vahedeta, on tegu toore jõu rünnakuga.

## SAMM 3: Kaughaldustarkvara ja tagauksed (Persistence)
Ründaja paigaldab kaughalduse (VNC, AnyDesk, TeamViewer) või tekitab tagaukse (Reverse Shell).

**1. Wazuh filter (Otsi kahtlaseid programme):**
 Kopeeri otsinguribale: `⁠data.process.name: ("vnc" OR "tightvnc" OR "anydesk" OR "nc" OR "netcat" OR "bash")`⁠
 Mida jälgida: Vaata, kas mõni neist käivitati kasutaja prügikastist või ajutisest kaustast (`⁠/tmp⁠ või ⁠AppData\Local\Temp⁠`).

**2. Wireshark filter (Otsi püsivat ühendust / C2):**
 Kirjuta filtriribale: `⁠tcp.port == 4444 || tcp.port == 5555⁠`
 Mida eriliselt jälgida: Kui näed stabiilset ja pidevat andmevahetust (isegi väikeste pakettidega) ohvri ja ründaja vahel nendel kahtlastel portidel, on tegu aktiivse tagauksega.

## SAMM 4: Õiguste kõrgendamine administraatoriks (Privilege Escalation)
Ründaja püüab tavakasutaja alt saada root/admin õiguseid.

**1. Wazuh filter (Otsi admini õiguste haaramist):**
 Kopeeri otsinguribale: `⁠rule.id: (5402 OR 5301 OR 1112 OR 5403) OR rule.description: "Sudo"`⁠
 Mida jälgida: Otsi reeglit ⁠`5402`⁠ (kasutaja lisamine administraatorite gruppi) või Linuxis `⁠sudo`⁠ käske, mis käivitati kahtlasel kellaajal.

## SAMM 5: Jälgede peitmine ja logide kustutamine (Defense Evasion)
Ründaja kustutab logisid, et uurija midagi ei näeks.

**1. Wazuh filter (Otsi logide puhastamist):**
 Kopeeri otsinguribale: `⁠rule.id: (5403 OR 5522 OR 1002 OR 18151)`⁠
 Mida jälgida: `⁠5403`⁠ tähendab "The audit log was cleared". See sündmus registreeritakse enne, kui logi kaob. Võta sealt kohe kasutajanimi ja kellaaeg.

**2. Wireshark filter (Kas pärast seda liigub veel andmeid?):**
 Wiresharki logisid ründaja masinast kustutada ei saa! Kui Wazuh logi katkeb, vaata Wiresharkist, mis liiklust ründaja samal ajal tegi: `⁠frame.time >= "Kellaaeg_mil_logi_kustutati"`⁠.

## SAMM 6: Sisevõrgu ründamine ja ülekoormus (Lateral Movement & DoS)
Ründaja kasutab kaaperdatud arvutit, et ettevõtte teisi servereid skaneerida või umbe joosta (Denial of Service).

**1. Wazuh filter (Otsi ohvri masina muutumist ründajaks):**
 Kopeeri otsinguribale: `⁠data.srcip: "<Sülearvuti_IP>" AND rule.level >= 8`⁠
 Mida jälgida: Vaata, kas töötaja arvuti on järsku hakanud tekitama häireid teiste võrgus olevate serverite suunas.

**2. Wireshark filter (Tuvasta teenuse tõrge / Flooding):**
 Kirjuta filtriribale: `⁠ip.src == <Sülearvuti_IP> && tcp.flags.syn == 1`⁠
 Mida eriliselt jälgida: Vali Wiresharki ülalt menüüst: **Statistics ➡️ Conversations või Statistics ➡️ I/O Graph.** 
 Kui näed graafikul sekundiga sadu tuhandeid pakette, on tegu klassikalise DoS/Flooding rünnakuga, mis jooksuatab serveri kokku.
 
# 💡 Sinu homne kuldne reegel:
1. **Wazuh** pealt võtad filtri abil **kellaaja, sündmuse sisu (Rule ID) ja ründaja IP**.
2. **Wiresharki** peal sisestad selle sama **ründaja IP ja kellaaja**, et võtta raportisse toorete pakettide pilt.
See kahekordne kontroll (Wazuh loogika + Wiresharki toored andmed) teeb su tööst elukutselise analüüsi.
