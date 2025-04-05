## HeaderHijack

>A secret agent's intercepted video file refuses to play. A mysterious checksum file was found alongside it. Your task is to repair the file and retrieve the flag...

与えられmp4を確認する
```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ace-ctf/steg]
└─$ file not_the_flag.mp4 
not_the_flag.mp4: data

```

mp4修復サイト、で検索して見つけた以下のサイトにアップロードする


[text](https://fix.video/)

修復された動画を再生すると、0:04秒の時にflagが現れた


![alt text](image.png)

`ACECTF{d3c0d3_h3x_1s_fun}`