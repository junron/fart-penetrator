import asyncio
import time
from typing import List

import requests
from requests import PreparedRequest

from lib.types.AttackConfig import AttackConfig, Predicate
from lib.types.FartRequest import FartRequest
from lib.types.FartResponse import FartResponse
from lib.types.ResponseCallback import ResponseCallback


class HttpWorker:
    reqs: List[FartRequest]
    session: requests.Session
    config: AttackConfig
    callback: ResponseCallback | None
    tasks: List[asyncio.Task]

    def __init__(self, reqs: FartRequest | List[FartRequest], session: requests.Session | None = None,
                 callback: ResponseCallback = None,
                 config: AttackConfig = None):
        if type(reqs) is not list:
            self.reqs = [reqs]
        else:
            self.reqs = reqs

        if session is None:
            session = requests.Session()

        if config is None:
            config = AttackConfig()

        self.session = session
        self.config = config
        self.callback = callback
        self.tasks = []

    def terminate_if(self, predicate: Predicate) -> "HttpWorker":
        self.config.terminate_attack_fn = predicate
        return self

    def store_if(self, predicate: Predicate) -> "HttpWorker":
        self.config.store_response_fn = predicate
        return self

    async def run(self) -> List[FartResponse]:
        assert len(self.tasks) == 0, "Cannot call run on a worker with existing tasks"
        self.tasks = [asyncio.ensure_future(self.__send(req.to_request(), i)) for i, req in enumerate(self.reqs)]
        finished, unfinished = await asyncio.wait(self.tasks)
        results = [task.result() for task in finished if not task.cancelled()]
        return list(filter(lambda x: x is not None, results))

    def run_wait(self) -> List[FartResponse]:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.run())

    def get_first(self, predicate: Predicate) -> FartResponse | None:
        self.terminate_if(predicate)
        self.store_if(predicate)
        results = self.run_wait()
        if len(results) == 0:
            return None
        return results[0]

    def cancel(self, except_index: int = None):
        for i, task in enumerate(self.tasks):
            if i != except_index:
                task.cancel()

    async def __send(self, req: PreparedRequest, index: int):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.__blocking_send, req, index)

    def __blocking_send(self, req: PreparedRequest, index: int):
        start = time.time_ns()
        resp = self.session.send(req, allow_redirects=False)
        delta = (time.time_ns() - start) // pow(10, 6)
        fart_resp = FartResponse.from_py_response(resp, delta, index, self.config)

        # Criteria not met for response to be stored
        if not self.config.store_response_fn(fart_resp):
            fart_resp = None

        if self.callback is not None:
            self.callback(index, fart_resp)

        # Criteria met for attack to be terminated
        if fart_resp is not None and self.config.terminate_attack_fn(fart_resp):
            self.cancel(index)
            # TODO: inform caller that job is cancelled
        return fart_resp
