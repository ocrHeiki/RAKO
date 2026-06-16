🕵️‍♂️ KROONIKA: Ründeahela ülevaade (Cyber Kill Chain)
1. ETAPP: Luure ja Skaneerimine (Reconnaissance & Weaponization)
KUS: Sihtmärgiks oli Ubuntu arendusserver (192.168.1.105).

KES: Ründaja IP-aadressilt 192.168.1.110.

MIDA: Ründaja alustas agressiivse pordi- ja teenusteskaneerimisega (TCP SYN Scan). Ta saatis tuhandeid pakette, et testida, mis uksed on serveris lahti.

MIKS: Et leida nõrku kohti ja teenuseid, mida rünnata. Skaneerimise tulemusena avastas ta, et serveris on avatud port 22 (SSH), port 80 (HTTP) ja port 3306 (MySQL andmebaas).

2. ETAPP: Lekkinud info kuritarvitamine (Delivery / Exploitation)
KUS: GitHubi avalik repositoorium ja Ubuntu serveri veebikeskkond (port 80).

KES: Ründaja (192.168.1.110) ja inimliku eksimuse teinud praktikant/arendaja.

MIDA: Praktikant pani üles uue dev-keskkonna, kuid jättis selle kogemata välisvõrgule avatuks ning komiteeris (laadis üles) andmebaasi paroolid ja ligipääsud avalikku GitHubi. Ründaja kuulas skaneerimistarkvaraga (dirb/gobuster) veebiserverit üle, otsides konfiguratsioonifaile, ning kasutas GitHubist leitud reaalseid andmebaasi ja süsteemi paroole.

MIKS: Ründajad monitoorivad pidevalt avalikke koode (nt GitHubi) lekitatud paroolide leidmiseks. Kui arendaja eksimus langes kokku ründaja skaneerimisega, sai ründaja ilma süsteemi "lõhkumata" ehk legitiimsete paroolidega otse uksest sisse jalutada.

3. ETAPP: Süsteemi sissetung ja kompromiteerimine (Installation)
KUS: Ubuntu arendusserveri veebiliides ja andmebaas.

KES: Ründaja (192.168.1.110).

MIDA: Pcap-faili lõpus on näha edukad veebipäringud ja serveri vastused HTTP/1.1 200 OK. See märgib hetke, kus ründaja sai veebikeskkonnale või andmebaasi haldusliidesele (nt phpMyAdmin) täieliku autoriseerimata ligipääsu. Ta logis sisse lekitatud paroolidega.

MIKS: Et saavutada kindel kanda sisevõrgus, hakata andmeid varastama ja valmistada ette pinnas edasiseks liikumiseks (näiteks Active Directory domeenikontrolleri ITSK_DC_2022 suunas).

4. ETAPP: Eesmärkide täitmine – Andmete leke (Actions on Objectives)
KUS: Ubuntu arenduskeskkond (192.168.1.105).

KES: Ründaja (192.168.1.110).

MIDA: Toimus andmete väljavõte (Data Exfiltration). Kuna ründaja pääses otse ligi MySQL andmebaasile (port 3306), laadis ta sealt alla konfidentsiaalsed andmed (kliendiandmed, siseinfo vms), mida server talle edukalt läbi võrgu edastas. Sellest tuleneb ka arendaja paanika piletis: "Kas me oleme lekkinud nüüd?" – Jah, olete küll.

MIKS: Ründe lõppeesmärk oli tundliku info kättesaamine, et seda kuritarvitada, müüa või ettevõtet šantažeerida.

💡 Kokkuvõte eksamikomisjonile (Lühike spikker):
Kes ründas? Seade IP-ga 192.168.1.110.

Kuhu rünnati? Ubuntu arendusserverisse 192.168.1.105.

Kuidas sisse saadi? Skaneeriti porte -> leiti avatud veeb ja andmebaas -> arendaja lekitas GitHubi paroolid -> ründaja kasutas neid paroole süsteemi sisselogimiseks ilma turvavigu vajamata.

Mis oli tulemus? Täielik andmebaasi ja dev-keskkonna kompromiteerimine ning info lekkimine ründajale (HTTP 200 OK).

Selle kronoloogia põhjal saad sa kirjutada piletitesse ülitugeva ja professionaalse analüüsi!
