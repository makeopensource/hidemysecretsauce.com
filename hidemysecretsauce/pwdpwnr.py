import itertools
import string
from database import users 
import sys
import hashlib


# takes username and charset as command line arguments.

def pwn_pwd(charset, log=False):
    i = 0
    for n in range (1, 5):
        for guess in itertools.product(charset, repeat=n):
            guess = "".join(guess)
            hashed_guess = hashlib.sha256(guess.encode()).hexdigest()
            i += 1   
            print(f'Guessing {guess}')
            if hashed_guess == userhash:
                print(f'Password: {guess}')
                exit()


if __name__ == '__main__':
    user = sys.argv[1]
    charset = None
    if len(sys.argv) == 3:
        charset = sys.argv[2]
    userhash = users.find_one({'username': user})["password"]
    if charset is None: pwn_pwd(string.printable)
    elif charset == '1': pwn_pwd(string.ascii_letters)
    elif charset == '2': pwn_pwd(string.digits)
    elif charset == '3': pwn_pwd(string.printable)
    else: print('Invalid charset')
