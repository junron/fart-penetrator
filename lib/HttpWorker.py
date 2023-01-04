import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List, Callable

import requests
import tqdm.cli
from requests import PreparedRequest

from lib.types.FartRequest import FartRequest
from lib.types.FartResponse import FartResponse
from lib.types.ResponseCallback import ResponseCallback

Predicate = Callable[[FartResponse], bool]


class HttpWorker:
    reqs: List[FartRequest]
    session: requests.Session
    store_raw_response: bool
    callback: ResponseCallback | None
    terminate_attack_fn: Predicate | None = None
    store_response_fn: Predicate | None = None
    tasks: List[asyncio.Task]
    tqdm: tqdm.tqdm
    pool: ThreadPoolExecutor

    def __init__(self, reqs: FartRequest | List[FartRequest], session: requests.Session | None = None,
                 callback: ResponseCallback = None, concurrency: int = 0,
                 store_raw_response=True, show_progress=False, dont_create_pool = False):
        if type(reqs) is not list:
            self.reqs = [reqs]
        else:
            self.reqs = reqs

        if session is None:
            session = requests.Session()

        self.session = session
        self.store_raw_response = store_raw_response
        self.callback = callback
        self.tasks = []
        self.cancelled = False
        self.show_progress = show_progress
        self.concurrency = concurrency
        self.sem = asyncio.Semaphore(concurrency) if concurrency > 0 else None
        self.dont_create_pool = dont_create_pool

    def terminate_if(self, predicate: Predicate) -> "HttpWorker":
        self.terminate_attack_fn = predicate
        return self

    def store_if(self, predicate: Predicate) -> "HttpWorker":
        self.store_response_fn = predicate
        return self

    async def run(self) -> List[FartResponse]:
        assert len(self.tasks) == 0, "Cannot call run on a worker with existing tasks"
        if not self.dont_create_pool:
            self.pool = ThreadPoolExecutor(self.concurrency if self.concurrency > 0 else min(100, len(self.reqs)))
        self.tasks = [asyncio.ensure_future(self.__send(req.to_request(), i)) for i, req in enumerate(self.reqs)]
        if self.show_progress:
            self.tqdm = tqdm.cli.tqdm(total=len(self.tasks))
        finished, unfinished = await asyncio.wait(self.tasks)
        results = [task.result() for task in finished if not task.cancelled()]
        if not self.dont_create_pool:
            self.pool.shutdown()
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

    def min_by(self, func) -> FartResponse | None:
        results = self.run_wait()
        if len(results) == 0:
            return None
        prop = min(map(func, results))
        return list(filter(lambda resp: func(resp) == prop, results))[0]

    def max_by(self, func) -> FartResponse | None:
        results = self.run_wait()
        if len(results) == 0:
            return None
        prop = max(map(func, results))
        return list(filter(lambda resp: func(resp) == prop, results))[0]

    def cancel(self, except_index: int = None):
        if self.cancelled:
            print("Warning: job double cancelled", except_index)
            return
        self.cancelled = True
        for i, task in enumerate(self.tasks):
            if i != except_index:
                task.cancel()

    async def __send(self, req: PreparedRequest, index: int):
        loop = asyncio.get_event_loop()
        if self.sem is not None:
            async with self.sem:
                return await loop.run_in_executor(self.pool, self.__blocking_send, req, index)
        return await loop.run_in_executor(self.pool, self.__blocking_send, req, index)

    def __blocking_send(self, req: PreparedRequest, index: int):
        start = time.time_ns()
        resp = self.session.send(req, allow_redirects=False)
        delta = (time.time_ns() - start) // pow(10, 6)
        fart_resp = FartResponse.from_py_response(resp, delta, index, self.reqs[index].payloads,
                                                  self.store_raw_response)
        if self.show_progress:
            self.tqdm.update()

        # Criteria not met for response to be stored
        if self.store_response_fn is not None and not self.store_response_fn(fart_resp):
            fart_resp = None

        if self.callback is not None:
            self.callback(index, fart_resp)

        # Criteria met for attack to be terminated
        if fart_resp is not None and self.terminate_attack_fn is not None and self.terminate_attack_fn(fart_resp):
            self.cancel(index)
        return fart_resp
