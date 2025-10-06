# analuus_nadalakoond_csv.py – Nädala koondanalüüs CSV failidest
# Autor: ocrHeiki (õpiprojekt)
# Kasutus: py analuus_nadalakoond_csv.py
# Eeldused: pip install pandas matplotlib openpyxl

from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re

# Kaustade seadistus
BASE = Path.home() / "Documents" / "SOC"
RAW = BASE / "raw"
PROC = BASE / "processed"
REP = BASE / "reports"
PROC.mkdir(parents=True, exist_ok=True)
REP.mkdir(parents=True, exist_ok=True)

def iso_from_filename(name):
    """Tuvastab kuupäeva failinimest (nt ThreatLog_06.10.2025.csv → 2025-10-06)."""
    m = re.search(r"(\d{2})\.(\d{2})\.(\d{4})", name)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else name

def analyze_csv(path):
    """Analüüsib ühe päeva CSV logi ja tagastab kokkuvõtte."""
    df = pd.read_csv(path, encoding="utf-8", low_memory=False)
    total = len(df)
    sev_counts = df["Severity"].astype(str).str.lower().value_counts() if "Severity" in df.columns else pd.Series(dtype=int)
    hi_crit = int(sev_counts.get("high", 0) + sev_counts.get("critical", 0))
    hi_crit_pct = round(100 * hi_crit / total, 2) if total else 0.0
    risk_avg = df["Risk"].mean() if "Risk" in df.columns else None
    return {
        "date": iso_from_filename(path.name),
        "alerts_total": total,
        "critical": int(sev_counts.get("critical", 0)),
        "high": int(sev_counts.get("high", 0)),
        "medium": int(sev_counts.get("medium", 0)),
        "low": int(sev_counts.get("low", 0)),
        "hi_crit": hi_crit,
        "hi_crit_pct": hi_crit_pct,
        "risk_avg": round(risk_avg, 2) if risk_avg else None,
    }

def main():
    csv_files = sorted(RAW.glob("ThreatLog_*.csv"))
    if not csv_files:
        print("[!] Ei leitud ühtegi CSV faili kaustast 'raw/'.")
        return
    
    print(f"[i] Leiti {len(csv_files)} faili analüüsiks.")
    results = [analyze_csv(p) for p in csv_files]
    week = pd.DataFrame(results).sort_values("date").reset_index(drop=True)

    # Delta arvutused
    for col in ["alerts_total", "hi_crit", "hi_crit_pct"]:
        week[f"{col}_delta"] = week[col].diff().fillna(0).round(2)

    # Salvestus
    today = datetime.now().date().isoformat()
    csv_out = PROC / f"nadalakoond_{today}.csv"
    xlsx_out = PROC / f"nadalakoond_{today}.xlsx"
    week.to_csv(csv_out, index=False, encoding="utf-8")
    week.to_excel(xlsx_out, index=False)
    print(f"[+] Salvesta: {csv_out}")
    print(f"[+] Salvesta: {xlsx_out}")

    # Trendigraafik
    plt.figure(figsize=(10, 6))
    plt.plot(week["date"], week["alerts_total"], marker="o", label="Kokku alerts")
    plt.plot(week["date"], week["hi_crit"], marker="o", label="High+Critical")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.title("Nädala alertide trend")
    plt.tight_layout()
    png_out = REP / f"nadal_trendid_{today}.png"
    plt.savefig(png_out)
    plt.close()
    print(f"[+] Graafik: {png_out}")

    print("\n[OK] Nädala analüüs lõpetatud!")

if __name__ == "__main__":
    main()
