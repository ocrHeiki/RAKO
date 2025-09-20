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

src = 'andmeFAILID/Persons.csv' # Algandmed
dst = 'andmeFAILID/Persons_accounts.csv' # Uus fail
header = 'Eesnimi;Perenimi;Isikukood;Kasutajanimi;Epost' # Uue faili päis
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
    d.write(header + '\n') # Kirjuta päis
    next(contents) # Jäta esimene rida vahele
   
    for row in contents: 
        date = row[2] # Sünniaeg eraldi muutujasse
        year = int(date.split('.')[2]) # Võta aasta sünniajast ja tee täisarvuks
        
        if year >= 1990 and year <= 1999:
            first_name = row[0] #Eesnimi eraldi muutujasse
            last_name = row[1] #Perenimi eraldi muutujasse

            #Eemalda tühik ja sidekriips
            first_name = first_name.replace(' ','')
            first_name = first_name.replace('-','')

            # Kasutajanime loomine
            username = '.'.join([first_name, last_name]).lower()
            username = strip_accents(username) # Eemalda rõhumärgid
              
            # Eposti loomine
            email = username + domain
            # Uue rea loomine
            
            new_line = ';'.join(row[:2]+[row[-1], username, email])
            d.write(new_line + '\n') # Kirjuta uus rida faili

            print(new_line) 