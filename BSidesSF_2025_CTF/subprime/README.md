# subprime

Rivest, Shamir, and Adleman think they have it all figured out, don't they?

cipher.txtとpublikeypair.txtが与えられます

RSA暗号です

## solution

1. 素因数分解によって n の素因数 p と q を見つけ、秘密鍵 d を計算して暗号文を復号する
2. オイラーのトーシェント関数の計算ϕ(n)=(p−1)×(q−1)
p = 9883 と q = 9973 で、計算して得られる値は φ(n) = 98543304
3. 秘密鍵 d を計算する d×e≡1 (mod ϕ(n))
Pythonの mod_inverse を使用

solve.py
```
from sympy import mod_inverse

# 公開鍵情報
e = 1009
n = 98563159

# 素因数p, q (手動で見つけた値)
p = 9883
q = 9973

# φ(n) の計算
phi_n = (p - 1) * (q - 1)

# 公開鍵eに対する秘密鍵dを計算 (逆元)
d = mod_inverse(e, phi_n)

# 与えられた暗号文
ciphertext = [
    23637004, 83925846, 2209113, 27583995, 30323096, 31771886, 30323096, 
    75901128, 31771886, 53482472, 97809030, 69683388, 68450410, 39905961, 
    75846723, 75901128, 53482472, 56293282, 69683388, 68450410, 63432789, 
    9450820, 81966837
]

# 復号処理
def rsa_decrypt(c, d, n):
    return pow(c, d, n)

# 復号文をASCIIに変換
plaintext = ''.join(chr(rsa_decrypt(c, d, n)) for c in ciphertext)

print("Plaintext:", plaintext)
```

出力
```
$ python3 solve.py 
Plaintext: CTF{n0n_0pt!m@l_pR!m3$}
```

## flag

`CTF{n0n_0pt!m@l_pR!m3$}`