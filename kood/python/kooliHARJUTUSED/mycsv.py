filename = 'DATA/Create-MyCSV-v.csv'
column = 0 # Veerg mida kokku liita
total = 0 # Veeru summa

with open(filename, 'r') as f:
    contents = f.readlines() # Loeme faili sisu muutujasse
    print(contents) # Prindime faili sisu