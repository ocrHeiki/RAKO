# SOC Level 1 töövoog (RAKO) — Täielik samm-sammuline juhend (Excel ilma lisafailideta)

See fail on **iseseisev**: siit saad **kopeeritava demo-andmestiku**, **täpsed Exceli sammud**, **valemid**, **tingimusvormingu reeglid** ja **Palo Alto Threat**-spetsiifilise juhendi. Eraldi CSV faile **ei ole vaja** — piisab, kui kopeerid allolevad andmed Excelisse.

---

## Sisukord
- [Kiirstart: kopeeri demo-andmestik Excelisse](#kiirstart-kopeeri-demo-andmestik-excelisse)
- [Tee tabeliks ja nimeta see Alerts](#tee-tabeliks-ja-nimeta-see-alerts)
- [Rippmenüüd (Data Validation)](#rippmenüüd-data-validation)
- [Valemid: Due_At, Age_h, Repeat_7d, Is_Repeat, RiskScore](#valemid-due_at-age_h-repeat_7d-is_repeat-riskscore)
- [Tingimusvorming (värvikoodid ja SLA)](#tingimusvorming-värvikoodid-ja-sla)
- [Kiirfiltrid, Slicers ja sorteerimine](#kiirfiltrid-slicers-ja-sorteerimine)
- [PivotTable & Timeline: korduvused ja trendid](#pivottable--timeline-korduvused-ja-trendid)
- [Palo Alto Threat logide erijuhend](#palo-alto-threat-logide-erijuhend)
- [Päevane checklist (L1)](#päevane-checklist-l1)
- [Märkus](#märkus)

---

## Kiirstart: kopeeri demo-andmestik Excelisse

1. Ava uus Exceli töövihik.
2. Mine **Sheet1** ja **A1** lahtrisse.
3. **Kopeeri allolev CSV-plokk** (komadega eraldatud) ja **kleebi** A1 lahtrisse. Excel tuvastab veerud automaatselt.

> Kui sinu Excel ei eralda kopeerimisel veerge, kasuta **Data → Text to Columns → Delimited → Comma**.

```csv
Alert_ID,Received_At,Rule,Category,Detection_Source,Asset_Name,Asset_Criticality,Asset_Type,Source_IP,Destination_IP,Username,User_Privileged,Geo,Event_Count,Severity,Status,Owner,SLA_min,Due_At,Age_h,Repeat_7d,Is_Repeat,RiskScore,Action_Taken,Evidence_Link,Notes,MITRE_Tactic,MITRE_Technique,Playbook,Ticket_ID,False_Positive_Reason
ALRT-0001,2025-09-25T09:55:00,Brute-force login attempts on DC,Authentication,Wazuh,DC-01,High,DomainController,203.0.113.5,10.0.0.10,svc_backup,Yes,EE,50,High,New,,30,,,,,,,"Multiple failed logins; new source IP.",Credential Access,T1110,AUTH-Bruteforce,,
ALRT-0002,2025-09-25T09:20:00,Malware detected and quarantined,Malware,Defender for Endpoint,LT-Jane,Medium,Workstation,198.51.100.23,10.0.0.55,jane,No,EE,1,High,New,,60,,,,,,,"Quarantined: Trojan.Win32.Generic",Execution,T1204,MAL-Quarantined,,
ALRT-0003,2025-09-25T07:05:00,Suspicious PowerShell (encoded command),Endpoint,EDR,SRV-FS01,High,FileServer,10.0.0.21,10.0.0.33,system,Yes,EE,3,Critical,Triage,analyst1,30,,,,,,,"Base64 cmdline seen.",Defense Evasion,T1027,EDR-SuspiciousPS,INC-10234,
ALRT-0004,2025-09-25T04:00:00,Port scan detected,Network,IDS,SRV-WEB01,Medium,WebServer,192.0.2.88,10.0.0.80,,No,DE,200,Low,New,,240,,,,,,,"Likely internet scan; monitor.",Discovery,T1046,NET-Scan,,
ALRT-0005,2025-09-24T09:15:00,Multiple 2FA failures,Identity,Azure AD,LT-Mark,Low,Workstation,203.0.113.77,10.0.0.15,mark,No,US,6,Medium,New,,180,,,,,,,"Unusual geo.",Credential Access,T1110,ID-2FA-Fail,,
ALRT-0006,2025-09-25T09:45:00,Blocked outbound to known C2,Network,Firewall,LT-Jane,Medium,Workstation,10.0.0.55,198.51.100.200,jane,No,EE,4,High,New,,60,,,,,,,"Matches threat intel list.",Command and Control,T1071,NET-C2-Blocked,,
ALRT-0007,2025-09-25T02:00:00,Suspicious file renamed to .exe,Endpoint,EDR,LT-Kai,Low,Workstation,10.0.0.60,10.0.0.60,kai,No,EE,1,Medium,New,,180,,,,,,,"User downloaded from unknown site.",Execution,T1204,EDR-FileRename,,
ALRT-0008,2025-09-23T12:00:00,Privileged group membership change,Identity,AD Audit,DC-01,High,DomainController,10.0.0.10,10.0.0.10,admin,Yes,EE,1,High,In Progress,analyst2,60,,,,,,,"Change window ticket CAB-555",Privilege Escalation,T1068,ID-GroupChange,INC-10240,
ALRT-0009,2025-09-25T08:30:00,Data exfiltration pattern (large upload),Data,DLP,LT-Jane,Medium,Workstation,10.0.0.55,203.0.113.200,jane,No,EE,2,High,New,,60,,,,,,,"Upload >1GB to unsanctioned site.",Exfiltration,T1041,DLP-Exfil,,
ALRT-0010,2025-09-22T10:10:00,Repeated failed sudo attempts,Authentication,Syslog,SRV-DB02,High,DatabaseServer,10.0.0.70,10.0.0.70,devops,Yes,EE,12,Medium,Closed,analyst1,120,,,,,,,"User confirmed fat-finger; reset",Privilege Escalation,T1068,AUTH-SudoFail,INC-10200,User error
```

> **Vihje:** Vorminda veerg **Received_At** kuupäev/kellaaeg vormingusse `yyyy-mm-dd hh:mm` (Custom), kui Excel ei kuva automaatselt.

---

## Tee tabeliks ja nimeta see `Alerts`

1. Klõpsa andmetes ükskõik kuhu → **Ctrl+T** (Mac: **⌘+T**).  
2. Märgi “**My table has headers**”.  
3. Table Design (Macis: Table) → **Table Name** = `Alerts`.  
4. Tee veerud **AutoFit** (double-click veerupiiril).  
5. View → **Freeze Top Row**, et päis püsiks nähtav.

---

## Rippmenüüd (Data Validation)

**Home → Data → Data Validation → Allow: List → Source:**

- Veerg **Severity** → `Low,Medium,High,Critical`
- Veerg **Status** → `New,Triage,In Progress,Escalated,Resolved,Closed,False Positive`
- Veerg **Asset_Criticality** → `Low,Medium,High`
- (Soovi korral) **User_Privileged** → `Yes,No`

> Vihje: tee need rippmenüüd **kogu veerule** (valik ülevalt alla), et uued read päriksid valikud.

---

## Valemid: `Due_At`, `Age_h`, `Repeat_7d`, `Is_Repeat`, `RiskScore`

**Pane kursor vastavasse veergu sellesama tabeli reas** ja kleebi valem. Excel täidab ülejäänud read automaatselt.

**1) Tähtaeg (Due_At)** — minutid päevadesse (1440 min = 1 päev):
```excel
=[@[Received_At]] + ([@[SLA_min]]/1440)
```

**2) Vanus tundides (Age_h)** — jooksev aeg vs vastuvõtu aeg:
```excel
=(NOW()-[@[Received_At]])*24
```

**3) Kordused 7 päeva sees (Repeat_7d)** — sama Rule + sama Asset:
```excel
=COUNTIFS(Alerts[Rule],[@Rule],
          Alerts[Asset_Name],[@Asset_Name],
          Alerts[Received_At],">=" & ([@[Received_At]]-7))
```

**4) Kas on korduv? (Is_Repeat)** — märgista kui ≥3:
```excel
=IF([@[Repeat_7d]]>=3,"YES","")
```

**5) Riskiskoor (RiskScore)** — lihtne, kuid tõhus:  
- Severity: Low=1, Medium=2, High=3, Critical=4  
- Asset_Criticality: Low=1, Medium=2, High=3  
- +2 kui korduv (`Is_Repeat="YES"`), +2 kui privileegikasutaja (`User_Privileged="Yes"`)

**Variandi A (SWITCH olemas):**
```excel
=(SWITCH([@Severity],"Low",1,"Medium",2,"High",3,"Critical",4,0)
  * SWITCH([@[Asset_Criticality]],"Low",1,"Medium",2,"High",3,0))
 + IF([@[Is_Repeat]]="YES",2,0)
 + IF([@[User_Privileged]]="Yes",2,0)
```

**Variandi B (kui SWITCH puudub):**
```excel
=(IF([@Severity]="Low",1,IF([@Severity]="Medium",2,IF([@Severity]="High",3,IF([@Severity]="Critical",4,0))))
  * IF([@[Asset_Criticality]]="Low",1,IF([@[Asset_Criticality]]="Medium",2,IF([@[Asset_Criticality]]="High",3,0))))
 + IF([@[Is_Repeat]]="YES",2,0)
 + IF([@[User_Privileged]]="Yes",2,0)
```

---

## Tingimusvorming (värvikoodid ja SLA)

**Home → Conditional Formatting → New Rule**

### Severity värvid (vali kogu veerg `Severity`):
- **Critical** → *Format only cells that contain* → *Specific Text* → **containing** `Critical` → Fill: **punane**, Font: valge.  
- **High** → sama, kuid **oranž** taust.  
- **Medium** → **kollane**.  
- **Low** → **roheline**.

> Alternatiiv: “Use a formula to determine which cells to format”, nt: `=$Severity="Critical"`

### SLA ületatud (kogu rida või veerg `Age_h`):
- Reegel (Use a formula):  
  ```excel
  =AND($Status<>"Resolved",$Status<>"Closed",NOW()>$Due_At)
  ```
  Värvi **helepunase** taustaga.

### Privilegeeritud kasutaja (rida esile):
```excel
=$User_Privileged="Yes"
```
Võid lisada **paksu ääre** või helepunase serva.

### Palo Alto “Allowed + High/Critical” (kui kasutad Palo Alto CSV-d või lisaveerge):
```excel
=AND($Severity<>"Low",$Severity<>"Medium",$Action="Allowed")
```
Tee **tumeoranž taust** – need väärivad kohest tähelepanu.

---

## Kiirfiltrid, Slicers ja sorteerimine

- **Sorteeri**: `Age_h` kahanevalt → vanimad enne (SLA piir käes).  
- **Slicerid** (Table Design → Insert Slicer): vali `Severity`, `Status`, `Asset_Criticality` (ja vajadusel `User_Privileged`).  
- **Filter**: aktiivsed juhtumid → `Status ∉ {Resolved, Closed, False Positive}`.  
- **Filtreeri korduvad**: `Is_Repeat = YES`.

---

## PivotTable & Timeline: korduvused ja trendid

1. Vali mis tahes lahter tabelis `Alerts`.  
2. Insert → **PivotTable** (New Worksheet).  
3. Näited:
   - **Rule × Count** (viimased 7 päeva): Rows=`Rule`; Values=`Count of Alert_ID`; Filter `Received_At` viimased 7 päeva.  
   - **Asset × Severity**: Rows=`Asset_Name`; Columns=`Severity`; Values=`Count of Alert_ID`.  
   - **Username korduvus**: Rows=`Username`; Values=`Count of Alert_ID`; Slicer=`Category`.  
4. **Timeline**: Insert → Timeline → väli `Received_At` → lohista filtrit (päev/kuu).

> Soovi korral lisa Pivot Chart (Clustered Column) kiireks visualiks.

---

## Palo Alto Threat logide erijuhend

Kui töötled Palo Alto (PA) ohte, lisa **lisaveerud** (või kasuta eraldi Palo Alto tabeleid):  
- **Threat_Name**, **Threat_ID**, **Action** (`Allowed/Blocked/Reset-Client`), **URL_Domain**, **App**, **Source_Zone**, **Destination_Zone**.

**Filtreerimisstrateegia:**
- `Severity ∈ {High,Critical}` **ja** `Action="Allowed"` → esmased.  
- **Korduvad Threat_ID** väärtused (Repeat_7d ≥ 3) → kontrolli lähemalt.  
- **C2/Exfiltration/Malware** kategooriad → kõrgem prioriteet.  
- **Privileegikasutaja** seotud? Kui jah, tõsta prioriteeti.

**Tingimusvorming** (PA jaoks):  
```excel
=AND($Severity<>"Low",$Severity<>"Medium",$Action="Allowed")
```
→ **tumeoranž taust**

---

## Päevane checklist (L1)

- Ava `New/Triage` alertid.  
- Slicer: **Severity=High/Critical**, **Asset_Criticality=High**.  
- Sorteeri `Age_h` kahanevalt → töötle **SLA kriitilised** enne.  
- Vaata **korduvaid** (`Is_Repeat=YES`).  
- Palo Alto: **Action=Allowed** juhtumid esimesena.  
- Lisa `Action_Taken`, `Notes`, `Evidence_Link`, uuenda `Status`.  
- Eskaleeri, kui `RiskScore ≥ 8` või `Severity=Critical`.  
- Tee Pivot-raport (24h kokkuvõte).  
- Sulge resolved/false positive read põhjendusega.

---

## Märkus

📌 *Materjalid koostatud ja jagatud GitHubi kasutaja [ocrHeiki](https://github.com/ocrHeiki) õpiprojekti tarbeks.*
