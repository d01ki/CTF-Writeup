# magic

I think there's something wrong with this file, can you work some magic?

magic.pngが与えられるがfileコマンドで確認すると dataになっている、恐らくファイルヘッダが破損している

```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/BSide]
└─$ file magic.png  
magic.png: data
```
マジックバイトを確認する

```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/BSide]
└─$ xxd -l 16 magic.png
00000000: 616e 7368 0d0a 1a0a 0000 000d 4948 4452  ansh........IHDR
```

PNGファイルのマジックバイトは以下が正しいが今回のmagic.pngは異なっていることが分かった
```
89 50 4E 47 0D 0A 1A 0A
```

正しいマジックバイトを上書きする

```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/BSide]
└─$ printf '\x89PNG\r\n\x1a\n' | dd of=magic.png bs=1 seek=0 count=8 conv=notrunc
8+0 records in
8+0 records out
8 bytes copied, 0.00551473 s, 1.5 kB/s
```
PNGに直ったので開くとFlagが出てくる

```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/BSide]
└─$ file magic.png                                                          
magic.png: PNG image data, 1441 x 1440, 8-bit/color RGBA, non-interlaced
```

`CTF{g0t_th3_p0w3r_u_n33d}`