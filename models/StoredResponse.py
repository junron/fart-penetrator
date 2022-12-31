import dataclasses

import requests

from models.AttackConfig import AttackConfig


@dataclasses.dataclass()
class StoredResponse:
    raw_response: requests.Response | None
    status_code: int | None
    timing_ms: int | None
    content_length: int | None

    @staticmethod
    def from_py_response(resp: requests.Response, timing_ms: int, config: AttackConfig):
        return StoredResponse(
            resp if config.store_raw_response else None,
            resp.status_code,
            timing_ms if config.store_timing else None,
            len(resp.content) if config.store_content_length else None
        )
