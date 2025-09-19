"""
Luua etteantud kasutajate kasutajanimi ja epostiaadress
KASUTAJANIMI:
eesnimi.perenimi
eesnimes eeldada tõhi ja/või sidekriips Mari Liis, Mari-Liis
eemalda rõhumärgid ja täpitähed (ä,ö,ü,õ,š,ž)
kasutajanimi väikeste tähtedega
EPOSTIAADRESS:
kasutajanimi@asutus.com
KELLELE TEHA:
Sündinud 1990-1999 k.a.
UUE FAILI SISU ON:
Eesnnimi, Perenimi, Isikukood, Kasutajanimi, Epost
Eesnimi;Perenimi;Sünniaeg;Sugu;Isikukood <-- ORIGINAAL
"""
import csv
import unicodedata

src = 'DATA/Persons.csv' # Algandmed
dst = 'DATA/Persons_accounts.csv' # Uus fail
header = ['Eesnimi', 'Perenimi', 'Isikukood', 'Kasutajanimi', 'Epost'] # Uue faili päis
domain = '@asutus.com' # Eposti domeen


def strip_accents(s):
   """
   Eemaldab rõhumärgid ja täpitähed
   https://stackoverflow.com/questions/517923/"""
   return ''.join(c for c in unicodedata.normalize('NFD', s) #
                  if unicodedata.category(c) != 'Mn')

with open(src, 'r', encoding='utf-8') as f: # Loetav algfail
   with open(dst, 'w', encoding='utf-8') as d: # Kirjutamiseks uus
      contents = csv.reader(f, delimiter=';') # faili sisu muutujasse
        
