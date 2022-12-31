from typing import Callable

import requests

ResponseCallback = Callable[[int, requests.Response, int], None]
