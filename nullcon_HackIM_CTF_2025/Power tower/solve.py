from Cryptodome.Cipher import AES
from Cryptodome.Util import number
from functools import reduce
from math import gcd
from sage.all import *

# n = number.getRandomNBitInteger(256)
n = 107502945843251244337535082460697583639357473016005252008262865481138355040617



def solve(primes, p):
    if len(primes) == 2:
        ret = pow(primes[0], primes[1], p)
    else:
        ret = pow(primes[-1], solve(primes[:-1], euler_phi(Integer(p))), p)
    return int(ret)


primes = [p for p in range(100) if number.isPrime(p)]
int_key = solve(primes, n)

key = int.to_bytes(int_key, 32, byteorder="big")

cipher = bytes.fromhex(open("cipher.txt", "r").read().strip())
flag = AES.new(key, AES.MODE_ECB).decrypt(cipher)
print(flag)