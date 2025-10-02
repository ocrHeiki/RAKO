# Lisa — VirusTotal automaatkontroll (lihtne näide)

See leht annab näite, kuidas automatiseerida IP-de kiire kontroll ilma keeruka infrastruktuurita. Kasuta API võtmeid vastavalt teenuse tingimustele.

## 1) Mida teha käsitsi (ilma API võtmeta)
- Kopeeri IP list (Top Destination) Excelist ja kleebi VirusTotal veebiliidese otsingusse ükshaaval (või tee CSV impordiga batch, kui konto lubab).

## 2) Lihtne Python skript (näidis)
```python
import requests, time
VT_API_KEY = "SINU_VT_API_KEY"
headers = {"x-apikey": VT_API_KEY}
def vt_check_ip(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    return None

ips = ["185.203.116.5","198.51.100.10"]
for ip in ips:
    resp = vt_check_ip(ip)
    print(ip, resp["data"]["attributes"]["last_analysis_stats"])
    time.sleep(15)  # väldi rate limit'e
```

## 3) AbuseIPDB näide (API)
```python
import requests
ABUSE_KEY = "SINU_ABUSE_KEY"
url = "https://api.abuseipdb.com/api/v2/check"
params = {"ipAddress": "185.203.116.5", "maxAgeInDays": 90}
headers = {"Key": ABUSE_KEY, "Accept": "application/json"}
r = requests.get(url, headers=headers, params=params)
print(r.json())
```

## Märkused
- API võtmed võivad olla piiratud; ärge jagage neid avalikult.
- Kui ei ole õigusi skriptide jooksutamiseks, kasuta veebiliideseid ja tee ekraanitõmmised.

