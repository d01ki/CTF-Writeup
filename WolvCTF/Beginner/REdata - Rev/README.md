# REdata - Rev
An eZ RE challenge.

dist.tar.gzが与えられるので解凍する
```
┌──(kali㉿kali)-[/media/…/ctf/WolvCTF_2025/Beginner/rev2]
└─$ ls
dist.tar.gz  redata
```

stringsで行けた
```
┌──(kali㉿kali)-[/media/…/ctf/WolvCTF_2025/Beginner/rev2]
└─$ strings redata | grep ctf{
wctf{n0_w4y_y0u_f0unD_1t!}
```

## flag
`wctf{n0_w4y_y0u_f0unD_1t!}`