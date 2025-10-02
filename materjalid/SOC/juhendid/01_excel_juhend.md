# Etapp 1 — Excel (logide esmase analüüsi juhend)

Selles etapis tehakse L1-taseme triage Excelis või Google Sheetsis.  
Eesmärk: kiiresti leida kõrge riskiga ühendused ja eristada valepositiivid.

---

## Kasutatavad väljad
- **Severity** (tekst: `critical` / `high` / `medium` / `low`)
- **Risk of app** (arv: `1–5`)
- **Action** (`allow` / `deny` / `drop`)
- **Rule** (millise poliitika alt lubati/keelati)
- **Source address**, **Destination address**
- **Application**
- **Bytes**
- **User** (vajadusel)
- **Start Time** / **End Time** / **High Res Timestamp**

---

## Värvikoodid (kasuta alati samu)
- 🔴 **Critical** → HEX `#FF0000`
- 🟧 **High** → HEX `#FFA500`
- 🟨 **Medium** → HEX `#FFFF00`
- 🔵 **Low** → HEX `#0000FF`

> Kui logis on **Severity** ja **Risk of app** mõlemad, kasuta _visuaalseks_ märgistamiseks **Severity** (selgem tekstina) ja _statistikaks_ **Risk of app** (arvuline).

---

## Samm-sammult (Excel / Google Sheets)

1. **Ava CSV**  
   File → Open → `log.csv`. Kontrolli, et eraldaja on koma.

2. **Lülita filtrid sisse**  
   Home → Sort & Filter → **Filter** (või Sheets: Data → Create a filter).

3. **Tee kaks Conditional Formatting reeglistikku**  
   **A. Kui olemas `Severity` (tekst):**  
   - Contains “critical” → **Fill color** `#FF0000`  
   - Contains “high” → **Fill color** `#FFA500`  
   - Contains “medium” → **Fill color** `#FFFF00`  
   - Contains “low” → **Fill color** `#0000FF`

   **B. Kui olemas ainult `Risk of app` (arv):**  
   - `=5` → **Fill** `#FF0000`  
   - `=4` → **Fill** `#FFA500`  
   - `=3` → **Fill** `#FFFF00`  
   - `=1` **OR** `=2` → **Fill** `#0000FF`

4. **Sorteeri riskitaseme järgi**  
   Pane kõrgeimad ette (Severity: critical/high; Risk: 5/4).

5. **Kontrolli `Action`**  
   - `allow` → kas see oli ootuspärane? Kui risk kõrge (4–5), võib olla intsident.  
   - `deny`/`drop` → enamasti madalam prioriteet, **kui** just pole korduv muster samast allikast.

6. **Kontrolli `Rule`**  
   - Kui lubati liiga laia reegliga (nt “allow any”) ja Risk on kõrge → **märgi eskaleerimiseks**.  
   - Kui lubati spetsiifilise, ootuspärase reegliga → tõenäoliselt **benign**.

7. **Lisa veerg `triage_note`**  
   Lühimärkused ridadele:  
   - `benign-cloud (ASN=Amazon)`  
   - `suspicious-proxy (large bytes)`  
   - `check-dns (high volume)`  
   - `ssl-unknown-dst (OSINT)`  
   - `smb-lateral (ws↔ws)`

8. **Salvesta**  
   Nimeline: `logitriage_YYYYMMDD_analyst.xlsx`

---

## Mida vaadata (kiire triage)

- **HTTP-Proxy (Risk 5)** → väga prioriteetne (andmeleke/C2 oht).  
- **DNS mass** (`dns-base`) → võimalik tunneldus (vaata mahtu ja kordust).  
- **SSL** → kui siht on tundmatu ASN/host → OSINT.  
- **SMB** → tööjaam ↔ tööjaam = lateraalliikumise kahtlus.

---

## Valepositiivid (sagedased põhjused)

- **Pilveteenused / CDN** (Google, Microsoft, AWS, Cloudflare): kõrge maht, kuid **legitiimne**.  
- **Monitooring** (Zabbix, SNMP, Ping): palju ühendusi → **normaalne**.  
- **Hooldustööd / Backups**: tipud ajas, kuid **plaanilised**.

---

## Näpunäited ja parimad tavad

- **Kasuta paralleelselt** Severity _ja_ Risk of app, et vältida pimedat nurka.  
- **Vaata Action + Rule konteksti**: blokitud liiklus ≠ intsident; lubatud kõrge riskiga liiklus = uurimise fookus.  
- **Dokumenteeri järjepidevalt** `triage_note` veerus (hiljem aitab Etapp 6 raportit).

---

## Valmistumine Etapp 2 jaoks (CSV-de ettevalmistus)

Järgmises etapis filtreerime Excelis eraldi logifailid (`high_risk.csv`, `proxy_logs.csv`, `dns_logs.csv`, `ssl_logs.csv`, `smb_logs.csv`).  
→ Jätka: **`juhendid/02_csv_valmistamine.md`**
