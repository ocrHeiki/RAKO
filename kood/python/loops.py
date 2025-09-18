import random


names = ['Mari', 'Jüri', 'Kati', 'Juhan']

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