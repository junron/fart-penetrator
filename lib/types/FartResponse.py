from __future__ import annotations
import dataclasses

import requests

import typing

if typing.TYPE_CHECKING:
    from lib.types.AttackConfig import AttackConfig


@dataclasses.dataclass()
class FartResponse:
    raw_response: requests.Response | None
    status_code: int | None
    timing_ms: int | None
    content_length: int | None
    index: int | None

    @staticmethod
    def from_py_response(resp: requests.Response, timing_ms: int, index: int, config: AttackConfig):
        return FartResponse(
            resp if config.store_raw_response else None,
            resp.status_code,
            timing_ms if config.store_timing else None,
            len(resp.content) if config.store_content_length else None,
            index
        )
