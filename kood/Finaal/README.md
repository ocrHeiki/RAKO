# ITSK25 Skriptimise lõputöö

See projekt sisaldab kahte omavahel seotud skripti:
1. **PowerShell skript** – tekitab juhuslike arvudega maatriksi ja salvestab selle faili `output.txt`
2. **Python skript** – loeb sama faili ning arvutab ridade ja veergude summad ning leiab suurima ja väikseima arvu

---

## 🧩 Ülesande kirjeldus

Eesmärk: õppida kasutama **kahte erinevat skriptimiskeelt (PowerShell ja Python)**, et need töötaksid koos.

**Töövoog:**
1. PowerShelli skript **genereerib andmeid** (juhuslikud arvud, salvestab faili)
2. Python skript **analüüsib andmeid** (loeb faili ja arvutab summad)

---

## ⚙️ 1. PowerShell skript – *andmete generaator*

**Failinimi:** `ITSK25_Heiki_generator.ps1`

```powershell
# ITSK25_Heiki_generator.ps1
# Loob juhuslike numbritega maatriksi ja salvestab faili 'output.txt'
# Autor: ocrHeiki

do {
    $suurus = Read-Host "Sisesta maatriksi suurus (3–10)"
} while ([int]$suurus -lt 3 -or [int]$suurus -gt 10)

$maatriks = @()
for ($i = 0; $i -lt $suurus; $i++) {
    $rida = @()
    for ($j = 0; $j -lt $suurus; $j++) {
        $arv = Get-Random -Minimum 1 -Maximum 100
        $rida += ("{0:D2}" -f $arv)
    }
    $maatriks += ,$rida
}

$outFile = "output.txt"
$maatriks | ForEach-Object { ($_ -join " ") } | Set-Content $outFile

Write-Host "Maatriks suurusega ${suurus}x${suurus} salvestatud faili 'output.txt'."
Write-Host "`nFaili sisu:"
Get-Content $outFile
```

---

### 🧱 **Selgitused PowerShelli koodist**

| Koodiosa | Selgitus |
|-----------|-----------|
| `$suurus = Read-Host "..."` | Küsib kasutajalt sisendi (maatriksi suuruse). |
| `do { ... } while (...)` | Tsükkel, mis kordab küsimist, kuni sisestatakse korrektne väärtus (3–10). |
| `$maatriks = @()` | Loob tühja **massiivi**, kuhu hiljem lisatakse read (nagu tühjad karbid). |
| `$rida = @()` | Loob uue tühja rea, kuhu lähevad arvud. |
| `Get-Random -Minimum 1 -Maximum 100` | Genereerib juhusliku arvu 1 kuni 99. |
| `("{0:D2}" -f $arv)` | Vormindab numbri kahekohaliseks (nt 01, 09, 45). |
| `$rida += ...` | Lisab uue arvu rea lõppu. |
| `$maatriks += ,$rida` | Lisab loodud rea maatriksi lõppu. |
| `$outFile = "output.txt"` | Määrab faili nime, kuhu andmed salvestatakse. |
| `Set-Content` | Kirjutab andmed faili. |
| `Get-Content $outFile` | Kuvab faili sisu konsoolis. |
| `` `n `` | Tähistab uut rida (line break). Sama nagu Pythoni `\n`. |

---

### 💾 Tulemus (näide)

Fail `output.txt`:
```
07 23 55 90
02 99 01 40
33 78 45 05
10 56 22 81
```

---

## 🐍 2. Python skript – *andmete analüsaator*

**Failinimi:** `ITSK25_Heiki_analyys.py`

```python
# ITSK25_Heiki_analyys.py
# Loeb faili 'output.txt' ja arvutab ridade ja veergude summad
# Autor: ocrHeiki

import os

if not os.path.exists("output.txt"):
    print("Faili 'output.txt' ei leitud! Käivita esmalt PowerShelli skript andmete loomiseks.")
    exit()

with open("output.txt", "r") as fail:
    read_lines = fail.readlines()

maatriks = []
for rida in read_lines:
    numbrid = [int(x) for x in rida.split()]
    maatriks.append(numbrid)

print("Maatriks failist:\n")
for rida in maatriks:
    print(" ".join(f"{num:02d}" for num in rida))

print("\nReasummad:")
for i, rida in enumerate(maatriks):
    print(f"Rida {i+1}: {sum(rida)}")

print("\nVeerusummad:")
for j in range(len(maatriks[0])):
    veeru_summa = sum(maatriks[i][j] for i in range(len(maatriks)))
    print(f"Veerg {j+1}: {veeru_summa}")

kõik_numbrid = [num for rida in maatriks for num in rida]
print(f"\nSuurim number: {max(kõik_numbrid)}")
print(f"Väikseim number: {min(kõik_numbrid)}")
```

