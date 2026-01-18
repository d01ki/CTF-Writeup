from pwn import *
import re

context.log_level = 'info'

# xor_tsuku_shift の実装と同じ
class xor_tsuku_shift:
    def __init__(self, seed):
        self.a = seed

    def shift(self):
        self.a ^= (self.a << 17) & 0xFFFFFFFFFFFFFFFF
        self.a ^= (self.a >> 9) & 0xFFFFFFFFFFFFFFFF
        self.a ^= (self.a << 18) & 0xFFFFFFFFFFFFFFFF
        return self.a & 0xFFFFFFFFFFFFFFFF

# じゃんけんで勝つ手を返す
def win_hand(tsukushi_hand):
    return (tsukushi_hand + 1) % 3

# Tsukushiの手を決定するロジック（問題によると shift() % 3）
def get_hand(val):
    return val % 3

# サーバ接続
io = remote("challs.tsukuctf.org", 30057)

# 冒頭メッセージをスキップ
for _ in range(3):
    io.recvline()

# Round 0 まで読み込み
line = io.recvuntil(b"Go!").decode()

# 入力を適当に与えてTsukushiの最初の手を観測
io.sendline(b"0")  # グー
result_line = io.recvline().decode()

# Draw だったら Tsukushi も 0（Rock）
# You win なら Tsukushi = 2（Scissors）
# You lose なら Tsukushi = 1（Paper）

if "Draw" in result_line:
    first_hand = 0
elif "win" in result_line:
    first_hand = 2
elif "lose" in result_line:
    first_hand = 1
else:
    log.error("Couldn't parse the result from server.")

# 64bitシード総当り（下位16bit固定などで高速化も可能）
log.info("Brute-forcing seed...")

for seed in range(0, 1 << 20):  # 範囲は調整可
    rng = xor_tsuku_shift(seed)
    first = get_hand(rng.shift())
    if first == first_hand:
        log.success(f"Found seed: {hex(seed)}")
        break
else:
    log.error("Seed not found.")
    exit()

# 改めて再接続
io.close()
io = remote("challs.tsukuctf.org", 30057)

# 再び冒頭スキップ
for _ in range(3):
    io.recvline()

# 本番開始
for challenge in range(300):
    line = io.recvline().decode()
    print("[DEBUG] recvline:", repr(line))  # これ追加
    if "tries" not in line:
        break


    rng = xor_tsuku_shift(seed)  # 各チャレンジごとにPRNGは初期化されている想定

    for round in range(294):
        io.recvuntil(b"Go!")
        tsukushi_val = rng.shift()
        tsukushi_hand = get_hand(tsukushi_val)
        you = win_hand(tsukushi_hand)
        io.sendline(str(you).encode())

        response = io.recvline().decode()
        print(f"[>] You: {you}, Tsukushi: {tsukushi_hand}")

        if "Draw" in response or "lose" in response:
            break

        # "Let's go to the next round!" を消費
        if round != 293:
            io.recvline()

    # 294回勝てた場合
    else:
        print(io.recvall().decode())
        break
