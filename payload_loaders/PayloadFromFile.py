from __future__ import annotations
import os
import typing

from PyQt6.QtWidgets import QMessageBox

from payload_loaders.PayloadLoader import PayloadLoader

if typing.TYPE_CHECKING:
    from penetrator import PenetratorWindow


class PayloadFromFile(PayloadLoader):
    def __init__(self, penetrator: PenetratorWindow):
        super().__init__(penetrator)
        self.ui.add_payload_btn.clicked.connect(lambda x: self.add_payload_set())

    def add_payload_set(self):
        filepath = self.ui.payload_file_input.text()
        payload_set = load_payload_from_file(filepath)
        if payload_set is not None:
            self.penetrator.add_payload_set(payload_set, filepath)
        else:
            QMessageBox.critical(self.penetrator, "Error", "File does not exist")


def load_payload_from_file(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r") as file:
            payload_set = file.readlines()
            return [x.strip() for x in payload_set if x.strip()]
    return None
