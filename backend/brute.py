import asyncio
import time
from typing import List

from requests import Session, PreparedRequest

from backend.RequestParser import RequestParser
from models.ResponseCallback import ResponseCallback


async def send(req: PreparedRequest, callback):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, normal_send, req, callback)


def normal_send(req: PreparedRequest, callback):
    s = Session()
    start = time.time_ns()
    resp = s.send(req, allow_redirects=False)
    delta = (time.time_ns() - start) // pow(10, 6)
    callback(resp, delta)


async def brute(http_request: str, request_payloads: List[tuple[str]], callback: ResponseCallback):
    req_queue = [make_request(http_request, payload) for payload in request_payloads]
    return await asyncio.gather(
        *[send(req, make_callback(i, callback)) for i, req in enumerate(req_queue)])


def make_callback(i, cb: ResponseCallback):
    def callback(res, timing):
        cb(i, res, timing)

    return callback


def make_request(http_request: str, payload: tuple[str]):
    for i, x in enumerate(payload):
        http_request = http_request.replace(f"FUZZ{i}", x)
    return RequestParser(http_request).to_request()
