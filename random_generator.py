import random
import string

def generateRandomString():
    characters = ""
    characters += string.ascii_letters
    characters += string.digits
    
    key = ""
    for i in range(3):
        random_char = random.choice(characters)
        key += random_char
    return key

random_key = generateRandomString()
print(random_key)