## trippple

出力からフラグを復元してください🐍
```
import os
from Crypto.Util.number import getPrime, bytes_to_long

m = bytes_to_long(os.getenv("FLAG").encode())
p = getPrime(96)
n = p * p * p
e = 65537
c = pow(m, e, n)

print(f"{n,c=}")
```
```
出力:
n,c=(272361880253535445317143279209232620259509770172080133049487958853930525983846305005657, 69147423377323669983172806367084358432369489877851180970277804462365354019444586165184)
```
公開鍵nが素数pの3乗(p^3)で構成されているのが特徴

解法
>- p を求める
n は p^3 なので、立方根を取ることでpを求める。
>- 秘密指数dを計算
RSAの秘密指数dはeの逆元であり、オイラー関数 φ(n) = p^2 * (p - 1) を用いて計算。
>- 復号する (m = c^d mod n)

```
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
```
```
$ python3 tripple.py 
Alpaca{h1t&4w4y_k4nzum3}
```

### Flag
`Alpaca{h1t&4w4y_k4nzum3}`
