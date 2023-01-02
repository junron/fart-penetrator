import dataclasses
import textwrap
from typing import Callable

from lib.types.FartResponse import FartResponse

Predicate = Callable[[FartResponse], bool]


@dataclasses.dataclass()
class AttackConfig:
    store_raw_response: bool = True
    store_timing: bool = True
    store_content_length: bool = True
    terminate_attack_fn: Predicate = lambda resp: resp.status_code > 499
    store_response_fn: Predicate = lambda resp: True

    def table_headers(self):
        return ["Status Code"] + (["Timing"] if self.store_timing else []) + (
            ["Length"] if self.store_content_length else [])


def make_predicate(condition: str, default: bool) -> Predicate:
    if condition is None or condition.strip() == "":
        return lambda x: default
    else:
        out = {}
        exec(
            textwrap.dedent(
                f"""
                def func(stored_response):
                    r = stored_response.raw_response
                    sc = stored_response.status_code
                    timing = stored_response.timing_ms
                    length = stored_response.content_length
                    content_length = stored_response.content_length
                    text = r.text
                    content = r.content
                    return bool({condition})
                """
            )
            , out)
        return out["func"]
