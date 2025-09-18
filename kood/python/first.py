# Import
from datetime import datetime

name = 'heiki rebane' # String ehk sõne
age = 25 # Täisarv (integer)
height = 1.79 # ujukomaarv (float)

print(name, age, height) # Väljasta kolm väärtust
# Kasutaja heiki rebane vanuses 25 aastat ja pikkusega 1.79 meetrit istub laua taga
print(f'Kasutaja {name.title()} vanuses {age} ja pikkusega {height} meetrit istub laua taga')
print('Kasutaja ' + name.title() + ' vanuses ' + str(age) + ' ja pikkusega ' + str(height) + ' meetrit istub laua taga ') # + märk tuleb ka ikka vahele panna kui on probleem!

#Arvutamine
birth_year = datetime.now().year - age # Jooksev aasta - vanus
print(birth_year)

name = name.title() # Korrasta nimi ja kasuta sama muutujat
print(name[1])       # Väljund: e
print(name[1:5])     # Väljund: "eiki"
print(name[6:])      # Väljund: Rebane
print(name[:5])      # Väljund: Heiki
print(name[::-1])    # Väljund: enaber ikieH

age = input('Sisesta vanus: ')
age= int(age)
if age < 1 or age > 122:
     print('Vanus on vales vahemikus (Lubatud on 1-122)')
elif age < 18:
    print('Alaealine') 
elif age < 65:
    print('Tööealine')
elif age < 100:
    print('Pensionär') 
else:
    print('Pikaealine')      

place = input('Sisesta elukoht: ')
print(f'Sisestati: {place}')

if len(place) > 1 and len(place) <= 7:
    print(f'Lühikese nimega koht {place.title()}')
elif len(place) > 7:
    print(f'Pika nimega koht {place.title()}')
else:
    print('Nimi liiga lühike.')       