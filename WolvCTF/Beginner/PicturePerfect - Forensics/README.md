# PicturePerfect - Forensics

Wow what a respectful, happy looking lad! Hmmmmmmm, all I see is a snowman... maybe some details from the image file itself will lead us to the flag.


hi_snowman.jpgが与えられるのでメタデータ確認する
```
┌──(kali㉿kali)-[/media/sf_vm_share/ctf/WolvCTF_2025/forensic]
└─$ exiftool hi_snowman.jpg 
ExifTool Version Number         : 12.76
File Name                       : hi_snowman.jpg
Directory                       : .
File Size                       : 4.1 MB
File Modification Date/Time     : 2025:03:23 12:36:46+09:00
File Access Date/Time           : 2025:03:23 13:09:35+09:00
File Inode Change Date/Time     : 2025:03:23 12:36:46+09:00
File Permissions                : -rwxrwx---
File Type                       : JPEG
File Type Extension             : jpg
MIME Type                       : image/jpeg
JFIF Version                    : 1.01
Resolution Unit                 : inches
X Resolution                    : 96
Y Resolution                    : 96
Exif Byte Order                 : Big-endian (Motorola, MM)
Padding                         : (Binary data 268 bytes, use -b option to extract)
XMP Toolkit                     : Image::ExifTool 11.88
About                           : uuid:faf5bdd5-ba3d-11da-ad31-d33d75182f1b
Title                           : wctf{d0_yOU_w@nt_t0_BUiLd_a_Sn0Wm@n}
Image Width                     : 3024
Image Height                    : 4032
Encoding Process                : Baseline DCT, Huffman coding
Bits Per Sample                 : 8
Color Components                : 3
Y Cb Cr Sub Sampling            : YCbCr4:2:0 (2 2)
Image Size                      : 3024x4032
Megapixels                      : 12.2
```

## flag
`wctf{d0_yOU_w@nt_t0_BUiLd_a_Sn0Wm@n}`
