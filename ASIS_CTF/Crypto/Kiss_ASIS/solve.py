#!/usr/bin/env python3

from pwn import *
from Crypto.Util.number import long_to_bytes, inverse
import string
import re

def continued_fraction(n, d):
    """Generate continued fraction expansion of n/d"""
    while d:
        yield n // d
        n, d = d, n % d

def convergents(n, d):
    """Generate convergents of the continued fraction n/d"""
    cf_list = []
    cf_gen = continued_fraction(n, d)
    
    # Get first few terms
    for _ in range(1000):
        try:
            cf_list.append(next(cf_gen))
        except StopIteration:
            break
    
    # Calculate convergents
    h_prev2, h_prev1 = 0, 1
    k_prev2, k_prev1 = 1, 0
    
    for q in cf_list:
        h = q * h_prev1 + h_prev2
        k = q * k_prev1 + k_prev2
        yield (h, k)
        h_prev2, h_prev1 = h_prev1, h
        k_prev2, k_prev1 = k_prev1, k

def isqrt(n):
    """Integer square root"""
    if n < 0:
        return None
    if n == 0:
        return 0
    x = n
    y = (x + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def recover_primes(N, phi, k=1):
    """Recover p and q from N and phi, given phi = (p^k - 1)(q^k - 1)"""
    if k == 1:
        # phi = (p-1)(q-1) = N - p - q + 1
        # p + q = N - phi + 1
        sum_pq = N - phi + 1
        
        # p and q are roots of x^2 - (p+q)x + N = 0
        # discriminant = (p+q)^2 - 4N
        disc = sum_pq * sum_pq - 4 * N
        
        if disc < 0:
            return None, None
        
        sqrt_disc = isqrt(disc)
        if sqrt_disc * sqrt_disc != disc:
            return None, None
        
        p = (sum_pq + sqrt_disc) // 2
        q = (sum_pq - sqrt_disc) // 2
        
        if p * q == N and p > 1 and q > 1:
            return p, q
    
    return None, None

def attack(N, e, enc):
    """Perform continued fraction attack (Wiener's attack)"""
    print("[*] Starting Wiener's attack (continued fraction)...")
    
    # Try convergents of e/N
    count = 0
    for k, d in convergents(e, N):
        count += 1
        if count % 100 == 0:
            print(f"[*] Tried {count} convergents...")
        
        if d == 0:
            continue
        
        # For Wiener's attack: e*d ≡ 1 (mod phi)
        # So e*d = k*phi + 1 for some k
        # phi = (e*d - 1) / k
        
        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            
            # Try to recover p and q from N and phi
            p, q = recover_primes(N, phi)
            
            if p and q:
                print(f"[+] Found valid p and q!")
                print(f"[+] k = {k}, d = {d}")
                print(f"[+] phi = {phi}")
                
                # Verify and decrypt
                try:
                    # Verify e*d ≡ 1 (mod phi)
                    if (e * d) % phi != 1:
                        # d might not be the actual decryption exponent
                        # Calculate the real one
                        d_real = inverse(e, phi)
                    else:
                        d_real = d
                    
                    # Decrypt
                    m = pow(enc, d_real, N)
                    msg = long_to_bytes(m)
                    
                    # Check if it's printable
                    try:
                        decoded = msg.decode('utf-8')
                        print(f"[+] Decrypted message: {decoded}")
                        return decoded
                    except:
                        # Try with latin-1
                        decoded = msg.decode('latin-1')
                        if decoded.isprintable():
                            print(f"[+] Decrypted message: {decoded}")
                            return decoded
                except Exception as ex:
                    print(f"[-] Decryption failed: {ex}")
                    continue
        
        # Stop after trying many convergents
        if count > 10000:
            print(f"[-] Tried {count} convergents without success")
            break
    
    print("[-] Attack failed")
    return None

def main():
    # Connect to server
    HOST = "65.109.214.93"
    PORT = 13137
    
    print(f"[*] Connecting to {HOST}:{PORT}...")
    conn = remote(HOST, PORT)
    
    # Receive banner
    banner = conn.recv(1024).decode(errors='ignore')
    print(f"[DEBUG] Banner:\n{banner}")
    
    # Get public parameters
    print("\n[*] Getting public parameters...")
    conn.sendline(b'p')
    data = conn.recv(4096).decode(errors='ignore')
    print(f"[DEBUG] Response to 'p':\n{data}")
    
    # Parse N and e
    n_match = re.search(r'N = (\d+)', data)
    e_match = re.search(r'e = (\d+)', data)
    
    if not n_match or not e_match:
        print("[-] Failed to parse N and e")
        conn.close()
        return
    
    N = int(n_match.group(1))
    e = int(e_match.group(1))
    
    print(f"\n[+] N = {N}")
    print(f"[+] e = {e}")
    print(f"[+] N bit length: {N.bit_length()}")
    
    # Get encrypted message
    print("\n[*] Getting encrypted message...")
    conn.sendline(b'e')
    data = conn.recv(4096).decode(errors='ignore')
    print(f"[DEBUG] Response to 'e':\n{data}")
    
    # Parse enc
    enc_match = re.search(r'enc = (\d+)', data)
    
    if not enc_match:
        print("[-] Failed to parse enc")
        conn.close()
        return
    
    enc = int(enc_match.group(1))
    print(f"\n[+] enc = {enc}")
    
    # Perform attack
    print("\n" + "="*60)
    secret_msg = attack(N, e, enc)
    print("="*60 + "\n")
    
    if secret_msg:
        # Send secret message
        print("[*] Sending secret message...")
        conn.sendline(b's')
        conn.recv(1024)  # Receive prompt
        conn.sendline(secret_msg.encode())
        
        # Get flag
        response = conn.recvall(timeout=2).decode(errors='ignore')
        print(f"\n[+] Server response:\n{response}")
        
        # Extract flag
        flag_match = re.search(r'ASIS\{[^}]+\}', response)
        if flag_match:
            print(f"\n{'='*60}")
            print(f"[SUCCESS] FLAG: {flag_match.group(0)}")
            print(f"{'='*60}")
    else:
        print("[-] Could not decrypt message")
    
    conn.close()

if __name__ == "__main__":
    main()