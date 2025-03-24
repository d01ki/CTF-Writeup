# Breakout

Something fishy about that photo... What could be hidden in this game?

https://wolvctf.io/files/14a1bab0e851eb85ae7e4db6c2577910/breakout.jpg?token=eyJ1c2VyX2lkIjoxMTY5LCJ0ZWFtX2lkIjo1OTgsImZpbGVfaWQiOjE4fQ.Z9-FXA.BLEul37pKGM5FPNBPxXVf20-iwM


```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/WolvCTF_2025/forensic]
└─$ steghide extract -sf breakout.jpg
Enter passphrase: 
the file "breakout.ch8" does already exist. overwrite ? (y/n) y
wrote extracted data to "breakout.ch8".
```

CHIP-8（チップエイト）という仮想マシン用のバイナリデータだね。
CHIP-8 は、1970年代に作られた簡単なインタープリタ言語で、レトロゲームを動かすためのものらしい