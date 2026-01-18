import string

ciphertext = "ayb wpg uujmz pwom jaaaaaa aa tsukuctf, hj vynj? mml ogyt re ozbiymvrosf bfq nvjwsum mbmm ef ntq gudwy fxdzyqyc, yeh sfypf usyv nl imy kcxbyl ecxvboap, epa 'avb' wxxw unyfnpzklrq."

def f_inv(c, k):
    c = ord(c) - ord('a')
    k = ord(k) - ord('a')
    p = (c - k + 26) % 26
    return chr(ord('a') + p)

def decrypt(ciphertext, known_plaintext_segment, segment_position):
    idx = 0
    plain = []
    cipher_without_symbols = []
    decrypted_key = []

    letters_only = [c for c in ciphertext if c in string.ascii_lowercase]

    for i in range(len(known_plaintext_segment)):
        c = letters_only[segment_position + i]
        p = known_plaintext_segment[i]
        k = (ord(c) - ord(p)) % 26
        k = chr(ord('a') + k)
        decrypted_key.append(k)

    idx = 0
    key = decrypted_key
    for c in ciphertext:
        if c in string.ascii_lowercase:
            if idx < len(key):
                k = key[idx]
            else:
                k = cipher_without_symbols[idx - len(key)]
            p = f_inv(c, k)
            cipher_without_symbols.append(c)
            plain.append(p)
            idx += 1
        else:
            plain.append(c)

    return ''.join(plain), ''.join(decrypted_key)

lower_only = [c for c in ciphertext if c in string.ascii_lowercase]
segment = "tsukuctf"
segment_position = 30  # Based on the assert

plaintext, key = decrypt(ciphertext, segment, segment_position)

print("Recovered key:", key)
print("\nDecrypted plaintext:\n", plaintext)
