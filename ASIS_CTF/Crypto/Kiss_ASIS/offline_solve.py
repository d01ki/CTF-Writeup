#!/usr/bin/env python3
"""
Offline solver using captured data
"""

from Crypto.Util.number import *

# Data from server
N = 9599119609395862186541800252974333664743350992183723110405639101720487802260576378331603719544250562272935326713636910614639378264174845787276066737588665167284921854778751038681783630151527612779939290769321370674282583403824007382256244266388163309541183278432036980460858247468656917788437204381293293896
1

e = 26187510285839980235415356684917632511090043841673644651319019468892618692902181614595737968667961233542130069766320558687727361049974456344960247983887562237290247697162173242778003908441210561769602628107025196562069927794587641954063880200449298622391370435121835107069213940465598188287557871511658512746840104057052680837736121418010170919535202455096094372029021560702090552900639756883684785933454824150510391835761537369643586056174890621781635819364564591113599182156838396818639348592101332606206151159971569157878756445381676222808655107701718763483404201740749702958256568689165491237682970902174421724453

enc = 818765321486244421214839449810353109493106882545694030967145975787453457217946962917088601714713455463615362234458580596965407197693085520446923517286107139942242103814853713616476056061411385156483227433450655021961457454294301482431387205860297427051388251562982961942396549963304754284320853722684537819
31

print(f"[*] N: {N.bit_length()} bits")
print(f"[*] e: {e.bit_length()} bits")
print(f"[*] enc: {enc}")

# Wiener's attack
from sympy import integer_nthroot

def continued_fractions(e, n):
    cf = []
    while n:
        cf.append(e // n)
        e, n = n, e % n
    
    convergents = []
    for i in range(len(cf)):
        if i == 0:
            num, den = cf[0], 1
        elif i == 1:
            num, den = cf[0] * cf[1] + 1, cf[1]
        else:
            num = cf[i] * convergents[i-1][0] + convergents[i-2][0]
            den = cf[i] * convergents[i-1][1] + convergents[i-2][1]
        convergents.append((num, den))
    
    return convergents

print("\n[*] Generating continued fractions...")
convergents = continued_fractions(e, N)
print(f"[+] Generated {len(convergents)} convergents")

print("\n[*] Testing convergents...")
for idx, (k, d) in enumerate(convergents[:300]):
    if k == 0:
        continue
    
    if idx % 20 == 0:
        print(f"[*] Testing convergent {idx}...")
    
    # Try both e*d = 1 + k*phi and e*d = -1 + k*phi
    for sign in [1, -1]:
        phi_candidate = (e * d + sign) // k
        
        if phi_candidate <= 0:
            continue
        
        # p + q = N - phi + 1
        s = N - phi_candidate + 1
        discriminant = s*s - 4*N
        
        if discriminant >= 0:
            sqrt_disc = integer_nthroot(discriminant, 2)[0]
            if sqrt_disc * sqrt_disc == discriminant:
                p = (s + sqrt_disc) // 2
                q = (s - sqrt_disc) // 2
                
                if p * q == N and p > 1 and q > 1:
                    print(f"\n[+] Found at convergent {idx}!")
                    print(f"[+] d = {d}")
                    print(f"[+] p = {p}")
                    print(f"[+] q = {q}")
                    
                    # Decrypt
                    m = pow(enc, d, N)
                    msg = long_to_bytes(m)
                    
                    print(f"\n[+] Decrypted message: {msg}")
                    print(f"\n[*] Send this to the server to get the flag!")
                    exit(0)

print("\n[!] Wiener's attack failed with standard approach")
print("[*] Trying extended search...")

# Try more convergents with direct decryption
for idx, (k, d) in enumerate(convergents[:500]):
    if k == 0 or d <= 0:
        continue
    
    try:
        m = pow(enc, d, N)
        msg_bytes = long_to_bytes(m)
        
        # Check if it's printable ASCII
        if len(msg_bytes) > 5 and len(msg_bytes) < 50:
            if all(32 <= b < 127 for b in msg_bytes):
                print(f"\n[+] Found possible message at convergent {idx}!")
                print(f"[+] d = {d}")
                print(f"[+] Message: {msg_bytes}")
    except:
        pass

print("\n[!] Attack failed!")
