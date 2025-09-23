# 📘 Juhuslike arvude analüüs

## 🎯 Eesmärk
See programm:
1. Genereerib 20 juhuslikku täisarvu vahemikus 1–100.  
2. Salvestab need koos tänase kuupäevaga faili **andmed.txt**.  
3. Loeb arvud failist tagasi.  
4. Kasutab funktsiooni, mis arvutab **summa, keskmise ja suurima arvu**.  
5. Kuvab tulemused ekraanile.  

---

## ⚙️ Kood ja selgitused

### 1. Moodulid (import)
```python
import random
from datetime import datetime
from zoneinfo import ZoneInfo
from pathlib import Path
```

- **`import random`** – võimaldab genereerida juhuarve.  
- **`from datetime import datetime`** – annab kuupäeva ja kellaaja tööriistad.  
- **`from zoneinfo import ZoneInfo`** – määrab ajavööndi (nt Eesti aeg).  
- **`from pathlib import Path`** – mugav viis failidega töötamiseks.  

---

### 2. Funktsioon
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

- **`def`** – funktsiooni loomine.  
- **`numbers: list[int]`** – tüüpide vihje: sisendiks on täisarvude loend.  
- **`-> tuple[int, float, int]`** – tagastab kolm väärtust (summa, keskmine, suurim).  
- **`return`** – funktsioon tagastab väärtused.  

---

### 3. Juhuarvude genereerimine
```python
juhuarvud = [random.randint(1, 100) for _ in range(20)]
```

- Loob 20 juhuslikku täisarvu listi.  
- **`random.randint(1, 100)`** – juhuarv vahemikus 1–100.  
- **`for _ in range(20)`** – kordab 20 korda.  

---

### 4. Kuupäeva vormindamine
```python
praegu = datetime.now(ZoneInfo("Europe/Tallinn"))
aeg_tekstina = praegu.strftime("%d.%m.%Y %H:%M:%S")
```

- **`datetime.now()`** – praegune aeg.  
- **`ZoneInfo("Europe/Tallinn")`** – Eesti ajavöönd.  
- **`strftime`** – muudab aja tekstiks (dd.mm.yyyy hh:mm:ss).  

---

### 5. Faili kirjutamine ja lugemine
```python
failitee = Path("andmed.txt")
failitee.write_text("\n".join(sisu), encoding="utf-8")

raw = failitee.read_text(encoding="utf-8").splitlines()
```

- **`Path("andmed.txt")`** – viitab failile.  
- **`write_text`** – kirjutab faili.  
- **`read_text`** – loeb faili.  
- **`splitlines()`** – jagab read listiks.  

---

### 6. Failist arvude töötlemine
```python
arvud_failist = [int(x) for x in raw[1].split(":", 1)[1].strip().split()]
```

- **`raw[1]`** – võtab faili teise rea.  
- **`.split(":", 1)`** – lõikab rea kaheks (eemaldame "Arvud:").  
- **`.strip()`** – eemaldab liigsed tühikud.  
- **`.split()`** – jagab numbrid listiks.  
- **`int(x)`** – muudab stringid täisarvudeks.  

---

### 7. Tulemuste kuvamine
```python
print("Failist loetud arvud:", arvud_failist)
print(f"Summa: {summa}")
print(f"Keskmine: {keskmine:.2f}")
print(f"Suurim arv: {suurim}")
```

- **`print()`** – kuvab ekraanile.  
- **f-string** – lubab panna muutujaid teksti sisse (`f"..."`).  
- **`{keskmine:.2f}`** – kuvab keskmise kahe komakohaga.  

---

## 📝 Kokkuvõte
Selles programmis kasutasime:
- **import** – moodulite toomiseks  
- **def, return** – funktsioonide loomiseks ja väärtuste tagastamiseks  
- **list comprehension** – listide loomiseks  
- **datetime ja strftime** – kuupäeva vormindamiseks  
- **Path, write_text, read_text** – failidega töötamiseks  
- **string meetodid (split, strip, join)** – teksti töötlemiseks  
- **print + f-string** – tulemuste kuvamiseks  
