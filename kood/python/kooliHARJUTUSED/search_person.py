import csv 

filename = 'DATA/Persons.csv'

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
              
else:
    print('Otsitav fraas on liiga lühike!')