## DONOTOPEN

>A suspicious script file seems to be hiding something important, but it refuses to cooperate. It's obfuscated, tampered with, and demands a password. Unravel the mystery to uncover the hidden flag.


```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ace-ctf/rev]
└─$ binwalk -e DONTOPEN

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
693           0x2B5           gzip compressed data, has original file name: "pythonscript.py", from Unix, last modified: 2025-01-25 14:43:44

WARNING: One or more files failed to extract: either no utility was found or it's unimplemented
```
pythonscript.pyが手に入ったのでcatで見てみる

```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/ace-ctf/rev]
└─$ cat _DONTOPEN.extracted/pythonscript.py
import hashlib
import requests
import webbrowser  
NOT_THE_FLAG = "flag{this-is-not-the-droid-youre-looking-for}"
flag0 = 'flag{cfcd208495d565ef66e7dff9f98764da}'
flag1 = 'flag{c4ca4238a0b923820dcc509a6f75849b}'
...
flag998 = 'flag{9ab0d88431732957a618d4a469a0d4c3}'
flag999 = 'flag{b706835de79a2b4e80506f582af3676a}'
FLAG_PREFIX = "ACE{%s}"

print("It looks like the box is locked with some kind of password, determine the pin to open the box!")
req = requests.get("http://google.com")
req.raise_for_status()

pin = input("What is the pin code?")
if pin == "ACE@SE7EN":
    print("Looks good to me...")
    print("I guess I'll generate a flag")

    req = requests.get("http://example.com")
    req.raise_for_status()

    print(FLAG_PREFIX % hashlib.blake2b((pin + "Vansh").encode("utf-8")).hexdigest()[:32])
else:
    print("Bad pin!") 
```
binwalkから抽出したpythonコードから、pin == "ACE@SE7EN”を入力するのがわかる
実行するとWhat is the pin code?と求められるのでACE@SE7ENを入れるとflagが手に入る

```
~/ctf/ace-ctf/rev$ python3 pythonscript.py
It looks like the box is locked with some kind of password, determine the pin to open the box!
gio: https://vipsace.org/: Operation not supported
What is the pin code?ACE@SE7EN
Looks good to me...
I guess I'll generate a flag
ACE{e2e3619b630b3be9de762910fd58dba7}
```

`ACE{e2e3619b630b3be9de762910fd58dba7}`