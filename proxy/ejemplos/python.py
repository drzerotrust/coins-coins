import requests

url = "https://api.ipify.org?format=json"

try:
    no_proxy = requests.get(url)
    proxy = requests.get(url, proxies={
        "http" : "http://172.28.0.2:8888",
        "https" : "http://172.28.0.2:8888"
    })
except Exception as error:
    raise error

out = "IP con proxy: %s\nIP sin proxy: %s" % (
    no_proxy.json().get("ip", "[!] error"),
    proxy.json().get("ip", "[!] error")
)

print(out)
