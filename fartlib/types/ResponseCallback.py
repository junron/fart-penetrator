from typing import Callable

from fartlib.types.FartResponse import FartResponse

ResponseCallback = Callable[[int, FartResponse], None]
