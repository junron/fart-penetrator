from __future__ import annotations

import typing

from PyQt6.QtWidgets import QApplication

from payload_loaders.PayloadLoader import PayloadLoader

if typing.TYPE_CHECKING:
    from penetrator import PenetratorWindow


class PayloadFromClipboard(PayloadLoader):
    def __init__(self, penetrator: PenetratorWindow):
        super().__init__(penetrator)
        self.ui.add_from_clipboard.clicked.connect(lambda x: self.add_payload_set())

    def add_payload_set(self):
        text = QApplication.clipboard().text()
        payload_set = [x.strip() for x in text.splitlines() if x.strip()]
        self.penetrator.add_payload_set(payload_set, "Clipboard")
