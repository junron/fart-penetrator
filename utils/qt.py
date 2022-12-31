from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem


def make_int_item(val: int):
    item = QTableWidgetItem()
    item.setData(Qt.ItemDataRole.DisplayRole, val)
    return item
