# Palo Alto Threatide Analüüs: Valepositiivide Kindlaks Tegemise Juhend

See juhend aitab sul läbi viia madala severity tasemega threatide analüüsi Palo Alto süsteemis – eriti seoses võimalike valepositiivide (väärade hoiatustega) tuvastamisega.

## 1. Eesmärk
Määrata kindlaks, kas 24h jooksul tekitatud palju madal-severity tasemega threat-e, mis ei pruugi olla reaalsed ohud – st valepositiivid. Selleks kasutatakse logide CSV-faili, mille alla laadisid Palo Alto süsteemist.

## 2. Ettevalmistused
- Ava alla laetud CSV-fail tabeliprogrammis (nt Excel, Google Sheets, LibreOffice Calc).
- Veendu, et andmed oleks õigesti imporditud (eraldajaks komad või semikoolonid).

## 3. Vajalikud veerud logis
Enne analüüsi pead valima järgmised veerud nähtavaks:
- **Threat Name** – threat-i nimi või ID
- **Severity** – tõsiduse tase (1–5, kus 1 on madalaim)
- **Occurrences/Count** – sagedus (mitu korda threat esines 24h jooksul)
- **Source IP / Destination IP** – liikluse lähte- ja sihtpunkt
- **Category / Subcategory** – millise kategooria alla see kuulub
- **Action Taken** – kas blokeeriti või lubati

## 4. Samm-sammuline juhis

### 4.1 Filtreeri madala severity tasemega kirjed
- Filtriks vali: `Severity = 1 või 2`.
- Sorteeri kirjed nt korduste arvu järgi (kõige enamat esinevad esimesena).

### 4.2 Vaata kõige sagedasemaid threat-e
- Milline "Threat Name" esineb enim?
- Kas see on tuntud veebi-/rakenduste skaneerimise või moonutuste tüüp?

### 4.3 Uuri threat-i lähemalt
- Otsi threat ID või name veebist Palo Alto Knowledge Base'ist:
  - [Palo Alto Knowledgebase](https://knowledgebase.paloaltonetworks.com/)
- Leia info:
  - Mis tüüpi threat see on?
  - Kuidas see käitub?
  - Milline severity tase on algselt määratud ja miks?

### 4.4 Võrdle võrgukontekstiga
- Vaata threati seost teiste andmetega:
  - Kas threat tulnud koduvõrgust või välisest IP-st?
  - Kas liiklus toimub tavaliselt kasutatud protokollide (nt HTTP, DNS, SSH) vahel?
  - Kas liiklus kuulub tavapäraseks võrguliikluseks loetavasse maatriksisse?

### 4.5 Kontrolli seost reeglitega
- Ava oma Palo Alto konfiguratsioon või konsulteeri õppejõuga, kuidas rule-setid on seadistatud.
- Vaata, kas "Threat Name" on seotud reegliga:
  - Kas see on liiga üldine (nt `any-any`)?
  - Kas sellel on aktiveeritud kaitseprofiil (IPS/antivirus)?
  - Kas threat peaks üldse toimuma?

### 4.6 Hinda tõenäosust valepositiivi kohta
- Kontrolli:
  - Kas threat on seotud legitiivse liiklusega (nt saidipäring või CDN)?
  - Kas threat-i sagedus on absurdne (nt tuhandekordne esinemine väga lühikese aja jooksul)?
  - Kas threat-i käitumine kattub teadaolevate moonutustega (nt legitiimsed skriptid mis näevad välja kahtlasena)?

## 5. Kokkuvõtte teemade aruandesse
Lisa vastused järgmistele küsimustele oma aruandesse:

1. **Mis severity tasemeid esines enim?**
2. **Milline threat-I ID esines enim madalate severity-dega ja miks?**
3. **Mis teavet said threat-i kohta teada?**
4. **Kas selle threat-i esinemine võib olla tingitud valesti konfigureeritud reeglist või mitteohulikust liiklusest?**
5. **Millise protsessi kaudu jõudsid järelduseni, et threat ei ole reaalne oht?**

## 6. Lisaresursid
- [Palo Alto Threat Encyclopedia](https://knowledgebase.paloaltonetworks.com/)
- Google Scholar / Internet – otsi "Palo Alto [Threat ID]"

## 7. Mida veel uurida?
- Võrdle threat-i esinemist eri IP-aadresside vahel.
- Uuri, kas threat-id muutuvad aja jooksul – kas tegu on püsiva müraga või reaalse ohtliku aktiivsusega.
- Arutle võimaluste üle threat-i monitoorimiseks ja/või vältimiseks (nt reegli täpsustamine).
