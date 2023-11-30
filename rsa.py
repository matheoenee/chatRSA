# file for generate RSA keys, encryption function and decryption function

# how to generate propre p and q ? (see https://fr.wikipedia.org/wiki/Chiffrement_RSA)

# fast exponentiation algorithm (to compute (m^e mod n) and (c^d mod n))

# encryption function (how to manage the fact the m > n? How to "split" m?)

# decryption function

<<<<<<< HEAD
import random
import subprocess
import re

def prime_generator(lenght=1024):
    A = random.choices(range(0,10), k=1024)
    n1_choice = range(0,10)
    n0_choice = [1,3,7,9]
    while True:
        #A est une liste de 1024 chiffres, dont le dernier est 1,3,7 ou 9
        A = A[1:]
        A[-1] = random.choice(n1_choice)
        A.append(random.choice(n0_choice))

        a=''
        #a est le nombre en str
        a = ''.join(map(str,A))

        #p est un nombre a 1024 chiffres
        p = int(a)

        #vérifions si p est premier
        command = 'openssl prime '
        r = subprocess.run(command + a, shell=True,stdout=subprocess.PIPE)
        result = r.stdout

        match = re.search(rb'not', result)
        if not match:
            return p
=======
# test commit matheo
>>>>>>> a38ee4d13009b8ab2d649c1afc29f518b3a6c369
