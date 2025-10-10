# ITSK25_Heiki_Rebane_analyys.py
# Loeb faili 'output.txt' ja arvutab ridade ja veergude summad
# Autor: ocrHeiki/Heiki Rebane

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
