try:
    import requests
except ImportError:
    print("Install requests with pip: pip install requests")
    exit(0)

#######################################################
# Add the same local proxy urls as in the compose file
# You can test the exit node ips of the proxies here
#######################################################

url = "https://api.ipify.org?format=json"

proxies = [
    "http://172.28.0.2:6666", 
    "http://172.28.0.3:6666", 
    "http://172.28.0.4:6666"
]

for proxy in proxies:
    p = proxy
    try:
        proxy = requests.get(url, proxies={
            "http" : proxy,
            "https" : proxy
        })
    except Exception as error:
        print("Proxy %s down" % proxy)
        continue
    if proxy.status_code != 200:
        print("Unable to get IP for proxy %s" % proxy)
        continue
    out = "Local Proxy %s | Proxy IP: %s" % (
        p,
        proxy.json().get("ip", "[!] error")
    )
    print(out)
