import os
from Crypto.Util.number import getPrime, bytes_to_long

x = bytes_to_long(os.getenv("FLAG").encode())
for _ in range(42):
    x *= getPrime(42)
print(x)