---

### 🧠 **Selgitused Pythoni koodist**

| Koodiosa | Selgitus |
|-----------|-----------|
| `import os` | Impordib mooduli, mis võimaldab kontrollida, kas fail eksisteerib. |
| `if not os.path.exists("output.txt"):` | Kontrollib, kas fail `output.txt` on olemas. Kui ei ole, annab teate ja lõpetab töö. |
| `with open("output.txt", "r") as fail:` | Avab faili lugemiseks (`r` = read). |
| `read_lines = fail.readlines()` | Loeb kõik read korraga listi. |
| `maatriks = []` | Loob tühja listi (nagu kast, kuhu lähevad kõik read). |
| `for rida in read_lines:` | Käib iga rea faili sees ükshaaval läbi. |
| `rida.split()` | Jagab rea arvudeks tühiku järgi. |
| `int(x)` | Muudab tekstina oleva arvu pärisarvuks. |
| `maatriks.append(numbrid)` | Lisab ühe rea (listi) maatriksi lõppu. |
| `print("Maatriks failist:\n")` | Kuvab teksti ja `\n` tähendab uut rida (newline). |
| `for i, rida in enumerate(maatriks):` | Käib iga rea läbi ja annab neile järjekorranumbri (1, 2, 3...). |
| `sum(rida)` | Arvutab rea kõigi arvude summa. |
| `len(maatriks[0])` | Tagastab, mitu elementi on esimeses reas (ehk mitu veergu). |
| `sum(maatriks[i][j] for i in range(...))` | Arvutab ühe veeru summa kõigist ridadest. |
| `max(kõik_numbrid)` | Leiab suurima arvu maatriksist. |
| `min(kõik_numbrid)` | Leiab väikseima arvu. |
| `f"{num:02d}"` | Vormindab numbri kahekohaliseks (nt 03, 45, 99). |

---

### 📊 Python skripti näidistulemus

```
Maatriks failist:

07 23 55 90
02 99 01 40
33 78 45 05
10 56 22 81

Reasummad:
Rida 1: 175
Rida 2: 142
Rida 3: 161
Rida 4: 169

Veerusummad:
Veerg 1: 52
Veerg 2: 256
Veerg 3: 123
Veerg 4: 216

Suurim number: 99
Väikseim number: 01
```

---

## 📁 Projekti struktuur

```
ITSK25_Skriptimine/
│
├── ITSK25_Heiki_generator.ps1    # PowerShelli skript (andmete generaator)
├── ITSK25_Heiki_analyys.py       # Pythoni skript (andmete analüsaator)
├── output.txt                    # Tekstifail, kuhu PowerShell salvestab maatriksi
└── README.md                     # Käesolev juhend koos seletustega
```

---

## 🔗 Samm-sammuline kasutus

1. Ava PowerShell ja käivita:
   ```powershell
   .\ITSK25_Heiki_generator.ps1
   ```
   → vali maatriksi suurus (nt 5)  
   → fail `output.txt` tekib kausta  

2. Seejärel ava Python ja käivita:
   ```bash
   python ITSK25_Heiki_analyys.py
   ```

---

## 🧠 Mida see töö õpetab

- Failide **loomist ja lugemist** erinevates keeltes  
- **Andmete vormindamist** ja konsooliväljundi kujundamist  
- **Muutujate ja tsüklite** kasutamist  
- **Listide ja massiivide** tööpõhimõtteid (append, for-tsükkel, len, sum, max, min)  
- Kuidas **kahe skriptimiskeele** vahel andmeid vahetada (faili kaudu)

---

## ✍️ Autor

**Nimi:** ocrHeiki  
**Õpperühm:** ITSK25  
**Kool:** Raplamaa Rakenduslik Kolledž  
**Kontakt:** [ocrHeiki @ GitHub](https://github.com/ocrHeiki)

---

Materjalid koostatud õppimise eesmärgil (Skriptimise lõputöö, RAKO ITSK25).
