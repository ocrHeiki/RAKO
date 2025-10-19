# 📘 SOC Terminid ja Seletused

## Threat/Content Name
Näitab tuvastatud rünnaku tüüpi või sisutüüpi.

Näide: `Nmap Scan $$94318$$` – threat-id on ID 94318

## Severity
Ohutaseme tase:
- low – infohankimine (nt portide skaneerimine)
- medium – sisemine rünnak (nt brute force)
- high – sisemine oht (nt root exploit)
- critical – väline IP ründab sisemist süsteemi

## Action
- **alert** – märgitud, aga lubatud
- **deny** – blokeeritud
- **drop** – ignoreeritud
- **reset-both** – TCP ühendus katkestatud

## Repeat Count
Mitu korda sama threat esines. Kui >100, siis sageli valepositiiv.

## Valepositiiv
Ei ole tegelik oht, pigem moonutus või tehniline viga.

## SOC L1 – L3
- **L1** – esmastöötlus, logide vaatamine
- **L2** – süvendatud analüüs, threati liigitamine
- **L3** – protokollide süvianalüüs, threat hunting

## Threat-ID
Palo Alto unikaalne number threatile.
