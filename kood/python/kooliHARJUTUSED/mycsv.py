filename = 'DATA/Create-MyCSV-v.csv'
column = 0 # Veerg mida kokku liita
column = 2 # Veerg mida kokku liita
total = 0 # Veeru summa

with open(filename, 'r') as f:
    contents = f.readlines() # Loeme faili sisu muutujasse
    print(contents) # Prindime faili sisu
    for line in contents: # Rea kaupa läbi käimine
        line = line.strip() # Eemalda tühikud ja reavahetuse. Peab tõstma TABiga edasi!
        parts = line.split(';') # Tükelda semikoolonist   
        if parts[column].isdigit(): # Kas kõik on numbrid
            total += int(parts[column]) # Liida number juurde
    print(total) # Tulemus