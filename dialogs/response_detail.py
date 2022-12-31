import requests
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog

from models.StoredResponse import StoredResponse


# Very bad
def reconstruct_raw_http(response: requests.Response):
    # Probably wrong
    version = "HTTP/1.1" if response.raw.version == 11 else "HTTP/1.0"
    lines = [f"{version} {response.status_code} {response.reason}"]
    for k, v in response.headers.items():
        lines.append(f"{k}: {v}")
    lines.append("")
    lines.append(response.text)
    return "\r\n".join(lines)


class ResponseDetail(QDialog):

    def __init__(self, req_num: int, response: StoredResponse):
        super().__init__()
        self.req_num = req_num
        self.response = response
        try:
            self.ui = uic.loadUi("./dialogs/response_detail.ui", self)
            self.ui.req_no.setText(f"Request Number: {req_num}")
            self.ui.timing.setText(f"Timing: {response.timing_ms}ms")
            self.ui.http_response.setTextFormat(Qt.TextFormat.PlainText)
            if response.raw_response is not None:
                self.ui.http_response.setText(reconstruct_raw_http(response.raw_response))
            else:
                self.ui.http_response.setText("Response not stored")
        except Exception as e:
            print(e)
        self.show()


