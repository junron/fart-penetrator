import requests
CRLF = '\r\n'

DEFAULT_HTTP_VERSION = 'HTTP/1.1'


class RequestParser(object):
    banned_headers = [x.lower() for x in ["Content-Length"]]

    def __parse_request_line(self, request_line):
        request_parts = request_line.split(' ')
        self.method = request_parts[0]
        self.url = request_parts[1]
        self.protocol = request_parts[2] if len(request_parts) > 2 else DEFAULT_HTTP_VERSION

    def __init__(self, req_text):
        req_lines = req_text.split(CRLF)
        if len(req_lines) == 1:
            req_lines = req_text.split("\n")
        self.__parse_request_line(req_lines[0])
        ind = 1
        self.headers = dict()
        req_line = req_lines[ind]
        while ind < len(req_lines) and len(req_line) > 0:
            colon_ind = req_line.find(':')
            if colon_ind + 1 != len(req_line) and req_line[colon_ind + 1] == " ":
                # Remove space
                req_line = req_line[:colon_ind] + req_line[colon_ind + 1:]
            header_key = req_line[:colon_ind]
            if header_key.lower() in self.banned_headers:
                ind += 1
                req_line = req_lines[ind]
                continue
            header_value = req_line[colon_ind + 1:]
            self.headers[header_key] = header_value
            ind += 1
            req_line = req_lines[ind]
        ind += 1
        self.data = [x.strip().encode("utf-8") for x in req_lines[ind:] if x.strip()] if ind < len(req_lines) else None
        self.headers["Content-Length"] = len(b"\r\n".join(self.data)) if self.data is not None else 0
        host = self.headers.get("Host")
        https = self.headers.get("Origin", "").startswith("https://") or self.headers.get("Origin", "").startswith(
            "https://")
        self.url = f"http{'s' if https else ''}://{host}{self.url}"

    def to_request(self):
        req = requests.PreparedRequest()
        req.prepare(self.method, self.url)
        req.method = self.method
        req.url = self.url
        req.headers = self.headers
        req.body = self.data
        return req
