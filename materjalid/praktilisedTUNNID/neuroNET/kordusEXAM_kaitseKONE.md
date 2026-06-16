# Slaid 1: Tiitelslaid (Sissejuhatus)

Mida rääkida: 

**"Tere! Tutvustan teile 16. juunil 2026 tuvastatud kriitilise võrguintsidendi uurimistulemusi. Tegu on reaalse ründeahelaga, mis algas välisest õngitsusest ja päädis meie sisevõrgu mailiserveri ülevõtmisega. Vaatame otsestele tõenditele tuginedes otsa sellele, mis juhtus, kuidas ründaja sisse sai ja mis on hetkeseis."**

# Slaid 2: Vaheslaid – Võrgu Infrastruktuuri Kaart

Mida rääkida: 

**"Enne detailide juurde asumist vaatame üle meie võrgu topoloogia. Meie sisevõrk koosneb pfSense tulemüürist, Windowsi domeenikontrollerist, Exchange'i mailiserverist ja Nextcloudi pilveserverist. Seda kõike jälgib taustal Wazuh SIEM turvaseire. Kahjuks leidsime sellest kaardist kriitilised nõrkused, mis tegid ründajale uksed lahti."**

# Slaid 3: Sisevõrgu Sõlmed ja Teenused (Tehniline vaade)

Mida rääkida: 

**"Võrgu auditeerimisel tuvastasime esimese suure ohukoha: Nextcloud pilveserver (.20) töötas üle krüpteerimata HTTP pordi 80. See tähendab, et kogu sealne andmevahetus liikus sisevõrgus puhta tekstina."**

**"Teine ja kõige valusam punkt on Mailiserver (.13). Ründaja sihtmärgiks sai just see server, kus ta suutis kompromiteerida kasutaja nimega peeter."**

**"Meie õnn oli see, et Wazuh SIEM (.42) ja võrgumonitooring salvestasid kogu tegevuse, mis võimaldas meil selle intsidendi tagantjärele täielikult dekonstrueerida."**

# Slaid 4: Punane Tsoon: Ründaja Jalajälg (Tõendid)

Mida rääkida: 

**"Nüüd aga kõige olulisem – ründaja konkreetsed IP-aadressid ja tõendid, mis me piletitest ja logidest leidsime:"**

 - Sisevõrgus (192.168.1.110): "Hommikul märgati võrgus võõrast Kali Linuxi masinat. Wiresharki püügifail (networkscan.pcapng) tõestab, et see seade kuulas pealt Nextcloudi liiklust ja tegi võrgus massiivset luuret."

 - Väline õngitsusserver (10.0.24.209): "Tuvastasime, et kasutaja Peeter suunati võltsitud Microsofti sisselogimislehele, kus temalt kalastati välja konto paroolid."

 - Väline juhtserver (C2 - 10.0.21.137): "See on intsidendi kõige kriitilisem pööre. Wazuh SIEM logid näitavad, et meie Mailiserverist loodi edukas root-õigustes SSH-ühendus otse ründaja välise aadressiga. See tähendab, et ründajal oli serverile käsurea kaudu täielik ligipääs andmete väljaviimiseks."

# Slaid 5: Mõju ja Ulatus (Mis juhtus süsteemide sees?)

Mida rääkida: 

**"Kuidas ründaja end sisse seadis? Me vaatasime Active Directory ja Computer Managementi logisid ja pilt on järgmine:"**

**"Kõigepealt kasutas ründaja pfSense tulemüüri avatud NAT / Port Forwarding reegleid – RDP ja SSH pordid olid internetti avatud, mis lubas tal kodust lahkumata sisse logida."**

**"Seejärel tõstis ta serveris õigusi. Kasutajale peeter anti Administrator ja Remote Desktop Users õigused."**

**"Et oma ligipääsu kindlustada, lisas ründaja Peetri konto ka OpenSSH Users gruppi. See on klassikaline püsivuse (Persistence) loomine – isegi kui me RDP ühenduse sulgeme, saab ta SSH pordi kaudu ikka sisse."**

# Slaid 6: Ründe Kronoloogia (Timeline)

Mida rääkida: 

**"Rünnak arenes kiiresti ja loogiliselt:"**

 - Kell 01:50 algas sisevõrgu automatiseeritud skaneerimine võõra Kali masina poolt.

 - Kell 01:59 tabas ründaja Wiresharki andmetel ära Nextcloudi krüpteerimata liikluse (HTTP port 80).

 - Kell 02:22 toimus paroolide kuritarvitamine – AD-s kaaperdati ja eskaleeriti konto "peeter".

 - Kell 02:40 fikseeris Wazuh turvaseire andmete väljaviimise kanali (C2) käivitamise välisele IP-le üle SSH.

# Slaid 7: Lõppsõna & Küsimused (Tegevusplaan)

Mida rääkida: 

**"Kokkuvõtteks – rünnak oli edukas, sest meil olid pordid internetti avatud ja sisevõrgu liiklus krüpteerimata. 
Kohesed sammud, mis me juba ette oleme võtnud ja peame lõpule viima:"**

 - Tulemüüris üleliigsete NAT/Port Forwarding reeglite sulgemine.

 - Kasutaja "peeter" konto parooli sundvahetus ja õiguste korrigeerimine AD-s.

 - Nextcloudi kohustuslik üleviimine HTTPS (port 443) peale.

**"Aitäh! Kas teil on raporti või ründeahela kohta küsimusi?"**

# 💡 Nõuanne esinejale:

Kui juhtkond küsib: 

**"Kas andmed läksid kaduma?"**, siis Sinu vastus on: **"Jah, tõenäosus on väga suur. Kuna Wazuh logis eduka SSH-ühenduse välise juhtserveriga 10.0.21.137 ja Nextcloud oli krüpteerimata, oli ründajal tehniliselt olemas kõik vajalik failide ja e-kirjade allalaadimiseks. Seetõttu peamegi reageerima kohe."**
