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
    """modular power : (x**y)%n with x, y et n integers"""
    result = 1
    while y>0:
        if y%2==1:
            result = (result*x)%n
        x = (x*x)%n
        y = y//2
    return result

# prime generators
def prime_generator(lenght=1024):
    A = random.choices(range(0,10), k=lenght)

    # to change the second last digit during the loop n+1 (last digit during the loop n so belongs to [1,3,7,9])
    n1_choice = range(0,10)

    # avoid even cases and multiples of 5 (last digit)
    n0_choice = [1,3,7,9]

    while True:
        # we take the last 1023 digits
        A = A[1:]
        # case where the first digit is '0'
        if A[0] == '0':
            A[0] = random.choice(range(1,10))

        # change last digit and add new one to reach 1024 digits
        A[-1] = random.choice(n1_choice)
        A.append(random.choice(n0_choice))

        a=''
        a = ''.join(map(str,A))
        # be careful : variable 'a' is a String

        p = int(a)
        # p is an integer

        # check if p is prime number
        command = 'openssl prime '
        r = subprocess.run(command + a, shell=True,stdout=subprocess.PIPE)
        result = r.stdout

        match = re.search(rb'not', result) # return True if 'not' is in the result
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
    d = modinv(e, phi_n)
    if not d:
        #this case will not appear as long as e is Fermat number
        return None
    return n, d, e

def encrypt(message: str, n: int, e=65537):
    #c = m^e mod n
    i = 1
    m = 0
    for letter in message:
        m += ord(letter) * i
        i *= 256
    c = lpowmod(m, e, n)
    return c

def decrypt(cipher: int, n: int, d):
    uncipher = lpowmod(cipher, d, n)
    message = ''
    while uncipher != 0:
        number = uncipher % 256
        message += chr(number)
        uncipher = uncipher // 256
    return message