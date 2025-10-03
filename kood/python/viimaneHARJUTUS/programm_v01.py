# ÜLESANNE:
# Programm, mis genereerib 20 juhuslikku täisarvu (1–100),
# salvestab need koos kuupäevaga faili andmed.txt,
# loeb need uuesti failist tagasi, arvutab summa, keskmise ja suurima arvu ning kuvab tulemused.
# Kirjutan funktsioonile dokumentatsiooni.
#
# Autor: Heiki Rebane - ITSK25
# Kuupäev: 23.09.2025

import random                  # Toob sisse mooduli juhuslike arvude genereerimiseks
from datetime import datetime  # Toob sisse kuupäeva ja kellaaja funktsioonid

def analyze_numbers(numbers: list[int]) -> tuple[int, float, int]:
    """Arvutab arvude summa, keskmise ja maksimumi.
    
    Args:
        numbers (list[int]): Arvude loend
    Returns:
        tuple: summa (int), keskmine (float), suurim arv (int)
    """
    if not numbers:
        raise ValueError("Loend ei tohi olla tühi!")
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    return total, average, maximum

# Genereerime 20 juhuslikku täisarvu
juhuarvud = [random.randint(1, 100) for _ in range(20)]

# Leiame praeguse aja
praegu = datetime.now()
aeg_tekstina = praegu.strftime("%d.%m.%Y %H:%M:%S")

# Kirjutame faili
with open("andmed.txt", "w", encoding="utf-8") as f:
    f.write(f"Kuupäev: {aeg_tekstina}\n")
    f.write("Arvud: " + " ".join(str(n) for n in juhuarvud))

# Loeme failist
with open("andmed.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()

# Teisendame teise rea arvud int-tüüpi numbriteks
arvud_failist = [int(x) for x in raw[1].split(":", 1)[1].strip().split()]

# Arvutame tulemused
summa, keskmine, suurim = analyze_numbers(arvud_failist)

# Kuvame ekraanile
print("Failist loetud arvud:", arvud_failist)
print(f"Summa: {summa}")
print(f"Keskmine: {keskmine:.2f}")
print(f"Suurim arv: {suurim}")
