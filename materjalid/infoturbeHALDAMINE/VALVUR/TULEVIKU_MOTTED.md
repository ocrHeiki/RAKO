###############################################################################
#                                                                             #
#   █████   █████           ████                                              #
#  ▒▒███   ▒▒███           ▒▒███                                              #
#   ▒███    ▒███   ██████   ▒███  █████ █████ █████ ████ ████████             #
#   ▒███    ▒███  ▒▒▒▒▒███  ▒███ ▒▒███ ▒▒███ ▒▒███ ▒███ ▒▒███▒▒███            #
#   ▒▒███   ███    ███████  ▒▒███  ▒███  ▒███  ▒███ ▒███  ▒███ ▒▒▒            #
#    ▒▒▒█████▒    ███▒▒███  ▒███  ▒▒███ ███   ▒███ ▒███  ▒███                 #
#      ▒▒███     ▒▒████████ █████  ▒▒█████    ▒▒████████ █████                #
#       ▒▒▒       ▒▒▒▒▒▒▒▒ ▒▒▒▒▒    ▒▒▒▒▒      ▒▒▒▒▒▒▒▒ ▒▒▒▒▒                 #
#                                                                             #
#   =======================================================================   #
#   |                                                                     |   #
#   |   PROJEKT:     VALVUR - Intsidendi süvaanalüüs                      |   #
#   |   FAILI NIMI:  TULEVIKU_MOTTED.md                                   |   #
#   |   LOODUD:      2026-05-15                                           |   #
#   |   AUTOR:       Heiki Rebane                                         |   #
#   |   KIRJELDUS:   VALVUR-i strateegiline arendusplaan (50 punkti).     |   #
#   |                                                                     |   #
#   =======================================================================   #
#                                                                             #
###############################################################################

# VALVUR - Strateegiline arendusplaan (Roadmap)

See dokument sätestab VALVUR-i (HeRe) pikaajalise visiooni ja arendusetapid pärast prototüübi edukat kaitsmist.

## I. Arhitektuur ja Skaleeritavus
- **Go/Rust moodulid**: Kriitiliste komponentide (hashing, scanning) ümberkirjutamine maksimaalse jõudluse saavutamiseks.
- **Agent-põhine kogumine**: Kergekaalulised agendid reaalajas logide kogumiseks sadadest masinatest.
- **Dockeriseeritud analüüs**: Analüüsimootorite isoleerimine konteineritesse, vältimaks süsteemseid konflikte.
- **PostgreSQL/Elasticsearch**: Üleminek CSV-põhiselt salvestuselt relatsioonilisele ja otsingumootoripõhisele andmehaldusele.
- **Resource Throttling**: Nutikas koormuse piiramine, et analüüs ei häiriks süsteemi põhitööd.

## II. Süvaforensika ja Andmehõive
- **Mälufailide süvaanalüüs**: Täielik integratsioon Volatility 3-ga (fileless malware tuvastus).
- **Artifact Parserid**: Brauseri ajaloo (Chrome/Edge), USB-seadmete registriajaloo ja LNK-failide automaatne analüüs.
- **VSS (Volume Shadow Copy) uurimine**: Vanemate ründejälgede leidmine varukoopiatest.
- **Kustutatud failide taastamine**: Failide "carving" ja MFT (Master File Table) skaneerimine.
- **Network Packet Capture**: Kahtlase tegevuse korral automaatne PCAP salvestamise alustamine.

## III. SIEM ja Visualiseerimine
- **Kibana/Grafana Dashboardid**: Interaktiivsed vaated ründe kulgemise (Lateral Movement) jälgimiseks.
- **Interaktiivne Timeline**: Graafiline ajajoon, mis koondab sündmused sekundilise täpsusega üle erinevate platvormide.
- **Võrgu topoloogia graaf**: Visuaalne esitus masinatevahelistest seostest ja ründe levikust.
- **Risk Scoring**: Masina koondhinde arvutamine leitud haavatavuste ja ründejälgede põhjal.
- **GeoIP Mapping**: Kahtlaste välisühenduste kuvamine reaalajas maailmakaardil.

## IV. Nutikas Tuvastus ja AI
- **YARA & Sigma reeglid**: Tööstusstandardite rakendamine failisüsteemi ja logide skaneerimisel.
- **Masinõpe (ML)**: Ebaharilike mustrite tuvastamine ilma eelnevalt defineeritud reegliteta (Anomaly Detection).
- **NLP Raporteerija**: AI-põhine kokkuvõtete genereerimine, mis tõlgib tehnilised leiud inimkeelde.
- **Automated Response (SOAR)**: Võimekus nakatunud masin automaatselt võrgust isoleerida.
- **Active Directory süvaaudit**: Golden Ticket ja teiste domeenispetsiifiliste rünnete tuvastamine.

## V. Kasutajamugavus ja Vastavus
- **Veebipõhine GUI**: Mugav liides uurijatele juhtumite (Case Management) haldamiseks.
- **E-ITS/ISO Roadmap**: Automaatne samm-sammuline kava leidude kõrvaldamiseks ja nõuetele vastavuse saavutamiseks.
- **Mobiilne teavitusäpp**: Kriitilised häired ja raportite kokkuvõtted otse turvaspetsialisti telefoni.
- **Võrdlev analüüs (A vs B)**: Võimalus võrrelda süsteemi olekut erinevatel ajahetkedel.
- **Mitmekeelsus**: Raportite genereerimine eesti, inglise ja saksa keeles.

---
*VALVUR: Vägi ilma tarkuseta on pime, tarkus ilma väeta on võimetu.*
