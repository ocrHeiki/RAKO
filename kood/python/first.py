# Import
from datetime import datetime

name = 'heiki rebane' # String ehk sõne
age = 25 # Täisarv (integer)
height = 1.79 # ujukomaarv (float)

print(name, age, height) # Väljasta kolm väärtust
# Kasutaja heiki rebane vanuses 25 aastat ja pikkusega 1.79 meetrit istub laua taga
print(f'Kasutaja {name.title()} vanuses {age} ja pikkusega {height} meetrit istub laua taga')
print('Kasutaja ' + name + ' vanuses ' + str(age) + ' ja pikkusega ' + str(height) + ' meetrit istub laua taga ') # + märk tuleb ka ikka vahele panna kui on probleem!

# Las arvuti teeb ise kindlaks mis aasta meil praegu kasutusel on ja lisasime faili algusesse Import
#Arvutamine
birth_year = datetime.now().year - age # Jooksev aasta - vanus
print(birth_year)
