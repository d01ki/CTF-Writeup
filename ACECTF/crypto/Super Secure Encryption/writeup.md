## Super Secure Encryption

>I'm doing a big favour with this one... I'm handing out my super secure functionality to the outer world to stumble upon & explore. Though, I still remember one of my colleagues once saying that nothing in this world is secure nowadays but my script right here stands on the contrary. I'll give you the access to my arsenal and see if you can prove me wrong.

```
from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

k = os.urandom(16) # Is it too short?

def encrypt(plaintext):
    cipher = AES.new(k, AES.MODE_CTR, counter=Counter.new(128)) # I was told, CTR can't be broken!
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext.hex()

msg = b'This is just a test message and can totally be ignored.' # Just checking functionality
encrypted_msg = encrypt(msg)

with open('flag.txt', 'r') as f:
    flag = f.readline().strip().encode()

encrypted_flag = encrypt(flag)

with open('msg.txt', 'w+') as o:
    o.write(f"{encrypted_msg}\n")
    o.write(f"{encrypted_flag}")
```
```
# output.txt
d71f4a2fd1f9362c21ad33c7735251d0a671185a1b90ecba27713d350611eb8179ec67ca7052aa8bad60466b83041e6c02dbfee738c2a3
c234661fa5d63e627bef28823d052e95f65d59491580edfa1927364a5017be9445fa39986859a3
```

ソースコードとtxtが与えられる
CTRモードは同じカウンター値で同じ鍵を使うと、暗号文が危険になる脆弱性がある

- 同じカウンターと鍵の使用: 上記のコードでは、同じカウンターと鍵が使用されています。これにより、同じ鍵ストリームが生成されるため、異なるメッセージが同じ場所で同じXOR操作を受ける
- 既知の平文を利用: msg = b'This is just a test message and can totally be ignored.'という既知の平文が暗号化されているので、その暗号文と比較し、鍵ストリームを復号できる

```
#solve.py
from Crypto.Cipher import AES
from Crypto.Util import Counter
import binascii

known_plaintext = b'This is just a test message and can totally be ignored.'
ciphertext_hex = 'd71f4a2fd1f9362c21ad33c7735251d0a671185a1b90ecba27713d350611eb8179ec67ca7052aa8bad60466b83041e6c02dbfee738c2a3'
ciphertext = binascii.unhexlify(ciphertext_hex)

# 鍵ストリームを復号
keystream = bytes([ct ^ pt for ct, pt in zip(ciphertext, known_plaintext)])

# フラグの暗号文を復号
flag_ciphertext_hex = 'c234661fa5d63e627bef28823d052e95f65d59491580edfa1927364a5017be9445fa39986859a3'
flag_ciphertext = binascii.unhexlify(flag_ciphertext_hex)
flag = bytes([fc ^ ks for fc, ks in zip(flag_ciphertext, keystream)])

print(f"The flag is: {flag.decode()}")
```
```
~/ctf/ace-ctf/cry$ python3 solve.py 
The flag is: ACECTF{n07h1n6_15_53cur3_1n_7h15_w0rld}
```
`ACECTF{n07h1n6_15_53cur3_1n_7h15_w0rld}`