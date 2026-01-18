## usbstorage

I attached my friend's USB drive to my laptop and accidently copied a private file, which I immediately deleted. But my friend still somehow got the file from looking at the USB message their drive recorded...

## solutions

pcapファイルからの抽出

```
(venv) iniad@localhost:~/ctf/CTF-Writeup/nullcon_HackIM_CTF_2025/usbstorage$ find usbstorage*.img
usbstorage10117120.img
usbstorage35270656.img
usbstorage35275648.img
usbstorage35275664.img
usbstorage35275672.img
usbstorage35275728.img
usbstorage35275736.img
usbstorage35275792.img
usbstorage9842688.img
usbstorage9850928.img
usbstorage9851048.img
usbstorage9851176.img
usbstorage9916712.img
```

解凍

```
(venv) iniad@localhost:~/ctf/CTF-Writeup/nullcon_HackIM_CTF_2025/usbstorage$ unar flag.gz
flag.gz: Gzip
  flag... OK.
Successfully extracted to "./flag".
(venv) iniad@localhost:~/ctf/CTF-Writeup/nullcon_HackIM_CTF_2025/usbstorage$ cat flag
ENO{USB_STORAGE_SHOW_ME_THE_FLAG_PLS}
```

## flag

`ENO{USB_STORAGE_SHOW_ME_THE_FLAG_PLS}`