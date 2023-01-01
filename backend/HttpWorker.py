import asyncio
import time
from typing import List, Callable, Any

from requests import Session, PreparedRequest
from backend.processors import *

from backend.RequestParser import RequestParser
from models.ResponseCallback import ResponseCallback


class HttpWorker:
    def __init__(self, http_request: str, request_payloads: List[tuple[str]], callback: ResponseCallback):
        self.http_request = http_request
        self.request_payloads = request_payloads
        self.callback = callback
        self.tasks = []

    async def run(self):
        req_queue = [make_request(self.http_request, payload) for payload in self.request_payloads]
        self.tasks = [asyncio.ensure_future(send(req, make_callback(i, self.callback))) for i, req in
                      enumerate(req_queue)]
        return await asyncio.gather(*self.tasks)

    def cancel(self):
        for task in self.tasks:
            task.cancel()


async def send(req: PreparedRequest, callback):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, normal_send, req, callback)


def normal_send(req: PreparedRequest, callback):
    s = Session()
    start = time.time_ns()
    resp = s.send(req, allow_redirects=False)
    delta = (time.time_ns() - start) // pow(10, 6)
    callback(resp, delta)


def make_callback(i, cb: ResponseCallback):
    def callback(res, timing):
        cb(i, res, timing)

    return callback


def make_request(http_request: str, payload: tuple[str]):
    assert b64e("hello") == 'aGVsbG8='
    for i, x in enumerate(payload):
        http_request = http_request.replace(f"FUZZ{i}", x)
    lines = http_request.splitlines()
    for i, line in enumerate(lines):
        if "{" in line and "}" in line:
            lines[i] = eval(f"f'{line}'")
    http_request = "\n".join(lines)
    return RequestParser(http_request).to_request()
