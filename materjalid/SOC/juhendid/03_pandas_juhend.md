# Etapp 3 — Pandas (detailsem filtreerimine ja analüüs)

Selles etapis kasutatakse Python Pandast, et süstemaatiliselt filtreerida ja otsida mustreid 24h logidest (või mitmest järjestikusest päevast).

---

## Värvikoodid (kasuta alati samu)
- 🔴 Critical → HEX `#FF0000`
- 🟧 High → HEX `#FFA500`
- 🟨 Medium → HEX `#FFFF00`
- 🔵 Low → HEX `#0000FF`

---

## 1) Laadimine ja ajaveerud
import pandas as pd

df = pd.read_csv("log.csv", low_memory=False)

# Kui ajatemplid on olemas:
for col in ["Start Time", "End Time", "High Res Timestamp"]:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

---

## 2) Severity (tekst → numbriks) ja Action/Rule kontroll
severity_map = {"critical":5, "high":4, "medium":3, "low":1}
if "Severity" in df.columns:
    df["Severity_num"] = df["Severity"].str.lower().map(severity_map)

if "Action" in df.columns:
    print(df["Action"].value_counts())
if "Rule" in df.columns:
    print(df["Rule"].value_counts().head(10))

**Tõlgendus:**
- Action == "allow" ja (Risk≥4 või Severity_num≥4) → potentsiaalne intsident.  
- Action == "deny" / "drop" → madalam prioriteet, kuid korduvatel juhtudel jälgi edasi.  
- Rule liiga üldine (nt “allow any”) + kõrge risk → eskaleeri.

---

## 3) Kõrge risk kombineeritult
high_combined = df[
    (df.get("Risk of app", 0) >= 4) |
    (df.get("Severity_num", 0) >= 4)
]
cols = ["Start Time","Source address","Destination address",
        "Application","Risk of app","Severity","Action","Rule","Bytes"]
high_combined[[c for c in cols if c in high_combined.columns]].head(20)

---

## 4) HTTP-Proxy ja Risk 5 fookus
crit = df[df.get("Risk of app", 0) == 5]
proxy = df[df.get("Application","").str.lower() == "http-proxy"]
suspicious = pd.concat([crit, proxy]).drop_duplicates()

suspicious.to_csv("risk5_proxy.csv", index=False)
suspicious[["Source address","Destination address","Bytes"]].head(15)

---

## 5) DNS anomaaliad
dns = df[df.get("Application","").str.lower() == "dns-base"]
top_dns_sources = dns["Source address"].value_counts().head(20)
top_dns_sources.to_csv("top_dns_sources.csv")

---

## 6) SSL sihtide puhastus
ssl = df[df.get("Application","").str.lower() == "ssl"]
whitelist_prefix = ("13.107.", "52.112.", "52.122.")
ssl_unknown = ssl[~ssl["Destination address"].astype(str).str.startswith(whitelist_prefix)]
ssl_unknown.to_csv("ssl_unknown.csv", index=False)

---

## 7) SMB lateraalliikumine
smb = df[df.get("Application","").str.contains("ms-ds-smb", case=False, na=False)]
work_subnet = "172.24."
lateral = smb[
    smb["Source address"].astype(str).str.startswith(work_subnet) &
    smb["Destination address"].astype(str).str.startswith(work_subnet)
]
lateral.to_csv("smb_lateral.csv", index=False)

---

## 8) Top IP-d
top_src = df["Source address"].value_counts().head(15)
top_dst = df["Destination address"].value_counts().head(15)
top_src.to_csv("top_source_24h.csv")
top_dst.to_csv("top_dest_24h.csv")

---

## 9) Võrdlus eelmise 24h-ga
df_y = pd.read_csv("log_yesterday.csv", low_memory=False)

def risk_counts(frame):
    base = frame.get("Risk of app")
    if base is None:
        base = frame.get("Severity_num")
    return base.value_counts().reindex([1,2,3,4,5], fill_value=0)

today_risks = risk_counts(df)
yday_risks = risk_counts(df_y)
delta = today_risks - yday_risks
print(delta)

---

## 10) 7 päeva kokkuvõte
import glob

paths = sorted(glob.glob("log_*.csv"))[-7:]
summary = []
for p in paths:
    x = pd.read_csv(p, low_memory=False)
    base = x.get("Risk of app", x.get("Severity_num"))
    counts = base.value_counts().reindex([1,2,3,4,5], fill_value=0)
    summary.append({
        "date": p.split("log_")[-1].split(".csv")[0],
        "low": counts[1] + counts[2],
        "med": counts[3],
        "high": counts[4],
        "crit": counts[5]
    })

wk = pd.DataFrame(summary).set_index("date")
wk.to_csv("weekly_severity.csv")

---

## 11) Valepositiivide tuvastus
- Pilveteenused (AWS, Azure, Google, Cloudflare) võivad näida kõrge riskiga.  
- CDN/resolverid → suur maht, kuid benign.  
- Monitooring (Zabbix, SNMP) → palju ühendusi normaalne.  
- Hooldustööd/backup aknad → sagedased FP.

---

## 12) Ekspordid raportisse
high_combined.to_csv("raport_high.csv", index=False)
suspicious.to_csv("raport_critical_proxy.csv", index=False)
ssl_unknown.to_csv("raport_ssl_unknown.csv", index=False)
lateral.to_csv("raport_smb_lateral.csv", index=False)
wk.to_csv("raport_weekly_severity.csv")
