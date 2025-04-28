import requests

res = requests.get(
    "https://your-browser-hates-you-4a61071d.challenges.bsidessf.net/",
    verify=False
)
print(res.text)
