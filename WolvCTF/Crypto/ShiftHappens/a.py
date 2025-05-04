# 初期値とフィードバック設定（REDACTED の部分を推測する必要があります）
FEEDBACK = 0b1101011010101101  # 実際の値に置き換えてください
state = 0b1010101010101010     # 実際の初期状態に置き換えてください

L = 16  # LFSRのビット長（16ビット）

# LFSRの次の状態を計算する関数
def next_state(current_state):
    bit = 0
    for i in range(L):
        bit ^= ((current_state >> i) & 1) & ((FEEDBACK >> i) & 1)
    new_state = (current_state << 1) | bit
    return new_state

# ciphertext.txt のビット列をリストに変換
ciphertext = [
    '01111011', '11000101', '10111011', '10110100', '00001111', '00100101', '11111101', '10001101',
    '01011000', '11011000', '01001111', '11100100', '11100110', '11111110', '01101001', '00111101',
    '01100011', '11100100', '00011011', '00010011', '10011111', '11011001', '11111111', '10001100',
    '00011110', '11110010', '01000001', '01010010', '01110000', '11100011', '10110001', '00000101',
    '10111110', '10111011', '10000101', '00001101', '01100111', '01000010', '01011000', '01101101',
    '11110000', '01001011', '11110101', '11000011', '01100000', '11101011', '10100011', '01001101',
    '00010110', '10110110', '11001101', '10000111', '01010110', '01010010', '01111110', '11101011',
    '01010101', '01000010', '00000011', '10001001'
]

# ciphertextをビット列に変換
ciphertext_bits = [int(b) for bit in ciphertext for b in bit]

# bitstreamを生成する
bitstream = []
for i in range(60 * 8):  # フラグは60文字なので、60*8ビット
    bit = (state >> 15) & 1  # 最上位ビットを取り出す
    bitstream.append(bit)
    state = next_state(state)

# フラグを復号する
flag_bits = []
for i in range(60 * 8):
    decrypted_bit = ciphertext_bits[i] ^ bitstream[i]  # XOR演算
    flag_bits.append(decrypted_bit)

# 復号されたビット列を文字に変換
flag = ''
for i in range(0, len(flag_bits), 8):
    byte = flag_bits[i:i + 8]
    byte_value = int(''.join(str(b) for b in byte), 2)
    flag += chr(byte_value)

print("Recovered Flag:", flag)
