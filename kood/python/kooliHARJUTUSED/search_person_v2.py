filename = 'DATA/Persons.csv'
total = 0 

phrase = input('Sisesta otsitav fraas (min. 2 märki): ')

if len(phrase.strip()) > 1:
    phrase = phrase.strip().lower() # Korrasta otsingu fraas
    f = open(filename, 'r', encoding='utf-8') # Avame faili lugemiseks
    contents = f.readlines()[1:] # Alates teisest reast
    f.close()   # Sulgeme faili
    for line in contents: # Rea kaupa läbi käimine
        line = line.strip() # Korrasta rida (eemalda reavahetus reast \n)
        if phrase in line.lower(): # Kui fraas on reas
            print(line) #Väljasta rida
            total += 1 # Suurenda loendurit
    print(f'Leiti {total} nime.') #Leitud ridade/nimede arv
else:
    print('Otsitav fraas on liiga lühike!')