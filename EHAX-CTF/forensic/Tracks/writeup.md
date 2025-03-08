## Tracks

mp4が与えられます
なにか隠されてないかと思いbinwalkコマンドするとqrf.pngが手に入りました

```
└─$ binwalk -e chall.mp4  

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
7892907       0x786FAB        Zip archive data, encrypted at least v1.0 to extract, compressed size: 45, uncompressed size: 33, name: flag.txt
7893134       0x78708E        Zip archive data, at least v2.0 to extract, compressed size: 2082, uncompressed size: 2642, name: qrf.png

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented

                                                                                                                     
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ehax-ctf/forensic]
└─$ dd if=chall.mp4 of=hidden.zip bs=1 skip=7892907
58664+0 records in
58664+0 records out
58664 bytes (59 kB, 57 KiB) copied, 10.7324 s, 5.5 kB/s
                                                                                                                     
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ehax-ctf/forensic]
└─$ ls
chall.mp4  _chall.mp4.extracted  ehaxradio  hidden.zip
                                                                                                                     
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ehax-ctf/forensic]
└─$ unzip hidden.zip 
Archive:  hidden.zip
warning [hidden.zip]:  227 extra bytes at beginning or within zipfile
  (attempting to process anyway)
  inflating: qrf.png                 
                                                                                                                     
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ehax-ctf/forensic]
└─$ ls
chall.mp4  _chall.mp4.extracted  ehaxradio  hidden.zip  qrf.png

```

https://www.aperisolve.com/

aperisolveに入れると以下の文字が出てくる

![alt text](image.png)

$t@cy*1245が出てきた。これをパスワードにしてZIP解凍すると
YB4R{x00zyh$bgcln7_f0p3yx_$n4ws}がflag.txtに入っていた
フラグフォーマットはEH4Xで始まるので
ROT13でAmount6にするとEH4X{d00fen$hmirt7_l0v3ed_$t4cy}となる

### Flag
`EH4X{d00fen$hmirt7_l0v3ed_$t4cy}`