# 📘 Juhuslike arvude analüüsi programm (täiendatud õppeversioon)

## 🧾 Ülevaade

See Python programm teeb järgmise sammudega töövoo:

1. **Genereerib 20 juhuslikku täisarvu** vahemikus 1–100.  
2. **Salvestab need koos kuupäeva ja kellaajaga** faili `andmed.txt`.  
3. **Loeb andmed failist tagasi**.  
4. **Analüüsib saadud numbreid** (summa, keskmine, suurim).  
5. **Kuvab tulemused** ekraanil.

Programmi eesmärk on õpetada:
- juhuslike arvude loomist (`random` moodul),
- aja käsitlemist (`datetime` moodul),
- failidega töötamist (`open`, `write`, `readlines`),
- andmete töötlemist ja funktsioonide kasutamist.

---

## 🧩 Koodi ülesehitus samm-sammult

### 1. Impordid ehk teekide sissetoomine

```python
import random                  # Juhuslike arvude genereerimiseks
from datetime import datetime  # Kuupäeva ja kellaaja kasutamiseks
```

📘 **Selgitus:**
- `import random` — lubab kasutada Python'i juhuslikke funktsioone (nt `randint()`).
- `from datetime import datetime` — toob sisse ainult `datetime` klassi, et saaks kasutada `datetime.now()` praeguse aja saamiseks.

---

### 2. Funktsioon `analyze_numbers()`

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

#### 💡 Samm-sammuline selgitus:

| Rida | Käsu või sümboli tähendus |
|------|---------------------------|
| `def analyze_numbers(...)` | loob **funktsiooni**, mida saab hiljem kasutada analüüsimiseks. |
| `numbers: list[int]` | tüübiviide — näitab, et sisend on **täisarvude loend**. |
| `-> tuple[int, float, int]` | tüübiviide tagastusele — funktsioon annab tagasi **kolm väärtust**: summa (int), keskmine (float) ja maksimum (int). |
| `if not numbers:` | kontroll, et loend poleks tühi — kui on, visatakse viga (`ValueError`). |
| `sum(numbers)` | sisseehitatud funktsioon, mis liidab kõik arvud kokku. |
| `len(numbers)` | loendite pikkuse leidmine (nt kui 20 arvu, siis tulemus = 20). |
| `max(numbers)` | leiab suurima arvu loendist. |
| `return total, average, maximum` | tagastab kolm väärtust ühes paketis (tuple). |

---

### 3. Juhuslike arvude genereerimine

```python
juhuarvud = [random.randint(1, 100) for _ in range(20)]
```

#### Selgitus:
- `random.randint(1, 100)` → annab **juhusliku täisarvu** 1 ja 100 vahel.  
- `[... for _ in range(20)]` → **list comprehension**, mis kordab seda 20 korda.
- `_` → sümbol tähendab “muutuja, mida ei kasutata”.  
- Tulemus: 20 juhuslikku numbrit ühes loendis, nt:
  ```
  [4, 67, 89, 12, 51, 23, 7, 99, 43, 66, 55, 38, 22, 91, 13, 5, 75, 49, 80, 17]
  ```

---

### 4. Kuupäeva ja aja vormindamine

```python
praegu = datetime.now()
aeg_tekstina = praegu.strftime("%d.%m.%Y %H:%M:%S")
```

#### Selgitus:
- `datetime.now()` → annab **praeguse kuupäeva ja kellaaja**.
- `.strftime()` → muudab kuupäeva **tekstiks (stringiks)** soovitud kujul.

🧮 **Formaadid:**
| Sümbol | Tähendus | Näide |
|--------|-----------|-------|
| `%d` | päev (01–31) | `23` |
| `%m` | kuu (01–12) | `09` |
| `%Y` | aasta (täis) | `2025` |
| `%H` | tund (00–23) | `14` |
| `%M` | minutid | `07` |
| `%S` | sekundid | `32` |

➡️ Näiteks tulemus: `"23.09.2025 14:07:32"`

---

### 5. Faili kirjutamine (`with open`, `f.write`, `join()`)

```python
with open("andmed.txt", "w", encoding="utf-8") as f:
    f.write(f"Kuupäev: {aeg_tekstina}\n")
    f.write("Arvud: " + " ".join(str(n) for n in juhuarvud))
```

#### Selgitus:

