"""
TÄIENDUS: Näita mitu nime leiti. Leiti xx nime."""
import csv 

filename = 'andmeFAILID/Persons.csv'

phrase = input('Sisesta otsitav fraas (min. 2 märki): ')

if len(phrase) > 1:
    with open(filename, 'r', encoding='utf-8') as  f:
        contents = csv.reader(f, delimiter=';')
        for row in contents:
            phrase = phrase.lower() # Tee väiketähtedeks
            first = row[0].lower() # Tee väiketähtedeks eesnimi
            last = row[1].lower() # Tee väiketähtedeks perekonnanimi
            if phrase in first or phrase in last:
                print(';'.join(row)) # Tee list stringiks
                total += 1
    print(f'Leiti {total} nime.')
    
else:
    print('Otsitav fraas on liiga lühike!')
