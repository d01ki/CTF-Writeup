# DigginDir - Forensics
Author: carmengh
So I tripped on an uneven sidewalk today.... and I dropped the flag somewhere (oops). It's gotta be here somewhere..... right?

Unlock Hint for 0 points
I wish there was a linux utility that let me search for stuff...

解凍すると以下のようなものが沢山出てくる
```
┌──(kali㉿kali)-[/media/…/ctf/WolvCTF_2025/Beginner/fore]
└─$ tar -xzvf dist.tar.gz
challenge/
challenge/0Egu9cCmH2tWMB48Uiw1N1Jfm/
challenge/0Egu9cCmH2tWMB48Uiw1N1Jfm/file.txt
challenge/0ghc6cHZYcqBUw1RrmWFmGKJK/
challenge/0ghc6cHZYcqBUw1RrmWFmGKJK/file.txt
challenge/0p82csvfHLnuwY8b6Cu9vK7LW/
challenge/0p82csvfHLnuwY8b6Cu9vK7LW/file.txt
challenge/0XYH4DKRibzfdJcnv5QtLBclk/
challenge/0XYH4DKRibzfdJcnv5QtLBclk/file.txt
challenge/13hyqkkQnjrV9LcXzdP8mUIf1/
challenge/13hyqkkQnjrV9LcXzdP8mUIf1/file.txt
challenge/1L1h3xlvFIMRTsnPEZWEv0X4K/
challenge/1L1h3xlvFIMRTsnPEZWEv0X4K/file.txt
challenge/29Lw3QDk6tF1stuax3U0Dn2EK/
challenge/29Lw3QDk6tF1stuax3U0Dn2EK/file.txt
```

## solve

grepで行けるんじゃないかと思いやるとできた
>ディレクトリ内のすべてのファイルを検索し、wctf{を含む部分を出力

```
┌──(kali㉿kali)-[/media/…/WolvCTF_2025/Beginner/fore/challenge]
└─$ grep -r "wctf{" *
EUOlptwlpqPt5qrGlMnFpbat6/.secret:wctf{0h_WOW_tH@Nk5_yOu_f0U^d_1t_xD}
```

## flag
`wctf{0h_WOW_tH@Nk5_yOu_f0U^d_1t_xD}`