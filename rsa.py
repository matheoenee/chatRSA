# file for generate RSA keys, encryption function and decryption function

# how to generate propre p and q ? (see https://fr.wikipedia.org/wiki/Chiffrement_RSA)

# fast exponentiation algorithm (to compute (m^e mod n) and (c^d mod n))

# encryption function (how to manage the fact the m > n? How to "split" m?)

# decryption function

import random
import subprocess
import re

def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
        gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None
    return x % m

def lpowmod(x, y, n):
    """puissance modulaire: (x**y)%n avec x, y et n entiers"""
    result = 1
    while y>0:
        if y&1>0:
            result = (result*x)%n
        y >>= 1
        x = (x*x)%n
        return result

def prime_generator(lenght=1024):
    A = random.choices(range(0,10), k=1024)
    n1_choice = range(0,10)
    n0_choice = [1,3,7,9]
    while True:
        #on récupère les 1023 derniers chiffres
        A = A[1:]
        #gestion du cas où le premier chiffre est 0
        if A[0] == '0':
            A[0] = random.choice(range(1,10))
        #changement du dernier chiffre, puis ajout pour atteindre 1024
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

def RSA_key():
    #choice of e predetermined
    e = 65537
    p = prime_generator()
    q = prime_generator()
    n = p*q
    phi_n = (p-1)*(q-1)
    # d=e⁻¹ mod phi_n
    d = modinv(phi_n, e)
    if not d:
        #this case will not appear as long as e is Fermat number
        return None
    return n, d, e


if __name__ == "__main__":
    print(RSA_key())