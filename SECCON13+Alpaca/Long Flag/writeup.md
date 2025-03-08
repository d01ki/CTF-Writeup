## Long Flag

出力からフラグを復元してください🐍
```
import os
from Crypto.Util.number import bytes_to_long

print(bytes_to_long(os.getenv("FLAG").encode()))
```
出力:
`35774448546064092714087589436978998345509619953776036875880600864948129648958547184607421789929097085`
long_to_bytesにすればいい
```
import os
from Crypto.Util.number import long_to_bytes

flag_long = 35774448546064092714087589436978998345509619953776036875880600864948129648958547184607421789929097085
flag_bytes = long_to_bytes(flag_long)
print(flag_bytes)
```
```
$ python3 a.py
b'Alpaca{LO00OO000O00OOOO0O00OOO00O000OOONG}'
```

### Flag
`Alpaca{LO00OO000O00OOOO0O00OOO00O000OOONG}`
