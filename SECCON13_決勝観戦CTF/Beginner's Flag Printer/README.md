## Beginner's Flag Printer

フラグを出力するアセンブリです🤖
```
.LC0:
        .string "Alpaca{%x}\n"
main:
        push    rbp
        mov     rbp, rsp
        sub     rsp, 16
        mov     DWORD PTR [rbp-4], 539232261
        mov     eax, DWORD PTR [rbp-4]
        mov     esi, eax
        mov     edi, OFFSET FLAT:.LC0
        mov     eax, 0
        call    printf
        mov     eax, 0
        leave
        ret
```
539232261の16進表記に変換する

### Flag
`Alpaca{20240805}`