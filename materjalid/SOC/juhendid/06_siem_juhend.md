# Etapp 6 — SIEM (alertid ja päringud)

See juhend annab praktilised päringu- ja alerti-näited Splunkile ja Elastic/Kibana'le, et saaksid L1→L3 tasemel triage ja eskalatsiooni teha.

## Eesmärk
- Korrelatsiooni tegemine logide vahel
- Automaatsete alertide loomine Risk>=4, DNS anomaaliad, SMB lateral movement
- Kiire päring ja tõendusmaterjal ticketisse

## Splunk näited
1. Kõrge risk (Risk >= 4)
```
index=paloalto sourcetype=paloalto_traffic "Risk of app">=4
| stats count by Application, "Destination address", "Source address"
| sort -count
```
2. HTTP-Proxy (Risk 5)
```
index=paloalto sourcetype=paloalto_traffic (Application="http-proxy" OR "Risk of app"=5)
| table _time, "Source address", "Destination address", Bytes, Rule, Action
```
3. DNS high volume (üks host > X päringut tunnis)
```
index=paloalto sourcetype=paloalto_traffic Application="dns-base"
| bucket _time span=1h
| stats count by _time, "Source address"
| where count > 1000
| table _time, "Source address", count
```

## Elastic/Kibana (KQL) näited
1. Risk >=4
```
event.dataset: "paloalto.traffic" and "Risk of app": >= 4
```
2. DNS single host high volume (saved search / alert)
```
application: "dns-base" and event.outcome: "success" 
| group by source.address | order by count desc
```
3. SMB lateral movement (workstation→workstation)
- Salvesta saved search, mis filtreerib SMB ja grupeerib source/destination

## Alerti soovitused (tõstke priority)
- Alert kui `Application == http-proxy` ja Source ei ole whitelist'is → High
- Alert kui üks host teeb >1000 DNS päringut tunnis → High
- Alert kui SMB liiklus tööjaamade vahel → High/Critical
- Alert kui Destination IP on VT/AbuseDB kinnitatud pahatahtlik → Critical

## SIEM evidence & ticket fields
- LISA ticketisse alati: timestamp, source, destination, application, risk, bytes, OSINT viited (VirusTotal link), analüütiku märkused, tehtud sammud.

## Soovitused L1 analüütikule
- Kui sul puudub SIEMi ligipääs, genereeri CSV-d (Etapp 1/2) ja edasta L2-le koos triage-märkustega.

