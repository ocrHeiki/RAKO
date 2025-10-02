# Etapp 1 — Excel (logide esmase analüüsi juhend)

Selles etapis teed kiire L1-taseme triage Excelis või Google Sheetsis — ei vaja programmeerimist, piisab CSV avamisest.

## Eesmärk
- Eemaldada müra ja tõsta esile kõrge riskiga seansid
- Märgistada valepositiivid (pilv, CDN, monitooring)
- Eksportida filtrid edasiseks analüüsiks (Pandas/SIEM/OSINT)

## Samm-sammult (Excel)
1. Ava `log.csv` Excelis (File → Open → vali CSV; vajuta „Delimited“ ja vali koma).  
2. Kontrolli veerge: `Start Time`, `Source address`, `Destination address`, `Application`, `Risk of app`, `Bytes`, `Action`, `Rule`, `Source user`.  
3. Lisa Filter (Home → Sort & Filter → Filter).  
4. Tee Conditional Formatting (Home → Conditional Formatting → New Rule → Use a formula):
   - Risk 5 (`Risk of app` = 5) → Täida taust punane (🔴 Critical)
   - Risk 4 (`Risk of app` = 4) → Täida taust oranž (🟧 High)
   - Risk 3 (`Risk of app` = 3) → Täida taust kollane (🟨 Medium)
   - Risk 1–2 (`Risk of app` = 1 OR 2) → Täida taust sinine (🔵 Low)
5. Sorteeri `Risk of app` (kõrge→madal) ja vaata esimesed 200 rida läbi manuaalselt — otsi `http-proxy`, `dns-base`, `ssl`, `ms-ds-smb` application'e.  
6. Filtreeri ja salvesta eraldi Exceli töölehed/CSV-d:
   - `proxy_logs.xlsx` (Application = http-proxy või Risk=5)
   - `dns_logs.xlsx` (Application = dns-base)
   - `ssl_logs.xlsx` (Application = ssl)
   - `smb_logs.xlsx` (Application sisaldab "ms-ds-smb")
7. Lisa veerg `triage_note` ja täida lühimärkused (nt `likely benign - cloud ASN`, `suspicious - needs OSINT`).  
8. Kõik salvestused nimeta formaadis: `proxy_logs_YYYYMMDD_analyst_initial.xlsx`.

## Näpunäited L1 analüütikule
- Kui `Destination address` kuulub tuntud pilveteenusele (Google/Azure/AWS) ja käitumine on ootuspärane → märgi `triage_note = benign-cloud` (valepositiiv).  
- Kui leiad `Http-proxy` või suured `Bytes` väärtused ühelt Source IP-lt → tõsta prioriteet ja jätka Etapp 2/Pandas või Etapp 4/OSINT.

## Üleminek Etapp 2-le
Salvesta filtritud CSV-d ja laadi need Pandasega analüüsimiseks: `02_pandas_juhend.md`.
