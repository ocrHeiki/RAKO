#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SOC L1 – Palo Alto RAW → TOP10 → Internal/OSINT Enrichment → Report (CSV + Markdown)

- Ilma väliste teekideta: kasutab ainult Python standardteeki (urllib, csv, json, socket, ipaddress, re, argparse).
- OSINT: AbuseIPDB, VirusTotal, OTX, ipinfo – HTTP päringud urllib'iga (keskkonnamuutujate alusel).
- WHOIS: port 43 (best-effort). Kui võrgu poliitika keelab, jäetakse vahele.
- Raport: Markdown (.md), mitte DOCX (vältimaks sõltuvusi).

Kasutus:
  python3 soc_top10_osint.py --raw-dir RAW --outdir results --md-report
"""
import os, sys, csv, json, re, argparse, socket, time, ipaddress
from collections import Counter, defaultdict
from datetime import datetime
from typing import Dict, Any, Iterable, List, Tuple
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import URLError, HTTPError

# ---- ENV KEYS (kui on) ----
ABUSEIPDB_KEY = os.getenv("ABUSEIPDB_KEY", "")
VT_API_KEY     = os.getenv("VT_API_KEY", "")
OTX_API_KEY    = os.getenv("OTX_API_KEY", "")
IPINFO_TOKEN   = os.getenv("IPINFO_TOKEN", "")

UA = ("SOC-L1-Top10-OSINT/1.0")
SLEEP = 0.5  # väike paus APIde vahel

# ---- Väljade kaardistused ----
SRC_KEYS = ["source address","src_ip","src","source","client_ip"]
DST_KEYS = ["destination address","dst_ip","dst","destination","server_ip"]
THR_KEYS = ["threat/content name","threatname","threat","content","signature","msg"]
SEV_KEYS = ["severity"]
ACT_KEYS = ["action"]
APP_KEYS = ["application"]
RUL_KEYS = ["rule"]
DEV_KEYS = ["device name","devicename","device"]
TIME_KEYS= ["receive time","time logged","generate time","receive_time","high res timestamp"]

IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
CIDR_RE = re.compile(r'^\s*(\d{1,3}(?:\.\d{1,3}){3})(?:/(\d{1,2}))?\s*$')
RANGE_RE = re.compile(r'^\s*(\d{1,3}(?:\.\d{1,3}){3})\s*-\s*(\d{1,3}(?:\.\d{1,3}){3})\s*$')

# ---- Heuristikad ----
LOW_FP_MIN_EVENTS = 50
LOW_FP_LOW_RATIO  = 0.8
WELL_KNOWN_UPDATE_PORTS = {80, 443, 8530, 52311}
COMMON_SERVICE_PORTS = {53, 80, 443, 22, 21, 123, 445, 3389}

def normkey(k: str) -> str:
    return (k or "").strip().lower()

def lower_keys(d: Dict[str, Any]) -> Dict[str, Any]:
    return {normkey(k): v for k, v in d.items()}

def pick_field(row: Dict[str,Any], candidates: List[str]) -> Any:
    for k in candidates:
        if k in row and row[k] not in (None, ""):
            return row[k]
    for k in row.keys():
        base = k.split(".")[-1]
        if base in candidates and row.get(k) not in (None, ""):
            return row[k]
    return None

def parse_ip_or_cidr(value):
    if not value: return (None, None)
    v = str(value).strip()
    m = CIDR_RE.match(v)
    if m:
        ip = ipaddress.ip_address(m.group(1))
        if m.group(2) is not None:
            net = ipaddress.ip_network(v, strict=False)
            return ('cidr', net)
        return ('ip', ip)
    mr = RANGE_RE.match(v)
    if mr:
        a = ipaddress.ip_address(mr.group(1))
        b = ipaddress.ip_address(mr.group(2))
        return ('range', (a,b))
    if '-' in v:
        try:
            a, b = [ipaddress.ip_address(x.strip()) for x in v.split('-',1)]
            return ('range', (a,b))
        except:
            pass
    try:
        ip = ipaddress.ip_address(v)
        return ('ip', ip)
    except:
        return (None, None)

def is_private_entity(kind, ent) -> bool:
    if kind == 'ip':
        return ipaddress.ip_address(ent).is_private
    if kind == 'cidr':
        return ent.network_address.is_private
    if kind == 'range':
        return ent[0].is_private and ent[1].is_private
    return False

def parse_int_safe(x, default=0) -> int:
    try:
        return int(x)
    except:
        try:
            return int(float(x))
        except:
            return default

# ---------- HTTP helper (urllib) ----------
def http_get_json(url: str, headers: Dict[str,str]=None, params: Dict[str,str]=None, timeout=15):
    if params:
        q = urlencode(params)
        if "?" in url:
            url = f"{url}&{q}"
        else:
            url = f"{url}?{q}"
    req = Request(url, headers={"User-Agent": UA, **(headers or {})})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read().decode("utf-8", errors="ignore")
            try:
                return json.loads(data)
            except:
                return {"raw": data}
    except HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except URLError as e:
        return {"error": f"URL error: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}

# ---------- RAW lugemine ----------
def flatten_json(d, parent_key="", sep="."):
    items = []
    if isinstance(d, list):
        for i, v in enumerate(d):
            items.extend(flatten_json(v, f"{parent_key}{sep}{i}" if parent_key else str(i), sep=sep).items())
    elif isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, d))
    return dict(items)

def parse_plain_line(line: str) -> Dict[str, Any]:
    m = IP_RE.search(line)
    if not m:
        return {}
    src_ip = m.group(0)
    threat = None
    for key in ["threat","content","signature","attack","msg","alert","category"]:
        mt = re.search(rf"{key}[:=]\s*([^|,\]]+)", line, re.IGNORECASE)
        if mt:
            threat = mt.group(1).strip()
            break
    if not threat:
        mt = re.search(r'"([A-Za-z0-9._\- ]{4,60})"', line)
        if mt:
            threat = mt.group(1).strip()
    return lower_keys({"source address": src_ip, "threat/content name": (threat or "unknown")})

def read_files(raw_dir: str) -> Iterable[Tuple[str, Dict[str, Any]]]:
    for root, _, files in os.walk(raw_dir):
        for fn in files:
            path = os.path.join(root, fn)
            lower = fn.lower()
            try:
                if lower.endswith(".csv"):
                    with open(path, newline="", encoding="utf-8", errors="ignore") as f:
                        r = csv.DictReader(f)
                        for row in r:
                            yield (path, lower_keys(row))
                elif lower.endswith(".json") or lower.endswith(".jsonl") or lower.endswith(".ndjson"):
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            line=line.strip()
                            if not line: continue
                            try:
                                obj = json.loads(line)
                                row = lower_keys(flatten_json(obj))
                                yield (path, row)
                            except:
                                continue
                else:
                    with open(path, encoding="utf-8", errors="ignore") as f:
                        for line in f:
                            line=line.strip()
                            if not line: continue
                            row = parse_plain_line(line)
                            if row: yield (path, row)
            except Exception as e:
                print(f"[WARN] lugemine ebaõnnestus {path}: {e}", file=sys.stderr)

# ---------- Analüüs ----------
def analyse_top(raw_dir: str):
    src_counter = Counter()
    threat_counter = Counter()
    threat_to_srcs = defaultdict(Counter)
    device_counter = Counter()
    low_threat_counter = Counter()

    rows = []
    paths_seen = set()
    latest_ts = None

    for path, row in read_files(raw_dir):
        rows.append((path, row))
        paths_seen.add(path)

        src = pick_field(row, SRC_KEYS)
        thr = pick_field(row, THR_KEYS)
        dev = pick_field(row, DEV_KEYS)
        sev = (pick_field(row, SEV_KEYS) or "").lower()

        if src:
            src_counter[str(src)] += 1
        if thr:
            tnorm = str(thr).strip()
            threat_counter[tnorm] += 1
            if src:
                threat_to_srcs[tnorm][str(src)] += 1
        if dev:
            device_counter[str(dev)] += 1

        if sev == "low" and thr:
            low_threat_counter[str(thr).strip()] += 1

        ts = pick_field(row, TIME_KEYS)
        if ts:
            try:
                tstr = str(ts)
                if "T" in tstr:
                    dt = datetime.fromisoformat(tstr.replace("Z","+00:00"))
                else:
                    dt = datetime.strptime(tstr[:16], "%d.%m.%Y %H:%M")
                if (latest_ts is None) or (dt > latest_ts):
                    latest_ts = dt
            except:
                pass

    top_src = src_counter.most_common(10)
    top_thr = threat_counter.most_common(10)
    top_low_thr = low_threat_counter.most_common(10)
    device = device_counter.most_common(1)[0][0] if device_counter else "unknown-device"

    candidate_ips = []
    for t,_ in top_thr:
        for ip,_c in threat_to_srcs[t].most_common(2):
            candidate_ips.append(ip)
    candidate_ips.extend([ip for ip,_ in top_src])

    seen=set(); ordered=[]
    for ip in candidate_ips:
        if ip not in seen:
            seen.add(ip); ordered.append(ip)
    ips_for_enrichment = ordered[:10]

    return {
        "rows": rows,
        "files": sorted(paths_seen),
        "latest_ts": latest_ts,
        "device": device,
        "top_src": top_src,
        "top_threat": top_thr,
        "top_low_threat": top_low_thr,
        "threat_to_srcs": threat_to_srcs,
        "ips_for_enrichment": ips_for_enrichment,
    }

# ---------- Internal konteksti analüüs ----------
def internal_context_analysis(src_entity: str, rows_for_ip: List[Tuple[str,Dict[str,Any]]]) -> Dict[str,Any]:
    stats = {"events": len(rows_for_ip), "sev": Counter(), "act": Counter(), "apps": Counter(),
             "ports": Counter(), "rules": Counter(), "hours": Counter(), "dst_countries": Counter()}
    for _, r in rows_for_ip:
        stats["sev"][(pick_field(r, SEV_KEYS) or "").lower()] += 1
        stats["act"][(pick_field(r, ACT_KEYS) or "").lower()] += 1
        stats["apps"][(pick_field(r, APP_KEYS) or "").lower()] += 1
        p = pick_field(r, ["destination port","destination_port","dst_port"]) or 0
        stats["ports"][parse_int_safe(p)] += 1
        stats["rules"][(pick_field(r, RUL_KEYS) or "").lower()] += 1
        c = (r.get("destination country") or r.get("destination_country") or "").lower()
        stats["dst_countries"][c] += 1
        t = pick_field(r, TIME_KEYS)
        if t and len(str(t))>=13:
            stats["hours"][str(t)[11:13]] += 1

    reasons=[]; fp_score=0; mal_score=0
    total = stats["events"]
    low_ratio = (stats["sev"]["low"]/total) if total else 0.0

    if total >= LOW_FP_MIN_EVENTS and low_ratio >= LOW_FP_LOW_RATIO:
        fp_score += 40; reasons.append("Palju sündmusi ja valdavalt LOW")
    if stats["act"].get("allow",0) and (stats["sev"].get("high",0) or stats["sev"].get("critical",0)):
        mal_score += 40; reasons.append("ALLOW + HIGH/CRITICAL kombinatsioon")
    if total > 10 and stats["hours"]:
        h, cnt = stats["hours"].most_common(1)[0]
        if cnt >= total*0.6:
            fp_score += 10; reasons.append(f"Sündmused koonduvad kella {h} kanti (ajastatud töö)")
    for p,_ in stats["ports"].most_common(3):
        if p in WELL_KNOWN_UPDATE_PORTS: fp_score += 10
        if p in COMMON_SERVICE_PORTS: fp_score += 5

    decision = "needs_review"
    if mal_score >= 70: decision = "malicious"
    elif fp_score >= 50 and mal_score < 30: decision = "likely_false_positive"
    elif mal_score >= 30: decision = "suspicious"

    return {
        "decision": decision, "fp_score": fp_score, "mal_score": mal_score, "reasons": reasons,
        "top_apps": stats["apps"].most_common(3), "top_ports": [p for p,_ in stats["ports"].most_common(3)],
        "top_rules": stats["rules"].most_common(3), "actions": dict(stats["act"]), "severities": dict(stats["sev"]),
        "events": total, "dst_countries": dict(stats["dst_countries"]), "hours": dict(stats["hours"])
    }

# ---------- NAT avalik IP OSINTiks ----------
def pick_nat_public_ip(row: Dict[str,Any]) -> str:
    candidates = [
        row.get("nat source ip"), row.get("nat_source_ip"),
        row.get("nat destination ip"), row.get("nat_destination_ip"),
        pick_field(row, SRC_KEYS),
        pick_field(row, DST_KEYS),
    ]
    for val in candidates:
        kind, ent = parse_ip_or_cidr(val)
        if kind == 'ip' and ent and not ent.is_private:
            return str(ent)
    return None

# ---------- rDNS ----------
def rdns_lookup(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None

# ---------- WHOIS (best-effort, port 43) ----------
def whois_lookup(ip: str):
    servers = ["whois.arin.net","whois.ripe.net","whois.apnic.net","whois.lacnic.net","whois.afrinic.net"]
    query = ip + "\r\n"
    for host in servers:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((host, 43))
            s.send(query.encode("ascii", errors="ignore"))
            data = b""
            while True:
                chunk = s.recv(4096)
                if not chunk: break
                data += chunk
            s.close()
            text = data.decode("utf-8", errors="ignore")
            if "NetName" in text or "inetnum" in text or "OrgName" in text:
                return {"whois_server": host, "raw": text[:2000]}
        except Exception:
            continue
    return None

# ---------- ipinfo ----------
def ipinfo_lookup(ip: str):
    url = f"https://ipinfo.io/{ip}/json"
    params = {}
    if IPINFO_TOKEN:
        params["token"] = IPINFO_TOKEN
    return http_get_json(url, params=params)

# ---------- AbuseIPDB ----------
def abuseipdb_lookup(ip: str):
    if not ABUSEIPDB_KEY:
        return {"error":"no_api_key"}
    headers = {"Key": ABUSEIPDB_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}
    return http_get_json("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params)

# ---------- VirusTotal v3 ----------
def virustotal_lookup(ip: str):
    if not VT_API_KEY:
        return {"error":"no_api_key"}
    headers = {"x-apikey": VT_API_KEY}
    return http_get_json(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}", headers=headers)

# ---------- AlienVault OTX ----------
def otx_lookup(ip: str):
    if not OTX_API_KEY:
        return {"error":"no_api_key"}
    headers = {"X-OTX-API-KEY": OTX_API_KEY}
    return http_get_json(f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/general", headers=headers)

# ---------- OSINT otsus ----------
def extract_vt_positives(vt_json: dict) -> int:
    try:
        stats = vt_json.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        return int(stats.get("malicious", 0)) + int(stats.get("suspicious", 0))
    except Exception:
        return 0

def extract_abuse_conf(aip: dict) -> int:
    try:
        return int(aip.get("data",{}).get("abuseConfidenceScore") or aip.get("abuseConfidenceScore") or aip.get("confidence") or 0)
    except Exception:
        return 0

def extract_otx_pulses(otx_json: dict) -> int:
    try:
        pulses = otx_json.get("pulse_info", {}).get("pulses", [])
        return len(pulses)
    except Exception:
        return 0

def do_osint_for_ip(ip: str) -> Dict[str,Any]:
    osint = {}
    osint["rdns"] = rdns_lookup(ip);     time.sleep(SLEEP)
    osint["ipinfo"] = ipinfo_lookup(ip); time.sleep(SLEEP)
    osint["abuseipdb"] = abuseipdb_lookup(ip); time.sleep(SLEEP)
    osint["virustotal"] = virustotal_lookup(ip); time.sleep(SLEEP)
    osint["otx"] = otx_lookup(ip);       time.sleep(SLEEP)

    abuse = extract_abuse_conf(osint.get("abuseipdb", {}) if isinstance(osint.get("abuseipdb"), dict) else {})
    vtpos = extract_vt_positives(osint.get("virustotal", {}) if isinstance(osint.get("virustotal"), dict) else {})
    otxp  = extract_otx_pulses(osint.get("otx", {}) if isinstance(osint.get("otx"), dict) else {})

    score=0; flags=[]
    if abuse >= 50: score += 50; flags.append(f"abuse={abuse}")
    if vtpos >= 1: score += 40; flags.append(f"vt_pos={vtpos}")
    if otxp  >= 1: score += 30; flags.append(f"otx_pulses={otxp}")

    if score >= 70: decision = "malicious"
    elif score >= 30: decision = "suspicious"
    else: decision = "unknown"

    return {"ip": ip, "osint": osint, "verdict": {"decision":decision, "score":score, "flags":flags}}

# ---------- I/O ----------
def write_top_summary(outdir: str, analysis: Dict[str,Any]):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "top10_summary.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section","rank","value","count"])
        for i,(ip,c) in enumerate(analysis["top_src"],1):
            w.writerow(["top_src_ip", i, ip, c])
        for i,(thr,c) in enumerate(analysis["top_threat"],1):
            w.writerow(["top_threat", i, thr, c])
        for i,(thr,c) in enumerate(analysis["top_low_threat"],1):
            w.writerow(["top_low_lowFreq", i, thr, c])
    with open(os.path.join(outdir, "ips_for_enrichment.txt"), "w", encoding="utf-8") as f:
        for ip in analysis["ips_for_enrichment"]:
            f.write(ip+"\n")
    return path

def write_enrich_json_csv(outdir: str, enrich_results: List[Dict[str,Any]]):
    e_dir = os.path.join(outdir, "enrich")
    os.makedirs(e_dir, exist_ok=True)
    for r in enrich_results:
        with open(os.path.join(e_dir, f"{r['ip']}.json"), "w", encoding="utf-8") as f:
            json.dump(r, f, indent=2, ensure_ascii=False)
    path = os.path.join(outdir, "enrich_summary.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["ip","decision","score","flags","abuse_conf","vt_malicious","rdns","country","isp"])
        for r in enrich_results:
            dec = r["verdict"]["decision"]; score=r["verdict"]["score"]
            flags = ";".join(r["verdict"]["flags"])
            aip = r["osint"].get("abuseipdb",{})
            abuse = extract_abuse_conf(aip) if isinstance(aip, dict) else ""
            vt = r["osint"].get("virustotal",{})
            vt_mal = ""
            if isinstance(vt, dict):
                stats = vt.get("data",{}).get("attributes",{}).get("last_analysis_stats",{})
                vt_mal = stats.get("malicious","") if stats else ""
            rdns = r["osint"].get("rdns") or ""
            info = r["osint"].get("ipinfo") or {}
            country = info.get("country","") if isinstance(info, dict) else ""
            isp = info.get("org","") if isinstance(info, dict) else ""
            w.writerow([r["ip"], dec, score, flags, abuse, vt_mal, rdns, country, isp])
    return path

def write_internal_csv(outdir: str, internal_results: List[Dict[str,Any]]):
    path = os.path.join(outdir, "internal_analysis.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["src_entity","decision","fp_score","mal_score","events","top_apps","top_ports","top_rules","reasons"])
        for r in internal_results:
            w.writerow([
                r["src_entity"], r["analysis"]["decision"], r["analysis"]["fp_score"], r["analysis"]["mal_score"],
                r["analysis"]["events"], str(r["analysis"]["top_apps"]), str(r["analysis"]["top_ports"]),
                str(r["analysis"]["top_rules"]), "; ".join(r["analysis"]["reasons"])
            ])
    return path

def write_md_report(outdir: str, analysis: Dict[str,Any], enrich_results: List[Dict[str,Any]], internal_results: List[Dict[str,Any]]):
    device = analysis["device"]
    date_str = (analysis["latest_ts"].strftime("%Y-%m-%d") if analysis["latest_ts"] else datetime.utcnow().strftime("%Y-%m-%d"))
    fn = os.path.join(outdir, f"Top10_Enrichment_Report_{device}_{date_str}.md")
    lines = []
    lines.append(f"# Palo Alto Threat Log – Top10 IP Enrichment Report")
    lines.append("")
    lines.append(f"- **Device:** {device}")
    if analysis["files"]:
        if len(analysis["files"]) == 1:
            lines.append(f"- **Source Log File:** `{analysis['files'][0]}`")
        else:
            lines.append(f"- **Source Log Files:** {len(analysis['files'])} files")
            for p in analysis["files"][:15]:
                lines.append(f"  - `{p}`")
            if len(analysis["files"]) > 15:
                lines.append(f"  - ...")
    lines.append(f"- **Log Last Timestamp:** {date_str}")
    lines.append(f"- **Generated:** {datetime.utcnow().isoformat()}Z")
    lines.append("\n---\n")

    lines.append("## Top 10 Source IPs")
    for i,(ip,c) in enumerate(analysis["top_src"],1):
        lines.append(f"{i}. `{ip}` — {c}")
    lines.append("")

    lines.append("## Top 10 Threat/Content")
    for i,(t,c) in enumerate(analysis["top_threat"],1):
        lines.append(f"{i}. {t} — {c}")
    lines.append("")

    if analysis["top_low_threat"]:
        lines.append("## Possible False Positives (LOW severity – high frequency)")
        for i,(t,c) in enumerate(analysis["top_low_threat"],1):
            lines.append(f"{i}. {t} — {c}")
        lines.append("")

    if enrich_results:
        lines.append("## OSINT Enrichment (Public IPs)")
        for r in enrich_results:
            lines.append(f"### {r['ip']}")
            v = r["verdict"]
            lines.append(f"- **Decision:** {v['decision']}  |  **Score:** {v['score']}  |  **Flags:** {', '.join(v['flags'])}")
            osint = r["osint"]
            lines.append(f"- **rDNS:** {osint.get('rdns') or '—'}")
            info = osint.get("ipinfo") or {}
            lines.append(f"- **Geo/ISP:** {info.get('country','')} / {info.get('org','') or info.get('hostname','')}")
            abuse = extract_abuse_conf(osint.get('abuseipdb',{}) if isinstance(osint.get('abuseipdb'),dict) else {})
            lines.append(f"- **AbuseIPDB:** confidence={abuse}  ([link](https://www.abuseipdb.com/check/{r['ip']}))")
            vt_pos = extract_vt_positives(osint.get("virustotal",{}) if isinstance(osint.get("virustotal"),dict) else {})
            lines.append(f"- **VirusTotal positives:** {vt_pos}  ([link](https://www.virustotal.com/gui/ip-address/{r['ip']}))")
            otx_p = extract_otx_pulses(osint.get("otx",{}) if isinstance(osint.get("otx"),dict) else {})
            lines.append(f"- **OTX pulses:** {otx_p}  ([link](https://otx.alienvault.com/indicator/ip/{r['ip']}))")
            lines.append("")
    if internal_results:
        lines.append("## Internal Analysis (Private IPs/Subnets)")
        for ent in internal_results:
            a = ent["analysis"]
            lines.append(f"### {ent['src_entity']}")
            lines.append(f"- **Decision:** {a['decision']}  |  **FP Score:** {a['fp_score']}  |  **Mal Score:** {a['mal_score']}  |  **Events:** {a['events']}")
            lines.append(f"- **Top Apps:** {a['top_apps']}")
            lines.append(f"- **Top Ports:** {a['top_ports']}")
            lines.append(f"- **Top Rules:** {a['top_rules']}")
            if a['reasons']:
                lines.append(f"- **Reasons:** " + "; ".join(a['reasons']))
            lines.append("")
    with open(fn, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return fn

# ---------- CLI ----------
def parse_args():
    p = argparse.ArgumentParser(description="SOC L1 – RAW → TOP10 → OSINT/Internal → Report (no external deps)")
    p.add_argument("--raw-dir", "-r", default="RAW", help="Sisendlogide kaust")
    p.add_argument("--outdir", "-o", default="results", help="Väljundkaust")
    p.add_argument("--md-report", action="store_true", help="Genereeri ka Markdown raport (.md)")
    return p.parse_args()

def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    print("[*] Analüüsin RAW:", args.raw_dir)
    analysis = analyse_top(args.raw_dir)

    print(f"[*] Leitud ridu: {len(analysis['rows'])}")
    print("[*] TOP 10 Source IP:")
    for i,(ip,c) in enumerate(analysis["top_src"],1):
        print(f"  {i:>2}. {ip:>15}  {c}")
    print("[*] TOP 10 Threat/Content:")
    for i,(t,c) in enumerate(analysis["top_threat"],1):
        show = t if len(t)<=70 else t[:67]+"..."
        print(f"  {i:>2}. {show}  {c}")

    top_csv = write_top_summary(args.outdir, analysis)
    print("[*] Salvestatud kokkuvõte:", top_csv)

    per_src = defaultdict(list)
    for path, row in analysis["rows"]:
        src = pick_field(row, SRC_KEYS)
        if src:
            per_src[str(src)].append((path, row))

    enrich_targets = analysis["ips_for_enrichment"]
    enrich_results = []
    internal_results = []

    for src_entity in enrich_targets:
        kind, ent = parse_ip_or_cidr(src_entity)
        if kind is None:
            rows_for = per_src.get(src_entity, [])
            nat_ip = None
            for _, r in rows_for:
                nat_ip = pick_nat_public_ip(r)
                if nat_ip: break
            if nat_ip:
                print(f"[*] OSINT (NAT public) {nat_ip}  (src: {src_entity})")
                res = do_osint_for_ip(nat_ip)
                res["src_entity"] = src_entity
                enrich_results.append(res)
            else:
                if rows_for:
                    print(f"[*] Internal analysis (ambiguous): {src_entity}")
                    ia = internal_context_analysis(src_entity, rows_for)
                    internal_results.append({"src_entity": src_entity, "analysis": ia})
            continue

        if is_private_entity(kind, ent):
            rows_for = per_src.get(src_entity, [])
            print(f"[*] Internal analysis (private) {src_entity}  events={len(rows_for)}")
            ia = internal_context_analysis(src_entity, rows_for)
            internal_results.append({"src_entity": src_entity, "analysis": ia})

            nat_ip = None
            for _, r in rows_for:
                nat_ip = pick_nat_public_ip(r)
                if nat_ip: break
            if nat_ip:
                print(f"[*] OSINT (NAT public) {nat_ip}  (src: {src_entity})")
                res = do_osint_for_ip(nat_ip)
                res["src_entity"] = src_entity
                enrich_results.append(res)
        else:
            if kind == 'ip':
                print(f"[*] OSINT {src_entity}")
                res = do_osint_for_ip(src_entity)
                res["src_entity"] = src_entity
                enrich_results.append(res)
            else:
                rows_for = per_src.get(src_entity, [])
                print(f"[*] Public CIDR/RANGE context {src_entity}  events={len(rows_for)}")
                ia = internal_context_analysis(src_entity, rows_for)
                internal_results.append({"src_entity": src_entity, "analysis": ia})

    enrich_csv = write_enrich_json_csv(args.outdir, enrich_results)
    print("[*] Enrichment CSV:", enrich_csv)

    internal_csv = write_internal_csv(args.outdir, internal_results)
    print("[*] Internal CSV:", internal_csv)

    if args.md_report:
        mdp = write_md_report(args.outdir, analysis, enrich_results, internal_results)
        if mdp:
            print("[*] Markdown-raport:", mdp)

    print("[OK] Valmis.")

if __name__ == "__main__":
    main()
