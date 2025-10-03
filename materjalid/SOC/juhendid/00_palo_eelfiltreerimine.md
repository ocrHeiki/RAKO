# Etapp 0 — Palo Alto logide eelfiltreerimine (Monitor → Logs)

Eesmärk: võtta **õige 24h väljavõte**, kus on just need väljad ja vood, mida hiljem Excelis/Pandases analüüsime.  
Alltoodud juhend on mõeldud *Traffic* logi jaoks (sama loogika kehtib suuresti ka *Threat/URL* logidele).

---

## 1) Ajavahemik ja ajavöönd
- **Time range:** *Last 24 hours* (või käsitsi täpne 24h aken)  
- **Time zone:** vali ettevõtte TZ (nt *Europe/Tallinn*) → vältid segadust hiljem graafikutega  

---

## 2) Logi tüüp
- Mine: **Monitor → Logs → Traffic**  
- (soovi korral lisa hiljem eraldi väljavõte ka **Threat** logidest: Monitor → Logs → Threat)  

---

## 3) Väljad (Columns) – vali ja järjestus
Vali *Columns* nupu alt **vähemalt**:
- **Time Received** / **Start Time**, **End Time**  
- **Source address**, **Destination address**  
- **NAT Source IP**, **NAT Destination IP** (kui NAT oluline)  
- **Application**, **Rule**  
- **Action** (allow/deny/drop/reset-both)  
- **Bytes**, **Bytes Sent**, **Bytes Received** (kui vaja)  
- **Session End Reason**  
- **Risk of app** (1–5)  
- **Severity** (low/medium/high/critical) – kui olemas  
- **Source user** (kui kasutajapõhine korrelatsioon vajalik)  
- **Destination zone**, **Source zone** (soovi korral)  
- **Device name** (kui väljavõte on mitmest fw-st)  

> Mida rohkem kasulikke veerge pikemas plaanis vajad, seda parem on need kohe CSV-sse panna – hiljem on lihtsam filtreerida.  

---

## 4) Filtrid (Traffic logi filter bar)

### 4.1 Üldfilter 24h triage jaoks
```
((start-time geq 'last-24-hrs') and ((risk-of-app geq 3) or (app eq 'http-proxy') or (app eq 'ssl') or (app eq 'dns-base') or (app contains 'ms-ds-smb')))
```
Selgitus:  
- toome **Risk ≥ 3** ja **neli fookus-app’i**: `http-proxy`, `ssl`, `dns-base`, `ms-ds-smb`  

### 4.2 Ainult lubatud ühendused (prioriteetsem uurida)
```
(((risk-of-app geq 4) or (app eq 'http-proxy')) and (action eq allow))
```
- kõrge risk (4–5) **ja** *allow* → suurem intsidirisk  

### 4.3 DNS mahu-anomaaliad (eraldamiseks)
```
((app eq 'dns-base') and (action eq allow))
```

### 4.4 SSL tundmatud sihid (toorfilter Palo Altos)
```
(app eq 'ssl')
```
> Palo Alto enda filtris ei saa lihtsalt “not in whitelist prefix” teha. Tee üldfilter, ekspordi CSV ja puhasta hiljem Excelis/Pandases.  

### 4.5 SMB lateraalliikumine (LAN↔LAN)
```
((app contains 'ms-ds-smb') and (srczone eq 'Trust') and (dstzone eq 'Trust'))
```
- või lisa IP/prefix tingimused, kui need on teada  

---

## 5) Mida **mitte** alguses välja filtreerida
- **deny/drop** liiklus: hoia alles (hiljem FP või korduv rünnak)  
- **Benign pilv/CDN**: ära kohe välista – märgi OSINT-is FP-ks hiljem (Cloudflare, Google, Microsoft, AWS)  
- **Backup/monitoring aknad**: ära kohe lõika – märgi hiljem FP-ks, kui kinnitad  

---

## 6) Ekspordi seaded (CSV)
- **Export** → *CSV*  
- **Delimiter:** koma (`,`), **Encoding:** UTF-8  
- **Include column headers:** *ON*  
- **Datetime format:** ISO kui võimalik  
- Failinimi:  
  `palo_traffic_24h_YYYYMMDD.csv`  
  *(kui teed mitu varianti, lisa suffiks nt `_allow`, `_risk4plus` jne)*  

---

## 7) (Valikuline) Threat logi eraldi väljavõte
- **Monitor → Logs → Threat**  
- Vali veerud: Time, Source, Destination, Application, Threat/Content Type, Threat Name, Action, Severity, Rule, Bytes  
- Filter (näide):
```
((time-received geq 'last-24-hrs') and ((severity eq 'high') or (severity eq 'critical')))
```
- Ekspordi `palo_threat_24h_YYYYMMDD.csv`  

---

## 8) Värvid (ühtlustatud HEX) – referents
- 🔴 Critical → `#FF0000`  
- 🟧 High → `#FFA500`  
- 🟨 Medium → `#FFFF00`  
- 🔵 Low → `#0000FF`  

---

## 9) Kvaliteedikontroll enne Excelit
- kas **Action** ja **Rule** veerud on kaasas?  
- kas **Risk of app** ja/või **Severity** on kaasas?  
- kas ajad (Time) on õiges ajavööndis ja formaadis?  
- kas failisuurus on mõistlik (mitte kärbitud liigselt)?  

---

## 10) Järgmised sammud
- Ava eksporditud CSV **Etapp 1 — Excel** juhendi järgi  
- Tee triage (värvidega), eralda *proxy/dns/ssl/smb/high-risk* filtrid eraldi failideks  
- Jätka **Etapp 2 — CSV ettevalmistamine Excelis**  
- Seejärel **Etapp 3 — Pandas** detailne analüüs  
