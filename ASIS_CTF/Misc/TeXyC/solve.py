#!/usr/bin/env python3
# ASIS CTF - TeXyC solver
# Full reimplementation of the TeX hash logic

import itertools
import sys
from multiprocessing import Pool, cpu_count

# --- Constants from TeX ---
POLY_H = 60856
POLY_L = 33568
HIGH_BIT = 32768

TARGETS = [
    "C1D196B1",
    "9D074ADB",
    "B544E197",
    "62A95FFA",
    "50BEDB0E",
    "7D4BC107",
    "1B4CD08A",
    "AFD9830C",
]

# Tuned charset for CTF flags
CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}_"

# --- TeX logic reimplementation ---

def calc_ctf(a, b):
    # XOR in GF(2) - polynomial arithmetic
    res = 0
    mul = 1
    while a != 0 or b != 0:
        bit = (a & 1) ^ (b & 1)
        a >>= 1
        b >>= 1
        if bit:
            res += mul
        mul <<= 1
    return res & 0xFFFF

def asis_bitstep(H, L):
    do_poly = (L & 1) == 1
    carry = (H & 1) == 1

    H >>= 1
    L >>= 1

    if carry:
        L += HIGH_BIT

    if do_poly:
        H = calc_ctf(H, POLY_H)
        L = calc_ctf(L, POLY_L)

    return H & 0xFFFF, L & 0xFFFF

def process_byte(H, L, byte):
    L = calc_ctf(L, byte)
    for _ in range(8):
        H, L = asis_bitstep(H, L)
    return H, L

def compute_hash(s):
    H = 0xFFFF
    L = 0xFFFF

    for c in s:
        H, L = process_byte(H, L, ord(c))

    H = calc_ctf(H, 0xFFFF)
    L = calc_ctf(L, 0xFFFF)

    return f"{H:04X}{L:04X}"

# --- Brute force solver ---

def find_match(args):
    target, charset_subset = args
    for cand in charset_subset:
        s = "".join(cand)
        if compute_hash(s) == target:
            return s
    return None

def solve_target(target):
    """Solve a single target hash"""
    print(f"[*] Solving chunk for {target} ...")
    
    # Generate all combinations
    batch_size = 10000
    combinations = itertools.product(CHARSET, repeat=4)
    
    for cand in combinations:
        s = "".join(cand)
        if compute_hash(s) == target:
            print(f"[+] {target} -> {s}")
            return target, s
    
    print(f"[!] No match found for {target}")
    return target, None

def main():
    results = {}

    for target in TARGETS:
        target_hash, result = solve_target(target)
        if result is None:
            print(f"[!] Failed to find match for {target_hash}")
            sys.exit(1)
        results[target_hash] = result

    flag = "".join(results[t] for t in TARGETS)
    print("\n=== FLAG ===")
    print(flag)

if __name__ == "__main__":
    main()
