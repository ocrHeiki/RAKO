# ⚙️ ülesanne 2: Küberintsidendi analüüsiaruanne
- **Autor:** Heiki Rebane `ocrHeiki`
- **Aeg:** 08.05.2026
- **Team51**
---
## 💻 masinad
- itsk-dc01-team51
- itsk-dev-team51
- itsk-router-team51
- itsk-soc-team51

- ITSK25-HeikiRebane-Kali
---
soc masina ip 192.168.30
**KALI**
brauseris avasin http://192.168.1.30 
- kasutaja `admin`
- parool `SecretPassword`

**dev**
Pa55w.rd
- kasutaja `audit`
- parool `Pa55w.rd`
## Uurimine
10:37:46 - Windows command prompt started by an abnormal process. Rule ID 92052 File: 0800-sysmon_id_1.xml
Rünnaku sisuks oli Wazuh kinni panna


Avasin PowerShelli ja uurisin mis kasutajatel on "Administrators" õigused.
`Get-LocalGroupMember -Group "Administrators"`

- Group   AUACHOO\Domain Admins     -   ActiveDirectory
- User    AUACHOO\j.black           -   ActiveDirectory
- User    dev-station\Administrator -   Local
- User    dev-station\john          -   Local

## 1. Tuvastatud rünnak ja selle sisu:
Wazuh andis märku kahtlasest tegevusest domeenikontrolleri (dc01) vastu. Logide analüüs paljastas kriitilise Kerberose vea (Event ID 7). Süsteem teatas, et Security Account Manager ebaõnnestus KDC (Key Distribution Center) päringu töötlemisel ootamatul viisil. See viitab katsele kuritarvitada domeeni autentimismehhanisme (nt Golden Ticket või Pass-the-Ticket rünnak).

## 2. Rünnaku kellaaeg:
Peamine intsident domeenikontrolleris toimus täpselt kell 03:11:25 (UTC aja järgi logides).

## 3. Kasutaja, kes "tegi midagi":
Kuigi KDC viga viitab süsteemitaseme rünnakule, tuvastati hilisema luuretegevuse käigus (kell 10:37) kahtlane PowerShelli kasutus kasutaja audit alt. Samuti on süsteemis märgatud domeenikasutajat AUACHOO\j.black, kelle õigusi administraatorite grupis rünnaku käigus kontrolliti/kasutati.

## 4. Täiendavad leidud:

Masin client on haavatav mitmele kriitilisele turvaaugule (nt CVE-2025-22230), mis võis olla ründaja esmane sisenemispunkt.

Kell 10:37 toimus kliendi masinas käskude loetlemine (Get-LocalGroupMember), mis viitab ründaja soovile laiendada oma õigusi domeenis.
