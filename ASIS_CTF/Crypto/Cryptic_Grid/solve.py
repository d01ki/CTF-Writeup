from pwn import *

# ターゲットサーバーの接続情報
HOST = '65.109.194.105'
PORT = 8080

# LCG定数 (focus = (focus * 5 + 3) & 0x3F)
def get_next_focus(f):
    return (f * 5 + 3) & 0x3F

def get_steps_to(start, target):
    curr = start
    for s in range(64):
        if curr == target:
            return s
        curr = get_next_focus(curr)
    return None

def solve():
    io = remote(HOST, PORT)
    
    core = [None] * 64
    known_indices = set()
    
    # 初回のFocusを取得
    io.sendlineafter(b"exit", b"s")
    io.recvuntil(b"Focus pulse: ")
    curr_focus = int(io.recvline().strip())
    
    while None in core:
        log.info(f"Progress: {64 - core.count(None)}/64 found")
        
        # 現在のキーにおける 0 の暗号化結果を取得 (Cost: 8)
        io.sendlineafter(b"exit", b"r")
        io.sendlineafter(b"Input (hex):", b"0")
        io.recvuntil(b"Reflection: ")
        e0 = io.recvline().strip().decode()
        
        # Alignmentを狙うか、新しい情報を取得するかのループ
        while True:
            # 既に知っている core の値の中に、現在の focus (または数ステップ先) があるか確認
            best_idx = None
            min_steps = 999
            
            for idx, val in enumerate(core):
                if val is not None:
                    steps = get_steps_to(curr_focus, val)
                    if steps < min_steps:
                        min_steps = steps
                        best_idx = idx
            
            # もし現実的なステップ数で Alignment できるなら実行
            # (残り attempts を考慮。ここでは安全策として少なめに見積もる)
            if best_idx is not None and min_steps < 20:
                log.info(f"Targeting known core[{best_idx}] == {core[best_idx]} in {min_steps} steps")
                for _ in range(min_steps):
                    io.sendlineafter(b"exit", b"s")
                    curr_focus = get_next_focus(curr_focus)
                
                # Queryを投げて Alignment 発生
                delta = (best_idx - 32) % 64
                io.sendlineafter(b"exit", b"q")
                io.sendlineafter(b"Entry (hex):", e0.encode())
                io.sendlineafter(b"Delta:", str(delta).encode())
                
                res = io.recvuntil(b"ALIGNMENT FOUND")
                log.success("Alignment reset!")
                # key が変わるため、内側のループを抜けて e0 を取り直す
                break
            
            else:
                # 未知のインデックスを調査 (Cost: q(1) + r(8) = 9)
                target_idx = core.index(None)
                delta = (target_idx - 32) % 64
                
                io.sendlineafter(b"exit", b"q")
                io.sendlineafter(b"Entry (hex):", e0.encode())
                io.sendlineafter(b"Delta:", str(delta).encode())
                io.recvuntil(b"Trace: ")
                trace = io.recvline().strip().decode()
                
                # Traceを復号して core[target_idx] を特定
                io.sendlineafter(b"exit", b"r")
                io.sendlineafter(b"Input (hex):", trace.encode())
                io.recvuntil(b"Reflection: ")
                val = int(io.recvline().strip())
                
                core[target_idx] = val
                log.info(f"Revealed: core[{target_idx}] = {val}")

    # すべて判明したら core を送信
    log.success("Full core recovered!")
    final_core_hex = bytes(core).hex()
    io.sendlineafter(b"exit", b"c")
    io.sendlineafter(b"Core key:", final_core_hex.encode())
    
    # フラグを表示
    print(io.recvall().decode())

if __name__ == "__main__":
    solve()