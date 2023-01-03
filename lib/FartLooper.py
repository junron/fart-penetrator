import asyncio
from typing import Any, Callable

from lib import HttpWorker, Predicate
from lib.types.FartResponse import FartResponse

StateUpdater = Callable[[FartResponse, Any], Any]
WorkerResponseSelector = Callable[[HttpWorker], FartResponse | None]


class FartLooper:
    def __init__(self, worker: HttpWorker, state: Any):
        self.worker = worker
        self.reqs = self.worker.reqs
        self.state = state
        self.updater: StateUpdater | None = None
        self.worker_response_selector: WorkerResponseSelector | None = None
        self.response_selector: Predicate | None = None
        self.debugger = None

    def update_with(self, updater: StateUpdater) -> "FartLooper":
        self.updater = updater
        return self

    def select_from_worker(self, func: WorkerResponseSelector) -> "FartLooper":
        self.worker_response_selector = func
        return self

    def max_by(self, func):
        self.select_from_worker(lambda worker: worker.max_by(func))
        return self

    def get_first(self, func: Predicate) -> "FartLooper":
        self.response_selector = func
        return self

    def debug(self, func):
        self.debugger = func
        return self

    def loop(self):
        assert self.updater is not None
        assert (self.worker_response_selector is not None or self.response_selector is not None)
        worker = self.worker
        while True:
            reqs = []
            for req in self.reqs:
                reqs += req.substitute(state=self.state)

            worker.cancelled = False
            worker.tasks = []
            worker.reqs = reqs
            worker.sem = asyncio.Semaphore(worker.concurrency) if worker.concurrency > 0 else None

            if self.worker_response_selector is not None:
                result = self.worker_response_selector(worker)
            else:
                result = worker.get_first(self.response_selector)
            if result is None:
                break
            if self.debugger is not None:
                self.debugger(result)
            self.state = self.updater(result, self.state)
            print(self.state)
        return self.state
