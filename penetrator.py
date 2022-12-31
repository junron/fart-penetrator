from __future__ import annotations

import asyncio
import itertools
from typing import List

from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QHeaderView, QTableWidget
from qasync import QEventLoop

from dialogs.attack_results import AttackResults
from models.AttackConfig import AttackConfig
from payload_loaders.PayloadFromFile import PayloadFromFile
from payload_loaders.PayloadFromIntRange import PayloadFromIntRange
from payload_loaders.PayloadFromWordlist import PayloadFromWordlist
from utils.qt import make_int_item


class PenetratorWindow(QMainWindow):
    payload_sets: List[List[str]] = []
    table_widget: QTableWidget
    selected_row: None

    def __init__(self):
        super(PenetratorWindow, self).__init__()
        self.ui = uic.loadUi('main.ui', self)
        self.ui.launch_attack_btn.clicked.connect(self.launch_attack)
        self.table_widget = self.ui.payload_table_widget
        self.table_widget.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table_widget.keyPressEvent = lambda event: self.handle_payload_set_delete(event)
        self.table_widget.cellPressed.connect(lambda row, col: self.handle_table_click(row, col))
        PayloadFromFile(self)
        PayloadFromWordlist(self)
        PayloadFromIntRange(self)
        self.show()

    def handle_table_click(self, row, col):
        self.selected_row = row

    def handle_payload_set_delete(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Delete:
            if self.selected_row is not None:
                self.table_widget.removeRow(self.selected_row)
                self.payload_sets.pop(self.selected_row)
                self.selected_row = None
                self.update_variable_numbers()
        return QTableWidget.keyPressEvent(self.table_widget, event)

    def update_variable_numbers(self):
        for i in range(len(self.payload_sets)):
            self.table_widget.setItem(i, 0, QTableWidgetItem(f"FUZZ{i}"))

    def launch_attack(self):
        try:
            text = self.ui.http_request_input.toPlainText()
            attack_config = AttackConfig(True, True, True)
            attack = AttackResults(list(itertools.product(*self.payload_sets)), text, attack_config)
            attack.start()
            attack.exec()
        except Exception as e:
            print(e)

    def add_payload_set(self, payload_set: List[str], source: str):
        self.payload_sets.append(payload_set)
        table_widget = self.ui.payload_table_widget
        row_pos = table_widget.rowCount()
        table_widget.insertRow(row_pos)
        table_widget.setRowCount(table_widget.rowCount())
        table_widget.setItem(row_pos, 0, QTableWidgetItem(f"FUZZ{row_pos}"))
        table_widget.setItem(row_pos, 1, QTableWidgetItem(source))
        table_widget.setItem(row_pos, 2, make_int_item(len(payload_set)))


if __name__ == '__main__':
    app = QApplication([])
    window = PenetratorWindow()
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    window.show()
    with loop:
        loop.run_forever()
