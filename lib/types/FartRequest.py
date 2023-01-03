import itertools
from typing import List, Iterable

import requests
import random
import time
from lib.processors import *

CRLF = '\r\n'

DEFAULT_HTTP_VERSION = 'HTTP/1.1'

# Prevent processors and useful libs from being optimized out
# Used for interpolation in requests
assert b64e("hello") == 'aGVsbG8='
rnd = random.randint(1, 10)
tme = time.time()


class FartRequest(object):
    __banned_headers = [x.lower() for x in ["Content-Length"]]

    def __init__(self, req_text: str, payloads: Iterable[str] | None = None):
        self.req_text = req_text.lstrip()
        self.payloads = payloads

    def substitute(self, *args, **kwargs):
        return self.substitute_product(*args, **kwargs)

    def substitute_product(self, *args, **kwargs):
        positions, arguments = self.__gen_positions(args, kwargs)
        payloads = list(itertools.product(*arguments))
        return self.substitute_raw(positions, payloads)

    def substitute_raw(self, positions: List[str], payloads: List[str] | List[List[str]] | List[tuple[str]]) \
            -> List['FartRequest']:
        if len(payloads) == 0:
            return []
        if type(payloads[0]) not in [list, tuple]:
            # Only 1 parameter
            payloads = [[x] for x in payloads]

        out = []
        for payload in payloads:
            http_request = self.req_text
            for i, x in enumerate(payload):
                http_request = http_request.replace(positions[i], x)
            lines = http_request.splitlines()
            for i, line in enumerate(lines):
                if "{" in line and "}" in line:
                    lines[i] = eval(f"f'{line}'")
            http_request = "\n".join(lines)
            out.append(FartRequest(http_request, payload))
        return out

    @staticmethod
    def __gen_positions(args: tuple, kwargs: dict):
        positions = [f"FUZZ{n}" for n in range(len(args))]
        positions += list(kwargs.keys())
        approved_arguments = []
        arguments = list(args) + list(kwargs.values())
        for argument in arguments:
            assert type(argument) in [str, list, tuple], "Argument type must be str, list or tuple"
            if type(argument) is str:
                approved_arguments.append([argument])
            else:
                for item in argument:
                    assert type(item) is str, ("Argument item type must be str", argument, item)
                approved_arguments.append(argument)
        return positions, approved_arguments

    # based on https://gist.github.com/cunla/c074179a587c0d012229ee8cc5c04a8c
    def to_request(self):
        req_lines = self.req_text.split(CRLF)
        if len(req_lines) == 1:
            req_lines = self.req_text.split("\n")
        request_parts = req_lines[0].split(' ')
        method = request_parts[0]
        url = request_parts[1]
        ind = 1
        headers = dict()
        req_line = req_lines[ind]
        while ind < len(req_lines) and len(req_line) > 0:
            colon_ind = req_line.find(':')
            if colon_ind + 1 != len(req_line) and req_line[colon_ind + 1] == " ":
                # Remove space
                req_line = req_line[:colon_ind] + req_line[colon_ind + 1:]
            header_key = req_line[:colon_ind]
            if header_key.lower() in self.__banned_headers:
                ind += 1
                req_line = req_lines[ind]
                continue
            header_value = req_line[colon_ind + 1:]
            headers[header_key] = header_value
            ind += 1
            req_line = req_lines[ind]
        ind += 1
        data = [x.strip().encode("utf-8") for x in req_lines[ind:] if x.strip()] if ind < len(req_lines) else None
        headers["Content-Length"] = len(b"\r\n".join(data)) if data is not None else 0
        host = headers.get("Host")
        https = headers.get("Origin", "").startswith("https://") or headers.get("Referer", "").startswith(
            "https://")
        url = f"http{'s' if https else ''}://{host}{url}"
        req = requests.PreparedRequest()
        req.prepare(method, url)
        req.method = method
        req.url = url
        req.headers = headers
        req.body = data
        return req
