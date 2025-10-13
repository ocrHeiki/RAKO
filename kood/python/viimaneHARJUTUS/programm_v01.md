# 📘 Juhuslike arvude analüüsi programm

## 🧾 Ülevaade

See programm:

1. **Genereerib 20 juhuslikku täisarvu** vahemikus 1–100.  
2. **Salvestab need koos kuupäeva ja kellaajaga faili** `andmed.txt`.  
3. **Loeb need uuesti failist tagasi**.  
4. **Arvutab** arvude summa, keskmise ja suurima väärtuse.  
5. **Kuvab tulemused** ekraanile.

---

## 🧭 Andmevoo skeem

```
┌──────────────────────────────────────────────────────────┐
│                 JUHUSLIKE ARVUDE PROGRAMM                │
└──────────────────────────────────────────────────────────┘
                │
                ▼
        [1] Genereeri 20 juhuarvu
                │
                ▼
        [2] Lisa kuupäev ja kellaaeg
                │
                ▼
        [3] Kirjuta fail "andmed.txt"
                │
                ▼
        [4] Loe failist andmed tagasi
                │
                ▼
        [5] Analüüsi (summa, keskmine, suurim)
                │
                ▼
        [6] Kuva tulemused ekraanile
```

---

## 💻 Kood ja samm-sammulised selgitused

### 1. Faili päis (kommentaarid)

```python
# ÜLESANNE:
# Programm, mis genereerib 20 juhuslikku täisarvu (1–100),
# salvestab need koos kuupäevaga faili andmed.txt,
# loeb need uuesti failist tagasi, arvutab summa, keskmise ja suurima arvu ning kuvab tulemused.
# Kirjutan funktsioonile dokumentatsiooni.
#
# Autor: Heiki Rebane - ITSK25
# Kuupäev: 23.09.2025
```

### 2. Vajalikud moodulid

```python
import random                  # Juhuslike arvude genereerimiseks
from datetime import datetime  # Kuupäeva ja kellaaja saamiseks
```

### 3. Funktsioon andmete analüüsimiseks

```python
def analyze_numbers(numbers: list[int]) -> tuple[int, float, int]:
    """Arvutab arvude summa, keskmise ja maksimumi."""
    if not numbers:
        raise ValueError("Loend ei tohi olla tühi!")
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    return total, average, maximum
```

### 4. Juhuarvude loomine

```python
juhuarvud = [random.randint(1, 100) for _ in range(20)]
```

### 5. Kuupäeva ja aja lisamine

```python
praegu = datetime.now()
aeg_tekstina = praegu.strftime("%d.%m.%Y %H:%M:%S")
```

### 6. Andmete salvestamine faili

```python
with open("andmed.txt", "w", encoding="utf-8") as f:
    f.write(f"Kuupäev: {aeg_tekstina}\n")
    f.write("Arvud: " + " ".join(str(n) for n in juhuarvud))
```

### 7. Faili lugemine tagasi

```python
with open("andmed.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()
```

### 8. Arvude eraldamine tekstist

```python
arvud_failist = [int(x) for x in raw[1].split(":", 1)[1].strip().split()]
```

### 9. Arvutuste tegemine ja tulemuste kuvamine

```python
summa, keskmine, suurim = analyze_numbers(arvud_failist)

print("Failist loetud arvud:", arvud_failist)
print(f"Summa: {summa}")
print(f"Keskmine: {keskmine:.2f}")
print(f"Suurim arv: {suurim}")
```

---

## ⚙️ Kokkuvõte

| Etapp | Tegevus | Eesmärk |
|-------|----------|----------|
| 1 | Genereeri arvud | Luuakse 20 juhuslikku täisarvu |
| 2 | Lisa kuupäev | Aja lisamine logimiseks |
| 3 | Salvesta fail | Andmete jäädvustamine |
| 4 | Loe fail | Faili sisu tagasisaamine |
| 5 | Analüüsi | Arvutatakse summa, keskmine ja suurim |
| 6 | Kuva tulemused | Esitatakse lõpptulemus kasutajale |

---

## ✍️ Autor

**Heiki Rebane**  
Rühm: *ITSK25*  
Kuupäev: *23.09.2025*
