import textwrap
from typing import Callable

from models.AttackConfig import AttackConfig
from models.StoredResponse import StoredResponse

Predicate = Callable[[StoredResponse], bool]


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
                    text = r.text
                    content = r.content
                    return bool({condition})
                """
            )
            , out)
        return out["func"]


class Filterer:
    terminate_attack_fn: Predicate
    store_response_fn: Predicate

    def __init__(self, config: AttackConfig):
        self.config = config
        terminate_attack_if = config.terminate_attack_if
        self.terminate_attack_fn = make_predicate(terminate_attack_if, False)
        self.store_response_fn = make_predicate(config.store_response_if, True)
