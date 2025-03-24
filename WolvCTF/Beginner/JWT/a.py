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
