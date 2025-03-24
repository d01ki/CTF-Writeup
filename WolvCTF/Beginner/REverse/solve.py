def caesar_decrypt(ciphertext, shift):
    # シーザー暗号の復号化（指定したシフト分）
    decrypted_text = ''.join(
        [chr(((ord(c) - 32 - shift) % 95) + 32) if 32 <= ord(c) <= 126 else c for c in ciphertext]
    )
    return decrypted_text

def brute_force_caesar(ciphertext):
    # すべてのシフトを試して復号化
    for shift in range(1, 95):  # 1から94までのシフトを試す（ASCII 32〜126の範囲）
        decrypted = caesar_decrypt(ciphertext, shift)
        print(f"Shift {shift}: {decrypted}")

# 混ぜ合わせたフラグ（例: "t`qcxo0s0o2.kd\\.k\\o0s0o20z"）
ciphertext = "t`qcxo0s0o2.kd\\.k\\o0s0o20z"

# 総当たり
brute_force_caesar(ciphertext)
