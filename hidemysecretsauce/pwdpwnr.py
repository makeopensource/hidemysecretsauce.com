import itertools
import string
from database import users 
import sys
import bcrypt
import hashlib


# Takes Username as command line arguments.
user = sys.argv[1]
userhash = users.find_one({'username': user})["password"]

print(userhash)

for n in range (1, 5):
    i = 0
    for guess in itertools.product(string.printable, repeat=n):
        guess = "".join(guess)
        hashed_guess = hashlib.sha256(guess.encode()).hexdigest()
        print(guess)
        i += 1
        
        if hashed_guess == userhash:
            print(f'Password: {guess}')
            exit()
