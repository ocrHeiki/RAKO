def welcome():
    """Väljastab staatilise tervitus teksti."""
    print("Tere, kuidas läheb!")

def welcome_name(name):
    """Tagastab tervituse koos nimega."""
    return f'Tere, {name}! ' 

welcome()

print(welcome_name('Heiki'))


kukimuki = welcome_name('KukiMuki')
print(kukimuki)