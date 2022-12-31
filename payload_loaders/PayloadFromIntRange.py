from __future__ import annotations
import os
import typing

from PyQt6.QtWidgets import QComboBox, QSpinBox, QMessageBox, QCheckBox

from payload_loaders.PayloadFromFile import load_payload_from_file
from payload_loaders.PayloadLoader import PayloadLoader

if typing.TYPE_CHECKING:
    from penetrator import PenetratorWindow


class PayloadFromIntRange(PayloadLoader):
    num_from: QSpinBox
    num_to: QSpinBox
    num_step: QSpinBox

    def __init__(self, penetrator: PenetratorWindow):
        super().__init__(penetrator)
        self.num_from = self.ui.num_from
        self.num_to = self.ui.num_to
        self.num_step = self.ui.num_step
        self.ui.add_nums.clicked.connect(lambda x: self.add_payload_set())

    def add_payload_set(self):
        num_from = self.num_from.value()
        num_to = self.num_to.value()
        num_step = self.num_step.value()
        int_range = range(num_from, num_to, num_step)
        if len(int_range) == 0:
            return QMessageBox.critical(self.penetrator, "Error", "Int range is empty")
        payload_set = [str(x) for x in int_range]
        zfill: QCheckBox = self.ui.num_zfill
        if zfill.isChecked():
            max_len = max(len(x) for x in payload_set)
            payload_set = [x.zfill(max_len) for x in payload_set]
        if num_step == 1:
            self.penetrator.add_payload_set(payload_set, f"Range({num_from},{num_to})")
        else:
            self.penetrator.add_payload_set(payload_set, f"Range({num_from},{num_to},{num_step})")
