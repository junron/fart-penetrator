import dataclasses
from typing import Callable

from PyQt6 import uic
from PyQt6.QtWidgets import QDialog, QCheckBox, QLineEdit

from models.AttackConfig import AttackConfig


class AttackConfigDialog(QDialog):

    def __init__(self, config: AttackConfig, callback: Callable[[AttackConfig], None]):
        super().__init__()
        self.config = dataclasses.replace(config)
        self.callback = callback

        self.ui = uic.loadUi("./dialogs/attack_config.ui", self)
        self.load()

        self.ui.ok_btn.clicked.connect(lambda x: self.submit())
        self.show()

    def load(self):
        ui = self.ui
        config = self.config
        store_resp: QCheckBox = ui.store_resp
        store_resp.setChecked(config.store_raw_response)
        ui.store_timing.setChecked(config.store_timing)
        ui.store_length.setChecked(config.store_content_length)

        store_resp_if: QLineEdit = ui.store_resp_if
        store_resp_if.setText(config.store_response_if)
        ui.terminate_if.setText(config.terminate_attack_if)

    def submit(self):
        ui = self.ui
        config = self.config
        store_resp: QCheckBox = ui.store_resp
        config.store_raw_response = store_resp.isChecked()
        config.store_timing = ui.store_timing.isChecked()
        config.store_content_length = ui.store_length.isChecked()

        store_resp_if: QLineEdit = ui.store_resp_if
        config.store_response_if = store_resp_if.text()
        config.terminate_attack_if = ui.terminate_if.text()

        self.callback(config)
        self.close()