| Element | Tähendus |
|----------|-----------|
| `open("andmed.txt", "w", encoding="utf-8")` | avab faili kirjutamiseks (`"w"` = *write mode*). Kui fail on olemas, kirjutatakse see üle. |
| `as f:` | annab failile nime `f`, et saaks seda käsu sees kasutada. |
| `f.write()` | kirjutab teksti faili (ühte ritta või koos `\n` uuele reale). |
| `f"Kuupäev: {aeg_tekstina}\n"` | f-string, mis paneb väärtuse `aeg_tekstina` teksti sisse. |
| `" ".join(str(n) for n in juhuarvud)` | loob kõikidest numbritest ühe pika tekstirea, tühikuga eraldatud. |

🧩 Näide:
```python
" ".join(str(n) for n in [1, 2, 3])
# annab tulemuseks: "1 2 3"
```

Faili sisu näeb välja nii:
```
Kuupäev: 23.09.2025 14:07:32
Arvud: 1 2 3 4 5 6 7 8 ...
```

---

### 6. Failist lugemine (`readlines()`)

```python
with open("andmed.txt", "r", encoding="utf-8") as f:
    raw = f.readlines()
```

#### Selgitus:
| Element | Tähendus |
|----------|-----------|
| `"r"` | avab faili lugemiseks (read mode). |
| `readlines()` | loeb kõik read ja tagastab listina. |
| `raw` | muutujasse salvestatakse ridade nimekiri. |

---

### 7. Arvude eraldamine tekstist (`split`, `strip`, `int()`)

```python
arvud_failist = [int(x) for x in raw[1].split(":", 1)[1].strip().split()]
```

#### Samm-sammuline selgitus:
1. `raw[1]` → võtab **teise rea** failist (seal on arvud).  
2. `.split(":", 1)` → jagab teksti kaheks tükiks: `["Arvud", " 5 10 20 30"]`.
3. `[1]` → võtab **teise osa** (pärast koolonit).
4. `.strip()` → eemaldab liigsed tühikud algusest/lõpust.
5. `.split()` → jagab teksti tühikute järgi sõnadeks.  
6. `[int(x) for x in ...]` → muudab kõik väärtused täisarvudeks.

📘 Tulemus:
```python
[5, 10, 20, 30]
```

---

### 8. Analüüsi funktsiooni kasutamine

```python
summa, keskmine, suurim = analyze_numbers(arvud_failist)
```

Kutsub varem loodud funktsiooni `analyze_numbers()`, mis tagastab kolm väärtust:  
summa, keskmine ja suurim arv.

---

### 9. Tulemuste kuvamine (`print`, f-stringid)

```python
print("Failist loetud arvud:", arvud_failist)
print(f"Summa: {summa}")
print(f"Keskmine: {keskmine:.2f}")
print(f"Suurim arv: {suurim}")
```

#### Selgitus:
| Element | Tähendus |
|----------|-----------|
| `print()` | kuvab andmed ekraanile. |
| `f"Summa: {summa}"` | f-string — väärtus `summa` asendatakse automaatselt. |
| `{keskmine:.2f}` | kuvab **kaks kohta pärast koma** (nt 42.75). |

---

## 📘 Kokkuvõte

| Käsk / Funktsioon | Mida teeb | Näide |
|-------------------|------------|--------|
| `random.randint(a, b)` | Loob juhusliku täisarvu vahemikus a–b. | `random.randint(1,100)` → `57` |
| `datetime.now()` | Tagastab praeguse aja. | `2025-09-23 14:07:32` |
| `.strftime()` | Vormindab aja tekstiks. | `"23.09.2025 14:07:32"` |
| `open(failinimi, "w"/"r")` | Avab faili kirjutamiseks/lugemiseks. |  |
| `f.write()` | Kirjutab teksti faili. | `f.write("Tere!")` |
| `readlines()` | Loeb kõik failiread listina. | `["rida1", "rida2"]` |
| `.split()` | Jagab teksti sõnadeks. | `"1 2 3".split()` → `["1", "2", "3"]` |
| `.join()` | Liidab sõnad kokku üheks tekstiks. | `" ".join(["1","2","3"])` → `"1 2 3"` |
| `int()` | Muudab teksti arvuks. | `int("5")` → `5` |
| `sum()`, `len()`, `max()` | Summa, elementide arv, suurim väärtus. | — |

---

## ✍️ Autor

**Heiki Rebane**  
Rühm: *ITSK25*  
Kuupäev: *23.09.2025*
