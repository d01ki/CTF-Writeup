#!/usr/bin/env python3

from Crypto.Util.number import *
from random import *
from string import *
import sys
from flag import flag

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.buffer.readline().strip()

def random_string(l):
	PRINTABLE = printable[:72]
	return ''.join([choice(PRINTABLE) for _ in range(l)])

def genkey(nbit, D, k):
	e = d = N = 1
	dbit = int(nbit * D) + 1
	while N.bit_length() != nbit and d.bit_length() != dbit:
		p, q = [getPrime(nbit >> 1) for _ in ':)']
		if p % 4 == q % 4 == 3:
			N = p * q
			phi = (p ** k - 1) * (q ** k - 1)
			d = getPrime(dbit)
			r = randint(0, 1)
			e = inverse(phi + (-1)**r * d, phi)
			keypair = (N, e, p, q)
			return keypair

def encrypt(msg, pubkey):
	N, e = pubkey
	m = bytes_to_long(msg)
	assert m < N
	return pow(m, e, N)

def main():
	border = "┃"
	pr('┏' + '━' * 47 + '┓')
	pr(border, "Welcome to the Kiss ASIS Crypto challenge :) ", border)
	pr(border, "Try to find the secret message and get flag! ", border)
	pr('┗' + '━' * 47 + '┛')
	D = uniform(0.9990, 0.9999)
	k, nbit = randint(1, 6), 1024
	N, e, p, q  = genkey(nbit, D, k)
	pubkey = (N, e)
	rmsg = random_string(randint(14, 40))
	enc = encrypt(rmsg.encode(), pubkey)
	while True:
		pr(border, "[E]ncrypted message! [P]ublic parameters [S]end secret message! [Q]uit")
		ans = sc().decode().lower()
		if ans == 'e':
			pr(border, f'{enc = }')
		elif ans == 'p':
			pr(border, f'{N = }')
			print(border, f'{e = }')
		elif ans == 's':
			pr(border, 'Please send the secret message: ')
			_msg = ans = sc().decode().strip()
			if _msg == rmsg:
				die(border, f'{flag = }')
			else:
				die(border, f'Your input is not correct! Bye!!')
		elif ans == 'q':
			die(border, f'Quitting...')
		else:
			die(border, f'Not valid choice! Bye!!')

if __name__ == "__main__":
	main()