# Ülesanne:
# Programm, mis genereerib 20 juhuslikku täisarvu (1–100), salvestab need koos kuupäevaga faili, adndmed.txt
# Loeb need uuesti failist tagasi, arvutab summa, keskmise ja suurima arvu ning kuvab tulemused.
# Kirjutan funktsioonile dokumentatsiooni

import random                       # Toob sisse mooduli juhuslike arvude genereerimiseks
from datetime import datetime       # Toob sisse kuupäeva ja kellaaja funktsioonid
from zoneinfo import ZoneInfo       # Võimaldab määrata ajavööndi (nt Eesti aeg)
from pathlib import Path            # Mugav tööriist failide ja kataloogide käsitlemiseks

def analyze_numbers(numbers: list[int]) -> tuple[int, float, int]:  # Loome funktsiooni arvude analüüsimiseks
    """Arvutab arvude summa, keskmise ja maksimumi."""              # Funktsiooni dokumentatsioon
    if not numbers:                                                 # Kontrollime, kas list on tühi
        raise ValueError("Loend ei tohi olla tühi!")                # Kui tühi, viskame veateate
    total = sum(numbers)                                            # Arvutame summa
    average = total / len(numbers)                                  # Arvutame keskmise
    maximum = max(numbers)                                          # Leiame suurima arvu
    return total, average, maximum                                  # Tagastame tulemused

juhuarvud = [random.randint(1, 100) for _ in range(20)]             # Genereerime 20 juhuslikku täisarvu

praegu = datetime.now(ZoneInfo("Europe/Tallinn"))                   # Leiame praeguse kuupäeva ja kella Eesti ajas
aeg_tekstina = praegu.strftime("%d.%m.%Y %H:%M:%S")                 # Vormindame aja loetavaks (dd.mm.yyyy hh:mm:ss)

sisu = [                                                             # Koostame faili sisu kahe rea kujul
    f"Kuupäev: {aeg_tekstina}",                                     # Esimene rida – kuupäev ja kellaaeg
    "Arvud: " + " ".join(str(n) for n in juhuarvud)                 # Teine rida – kõik arvud tühikutega eraldatult
]

failitee = Path("andmed.txt")                                       # Loome faili teekonna (nimi: andmed.txt)
failitee.write_text("\n".join(sisu), encoding="utf-8")              # Kirjutame teksti faili

raw = failitee.read_text(encoding="utf-8").splitlines()             # Loeme faili sisu ja jagame read listiks
arvud_failist = [int(x) for x in raw[1].split(":", 1)[1].strip().split()]  # Võtame teisest reast arvud ja teeme neist int tüüpi numbrid

summa, keskmine, suurim = analyze_numbers(arvud_failist)            # Kasutame funktsiooni tulemuste arvutamiseks

print("Failist loetud arvud:", arvud_failist)                       # Kuvame ekraanile loetud arvud
print(f"Summa: {summa}")                                            # Kuvame summa
print(f"Keskmine: {keskmine:.2f}")                                  # Kuvame keskmise (2 komakohaga)
print(f"Suurim arv: {suurim}")                                      # Kuvame suurima arvu
