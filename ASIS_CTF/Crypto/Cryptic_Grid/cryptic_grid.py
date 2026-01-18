#!/usr/bin/env python3

from Crypto.Cipher import AES
from random import *
import os, sys
from flag import flag

key = None
MAX_ATTEMPTS = 0b101010

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.buffer.readline().strip()

def wrap(data, mode=True):
	try:
		c = AES.new(key, AES.MODE_ECB)
		if mode:
			return c.encrypt(int(data).to_bytes(0x10, "big")).hex()
		else:
			return int.from_bytes(c.decrypt(bytes.fromhex(data)), "big")
	except Exception:
		return None

def build_grid(core):
	global key
	key = os.urandom(16)
	return {wrap(i): wrap(core[i]) for i in range(0x40)}

def main():
	border = "┃"
	pr('┏' + '━' * 47 + '┓')
	pr(border, "  .::  THE CRYPTIC GRID OF HIDDEN PATHS  ::. ", border)
	pr(border, "  Echoes in the void reveal faint traces...  ", border)
	pr('┗' + '━' * 47 + '┛')

	core = list(range(0x40))
	shuffle(core)
	core = bytes(core)

	focus = randint(0, 0x3F)
	attempts = MAX_ATTEMPTS
	grid = build_grid(core)

	while MAX_ATTEMPTS >= attempts > 0:
		pr(border, f"Attempts: {attempts}")
		pr(border, "[C]heck [Q]uery [R]eflect [S]hift e[X]it")
		cmd = sc().decode().lower()

		if cmd == "s":
			attempts -= 1
			focus = (focus * 5 + 3) & 0x3F
			pr(border, f"Focus pulse: {focus}")

		elif cmd == "q":
			attempts -= 1
			pr(border, "Entry (hex):")
			entry = sc().decode()
			pr(border, "Delta:")
			delta = int(sc().decode())
			idx = (wrap(entry, False) + delta + 0x20) & 0x3F
			out = grid[wrap(idx)]
			if wrap(out, False) == focus:
				pr(border, f"ALIGNMENT FOUND at {idx}")
				attempts = MAX_ATTEMPTS
				grid = build_grid(core)
			else:
				pr(border, f"Trace: {out}")

		elif cmd == "r":
			attempts -= 8
			pr(border, "Input (hex):")
			inp = sc().decode()[:0x20]
			pr(border, f"Reflection: {wrap(inp, len(inp) < 0x20)}")

		elif cmd == "c":
			pr(border, "Core key:")
			die(
				border,
				f"UNLOCKED: {flag}"
				if bytes.fromhex(sc().decode()) == core
				else "REJECTED",
			)
		elif cmd == "x":
			die(border, "Vanishing into the void...")
		else:
			pr(border, "Invalid")
	die(border, "Attempts depleted.")


if __name__ == "__main__":
	main()