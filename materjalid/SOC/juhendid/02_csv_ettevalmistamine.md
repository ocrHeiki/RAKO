# Etapp 2 — CSV-de ettevalmistamine Excelis

Selles etapis valmistame ette eraldi CSV-failid, mida Etapp 3 (Pandas) vajab.  
Failid **filtreeritakse Excelis** ja salvestatakse väiksemateks logikomplektideks, et analüüsida täpsemalt.

---

## Samm-sammult

1. Ava **log.csv** Excelis (või Google Sheetsis).  
2. **Lisa Filter** kõigile veergudele (Data → Filter).  
3. Filtreeri järgmised kategooriad ükshaaval ja salvesta uue failina:

### A) Kõrgriskilised ühendused
- Filtreeri `Severity = critical/high`  
  või `Risk of app >= 4`.  
- Salvesta kui: **`high_risk.csv`**

### B) HTTP-Proxy
- Filtreeri `Application = http-proxy`  
  või `Risk of app = 5`.  
- Salvesta kui: **`proxy_logs.csv`**

### C) DNS liiklus
- Filtreeri `Application = dns-base`.  
- Salvesta kui: **`dns_logs.csv`**

### D) SSL ühendused
- Filtreeri `Application = ssl`.  
- Salvesta kui: **`ssl_logs.csv`**

### E) SMB liiklus
- Filtreeri `Application` sisaldab `ms-ds-smb`.  
- Salvesta kui: **`smb_logs.csv`**

---

## Failinime formaat
Kasuta ühtset formaati:  
{teema}_YYYYMMDD_{analyst}.csv

Näited:  
- `high_risk_20251002_ab.csv`  
- `proxy_logs_20251002_ab.csv`

---

## Miks eraldi CSV-d?
- Pandas saab hiljem kiiremini analüüsida väiksemaid fokusseeritud logifaile.  
- SOC töövoos on selge, millist liiklust vaadatakse (nt DNS-anomaaliad, SSL-sihtkohad, SMB-lateraalliikumine).  
- Võrdlus eelmise päeva või 7 päeva jooksul muutub lihtsamaks.  

---

## Valmistumine Etapp 3 jaoks
Kui need failid on valmis, jätka **Etapp 3 (Pandas)** juhendi järgi:  
- Laadi CSV Pandasesse  
- Tee riskitasemete põhine filtreerimine  
- Analüüsi valepositiive  
- Ekspordi raportisse
