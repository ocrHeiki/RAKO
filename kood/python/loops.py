import random


names = ['Mari', 'Anna', 'Villem', 'Jüri']

# Väljasta listis olevad nimed nime kaupa eraldi real.
for name in names:
    print(name)

print() # Tühi rida
# Teistmoodi väljastus
for x in range(len(names)): # x = 0..3
    print(names[x], random.randint(1, 122))
print()
# Lihsad numbrid    
for x in range(1, 5): # 1, 2, 3, 4
    print(x, end=' ')
print('\n') # Kaks tühja rida!

for x in range(0, 10, 2): # Paarisarvud 0..8
    print(x, end=' | ')

print('\n')    

x = 0
while x < len(names):
    print(names[x])
    x += 1 # x = x + 1
print()    

"""
Väljasta listi nimed konsooli iga nimi eraldi real, kuid iga nime ees on järjekorranumber. Järjekorranumber algab 1-st. Korrektne rida on järgmine
1. Mari
2. Anna
3. Villem
4. Jüri

TÄIENDUS: Tee igale nimele juhuslik vanus, kuid kirjuta see vanus listi nimega ages.
Näita tulemust samas for või while loopis. Peale kordust näita nii names, kui ages listi sisu lihtsalt nagu listid.py failis näitasime.

"""
for i in range(len(names)):
    print(f'{i+1}. {names[i]}') # i = 0..3 
print()

ages = []
for i in range(len(names)):
    ages.append(random.randint(1, 100))
    print(f'{i+1}. {names[i]} - {ages[i]} aastat vana.')    