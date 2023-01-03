from __future__ import annotations
import dataclasses

import requests

import typing


@dataclasses.dataclass()
class FartResponse:
    raw_response: requests.Response | None
    status_code: int | None
    timing_ms: int | None
    content_length: int | None
    index: int | None
    text: str | None
    payloads: typing.Iterable[str] | None

    @staticmethod
    def from_py_response(resp: requests.Response, timing_ms: int, index: int, payloads: typing.Iterable[str],
                         store_raw: bool = True):
        return FartResponse(
            resp if store_raw else None,
            resp.status_code,
            timing_ms,
            len(resp.content),
            index,
            resp.text if store_raw else None,
            payloads
        )
