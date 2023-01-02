from __future__ import annotations

import os
import typing

from PyQt6.QtWidgets import QComboBox

from payload_loaders.PayloadFromFile import load_payload_from_file
from payload_loaders.PayloadLoader import PayloadLoader

if typing.TYPE_CHECKING:
    from penetrator import PenetratorWindow


class PayloadFromWordlist(PayloadLoader):
    def __init__(self, penetrator: PenetratorWindow):
        super().__init__(penetrator)
        wordlists = os.listdir("./wordlists")
        self.combobox: QComboBox = self.ui.wordlist_combobox
        self.combobox.addItems(wordlists)
        self.ui.add_from_wordlist_btn.clicked.connect(lambda x: self.add_payload_set())

    def add_payload_set(self):
        text = self.combobox.currentText()
        payload_set = load_payload_from_file(f"./wordlists/{text}")
        self.penetrator.add_payload_set(payload_set, text)
