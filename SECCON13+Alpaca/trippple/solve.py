from Crypto.Util.number import long_to_bytes
from sympy import integer_nthroot
from gmpy2 import invert

n = 272361880253535445317143279209232620259509770172080133049487958853930525983846305005657
c = 69147423377323669983172806367084358432369489877851180970277804462365354019444586165184

p, exact = integer_nthroot(n, 3)

e = 65537
phi_n = p*p*(p-1)
d = int(invert(e, phi_n))

m = pow(c, d, n)
flag = long_to_bytes(m)

print(flag.decode())
