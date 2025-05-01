key = 0xab
decrypted = bytearray()

with open("memo.pdf.enc", "rb") as f:
    encrypted = f.read()

for b in encrypted:
    decrypted_byte = b ^ key
    key = b
    decrypted.append(decrypted_byte)

with open("memo_decrypted.pdf", "wb") as f:
    f.write(decrypted)
