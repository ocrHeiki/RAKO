# Küberturve peaks olema kihiline nagu Napoleoni kook.
**11.veebruar.2026**

```
Kui esimene kiht ei suuda ründaja teed sulgeda ja petukirja saaja vajutab selles oleval lingil,
siis tuleb appi teine ehk taustal töötav tarkvara, mis blokeerib ühenduse õngitsuslehega enne,
kui kasutaja jõuab sinna oma andmed sisestada 

Kihilist kaitset ja varulahenduste-rohkeid teenuseid!

"RIA - Küberturvalisuse Aastaraamat 2026"
```
## Arvestades kevadist eksamid

E-ITS tuleb hakata ikkagi korralikult läbi lugema, sest mõnes kohas kasutatakse seda igapäevase töövahendina ja eksamile tuleb ka meil sellest juttu...
Vaata ära mis on teada tuntud tõed/probleemid
https://eits.ria.ee/et/versioon/2024/eits-poohidokumendid/etalonturbe-kataloog/ops-kaeidutoeoed/ops1-oma-kaeidutoeoed/ops11-itpoohitoeoed/ops115-logimine/3-meetmed
EITS ülesande juures tuleb ära märkida mis on valesti ja andma soovituse, kuidas/mida seda teha.

Eraldi on märgitud mingi ülesanne, kui on vaja midagi korda teha.

SYS.IT süsteemid: Servr,Linux, Windows, 
App.Rakendused: võrguteenused


## Harjutus vmWares dc01-pentest
dc01-pentest masin pw: `stars4191*`

### Esimesed kontrollid
Local Server:
- Remote management ja Remont Desktop, miks nad on Enabled
- Last installed updates, miks Never
- Defender Antivirus, miks Off
- Timezone

Tools 
- Computer Management:
 - Task Scheduler Libraries - Vahel võib näidata kui lülitada `Display All Running Tasks` ja siis vaadata, mis karjuma hakkab
 - Event Viewer     NXLog - on hea agent, mis aitab logisid kokku koguda
Logide kokku kogumise koht ei tohiks olla kunagi Domeeniserver
 - Shared Folders - Shares , siin tulevad välja ka peidetud failid, mis on kuhugi jagatud
  - Storage
    - Windows Server Backup, kas saame teha backupi
    - Disk Management
Tools - Group Policy Management:
- Policies-Windows Settings-Security Settings
  - Account Policy-Password Policy - parem klõps-Edit
  - Security Options:
    - Network security:Restrict NTLM: Audit Incoming NTLM Traffic - Enable all (siis annab märku kui Kuldpääsu ründed toimuvad... vm sellist)
    - Network security:Restrict NTLM: Incoming NTLM traffic - Deny All
    - Network security:Restrict NTLM: NTLM authentication in this domain - Deny All
      - Seejärel PS: `gpupdate /force` suruda jõuga õigused peale.. restart ei aita
    - Network security:Force logoff when logon hours expire

