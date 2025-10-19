# 🔐 Kuidas eksportida Palo Alto Threat Logisid

## Sisse logimine

1. Mine: `https://<palo-alto-ip>/`
2. Sisene oma kasutajanime ja parooliga

## Logide otsimine

1. Mine: `Monitor > Logs > Threat`
2. Määratle ajavahemik:
   - Last 24 hours
   - Custom: kuupäevad

## Filter

- Severity: medium, high, critical
- Action ≠ Allow

## Andmete eksportimine

1. Kliki: `Export`
2. Vali formaat: `CSV`
3. Salvesta fail kausta `raw/`

📁 Näide: `log_18.10.2025.csv`
