def welcome():
    """Väljastab staatilise tervitus teksti."""
    print("Tere, kuidas läheb!")

def welcome_name(name):
    """Tagastab tervituse koos nimega."""
    return f'Tere, {name}! ' 

def division(number1, number2):
    """Tagastab kahe arvu jagamise.
    
    Args:
        number1 (float): Jagatav arv
        number2 (float): Jagaja (ei tohi olla null)
        
    Returns:
        float: Jagatise väärtus
    """
    if number2 != 0:
        return number1 / number2
    return -1


def introduction(name, age = 25):
    """Loob lihtsa tutvustava lause.
    
    :param name: Inimese nimi
    :type name: str
    :param age: Inimese vanus (vaikimisi 25)
    :type age: int, valikuline
    :return: Tektsiline tutvustus vormis 
            'Tema on <nimi> ja ta on <vanus> aastane.'
    :rtype: str
    """
    return f'Tema on {name} ja ta on {age} aastane.'



welcome()

print(welcome_name('Heiki'))


kukimuki = welcome_name('KukiMuki')
print(kukimuki)

a = 10
b = 5
print(division(a, b))
print(division(b, 0))
print(division(b, 0))
print()
print(introduction('Heiki'))
print(introduction('KukiMuki', 30))

"""ÜLESANNE: Loo list viie nimega. Väljasta viie nime tervitus."""

names = ['Heiki', 'KukiMuki', 'Juku', 'Mari', 'Peeter'] 
for name in names:
    print(welcome_name(name))
    