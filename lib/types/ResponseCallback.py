from typing import Callable

from lib.types.FartResponse import FartResponse

ResponseCallback = Callable[[int, FartResponse], None]
