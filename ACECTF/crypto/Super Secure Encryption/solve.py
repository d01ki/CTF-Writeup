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