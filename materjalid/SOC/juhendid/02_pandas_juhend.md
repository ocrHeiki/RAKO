# Etapp 2 — Pandas (detailsem filtreerimine ja analüüs)

Alljärgnevad **täpsed sammud ja koodinäited** töötavad failiga `log.csv` (Palo Alto TRAFFIC 24h).  
Kopeeri koodijupid Jupyter/VSCode/terminali. Kui sul pole Pythonit, kasuta Etapp 1 (Excel).

> **NB!** Ära lükka ettevõtte päris logisid avalikku keskkonda. Kood töötab lokaalselt.

---

## 1) Laadimine ja esmavaade

```python
import pandas as pd

df = pd.read_csv("log.csv", low_memory=False)
# (soovi korral) kui on ajatemplid:
for col in ["Start Time", "End Time", "High Res Timestamp"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
df.head(3)
df.columns.tolist()
```

**Kontrolli veerge:** `Application`, `Source address`, `Destination address`, `Risk of app`, `Bytes`, `Action`, `Rule`, `Source user`.

---

## 2) Kõrge riskiga liiklus (Risk ≥ 4)

```python
high = df[df["Risk of app"] >= 4]
high.to_csv("high_risk.csv", index=False)
high["Application"].value_counts().head(10)
```

**Sammud:**  
- Vaata, kas tipus on `http-proxy`, `ssl`, `web-browsing`.  
- Kui `http-proxy` → märgi **🔴/🟧** ja liigu OSINT kontrollile (Etapp 4).

---

## 3) HTTP-Proxy ja muud Risk 5

```python
crit = df[df["Risk of app"] == 5]
proxy = df[df["Application"].str.lower()=="http-proxy"]
suspicious = pd.concat([crit, proxy]).drop_duplicates()
suspicious[["Start Time","Source address","Destination address","Bytes","Rule"]].head(20)
suspicious.to_csv("risk5_proxy.csv", index=False)
```

**Mida otsida:**  
- Kas `Source address` on tööjaam? Kas `Destination address` kuulub hostingule (vt OSINT)?  
- Suured `Bytes` väärtused võivad viidata andmeväljavoolule.

---

## 4) DNS anomaaliad (võimalik tunneldus)

```python
dns = df[df["Application"].str.lower()=="dns-base"]
top_dns_sources = dns["Source address"].value_counts().head(20)
top_dns_sources.to_csv("top_dns_sources.csv")
top_dns_sources
```

**Heuristikad:**  
- Kui üks `Source address` teeb **tuhandeid** päringuid 24h jooksul → tõsta **🟨 → 🟧**.  
- Kui sul on veerg `Destination domain`, võta Top 20 ja vaata OSINT-is.

---

## 5) SSL ühendused tundmatutesse kohtadesse

```python
ssl = df[df["Application"].str.lower()=="ssl"]
# (valikuline) kui sul on whitelist CIDR/valdkondade kaupa, eemalda need:
whitelist = ["13.107.", "52.112.", "52.122."]  # Microsoft/Azure näited
susp_ssl = ssl[~ssl["Destination address"].astype(str).str.startswith(tuple(whitelist))]
susp_ssl.to_csv("ssl_sus.csv", index=False)
susp_ssl["Destination address"].value_counts().head(20)
```

**Mida otsida:**  
- Palju seansse ühe tundmatu IP suunas.  
- Seadista OSINT kontroll (Etapp 4).

---

## 6) SMB lateraalliikumise kontroll

```python
smb = df[df["Application"].str.contains("ms-ds-smb", case=False, na=False)]
work_subnet = "172.24."
lateral = smb[smb["Source address"].astype(str).str.startswith(work_subnet) &
              smb["Destination address"].astype(str).str.startswith(work_subnet)]
lateral.to_csv("smb_lateral.csv", index=False)
lateral[["Source address","Destination address"]].value_counts().head(15)
```

**Märgid:** tööjaam ↔ tööjaam ühendused → **🟧/🔴** vastavalt kontekstile.

---

## 7) Top IP-d (24h kokkuvõte)

```python
top_src = df["Source address"].value_counts().head(15)
top_dst = df["Destination address"].value_counts().head(15)
top_src.to_csv("top_source_24h.csv")
top_dst.to_csv("top_dest_24h.csv")
top_src, top_dst
```

---

## 8) Võrdlus eelmise 24h-ga

Loe sisse ka eilne fail (nt `log_yesterday.csv`) ja võrdle pilti.

```python
df_y = pd.read_csv("log_yesterday.csv", low_memory=False)

def risk_counts(frame):
    return frame["Risk of app"].value_counts().reindex([1,2,3,4,5], fill_value=0)

today_risks = risk_counts(df)
yday_risks = risk_counts(df_y)
delta = today_risks - yday_risks
delta.rename("Delta (täna - eile)")
```

**Tõlgendus:** kui `Risk 4/5` kasvas oluliselt, too see raportis välja.

---

## 9) 7 päeva kokkuvõte (päevade lõikes)

```python
import glob

# Eelda et sul on 7 CSV faili: log_2025-10-01.csv, log_2025-09-30.csv, ...
paths = sorted(glob.glob("log_*.csv"))[-7:]
summary = []
for p in paths:
    x = pd.read_csv(p, low_memory=False)
    counts = x["Risk of app"].value_counts().reindex([1,2,3,4,5], fill_value=0)
    summary.append({"date": p.split("log_")[-1].split(".csv")[0],
                    "low": counts[1]+counts[2],
                    "med": counts[3],
                    "high": counts[4],
                    "crit": counts[5]})
wk = pd.DataFrame(summary).set_index("date")
wk.to_csv("weekly_severity.csv")
wk
```

**Raportis:** joonista sellest line chart (Etapp 3) ja kirjelda trendid.

---

## 10) Valepositiivide tuvastus (heuristikad)

- **Pilveteenused (ASN: Amazon/Microsoft/Google)**: kui siht-IP kuulub nende ASN-ile ja käitumine on ootuspärane → **🔵/🟨**.  
- **CDN / DNS resolv**: suur maht ei pruugi olla pahatahtlik.  
- **Monitooring (Zabbix/SNMP/Ping)**: palju ühendusi on normaalne.  
- **Ajastus**: hoolduse ajal tekkinud tipud → sageli benign.

---

## 11) Ekspordid raportisse

```python
high.to_csv("raport_high.csv", index=False)
suspicious.to_csv("raport_critical_proxy.csv", index=False)
lateral.to_csv("raport_smb_lateral.csv", index=False)
wk.to_csv("raport_weekly_severity.csv")
```

Lisa need kokkuvõtted Word/Markdown raporti mallis vastavatesse jaotistesse (ilma toorest logi paljastamata).
