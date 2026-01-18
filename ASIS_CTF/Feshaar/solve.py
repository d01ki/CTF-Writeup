data = open("flag.fshr", "rb").read()

candidates = []

# 2通りの8bit化（下位 / 上位）
streams = {
    "low":  bytes(data[i]   for i in range(0, len(data), 2)),
    "high": bytes(data[i+1] for i in range(0, len(data), 2)),
}

def score_printable(bs):
    return sum(32 <= b <= 126 for b in bs)

for name, raw in streams.items():
    for k in range(256):
        # XOR
        out_xor = bytes((b ^ k) for b in raw)
        # ADD / SUB
        out_add = bytes((b - k) & 0xff for b in raw)
        out_sub = bytes((b + k) & 0xff for b in raw)

        for mode, out in [("xor", out_xor), ("add", out_add), ("sub", out_sub)]:
            # printable率が高いものだけ残す
            if score_printable(out) > len(out) * 0.7:
                candidates.append((name, mode, k, out))

# 結果表示（先頭だけ）
for name, mode, k, out in candidates[:20]:
    print(f"[{name}][{mode}][key={k}]")
    print(out[:200])
    print("-" * 40)
