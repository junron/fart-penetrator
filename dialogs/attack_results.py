import asyncio
import functools
from typing import List

import requests
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QTableWidgetItem, QHeaderView, QProgressBar, QPushButton

from backend.HttpWorker import HttpWorker
from dialogs.response_detail import ResponseDetail
from models.AttackConfig import AttackConfig
from models.StoredResponse import StoredResponse
from utils.qt import make_int_item


class AttackResults(QDialog):
    progress = pyqtSignal(int, name="progress")
    num_done = 0
    responses: List[StoredResponse | None]
    num_variables = 0
    worker: HttpWorker | None = None

    def __init__(self, request_payloads: List[tuple[str]], http_request: str, config: AttackConfig):
        super(AttackResults, self).__init__()
        self.ui = uic.loadUi("./dialogs/attack_dialog.ui", self)
        self.request_payloads = request_payloads
        self.num_variables = len(request_payloads[0])
        self.http_request = http_request
        self.config = config
        self.num_reqs = len(request_payloads)
        self.ui.progress_bar.setMaximum(self.num_reqs)
        self.progress.connect(self.ui.progress_bar.setValue)
        self.responses = [None for _ in range(self.num_reqs)]
        self.table_widget = self.ui.attack_results_table
        self.ui.stop_btn.clicked.connect(lambda x: self.cancel())
        self.setup_table()
        self.show()

    def setup_table(self):
        for i in range(2, self.num_variables + 1):
            self.table_widget.insertColumn(i)
            self.table_widget.setColumnCount(self.table_widget.columnCount())
        self.table_widget.setHorizontalHeaderLabels(
            ["Num"] + [f"FUZZ{n}" for n in range(self.num_variables)] + self.config.table_headers())
        for pl in self.request_payloads:
            self.add_row(pl)
        for i in range(4 + self.num_variables):
            self.ui.attack_results_table.horizontalHeader() \
                .setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        self.table_widget.cellDoubleClicked.connect(
            lambda row, col: self.show_response(int(self.table_widget.item(row, 0).text())))

    def add_row(self, payload):
        table_widget = self.table_widget
        row_pos = table_widget.rowCount()
        table_widget.insertRow(row_pos)
        table_widget.setRowCount(table_widget.rowCount())
        table_widget.setItem(row_pos, 0, make_int_item(row_pos))
        for i in range(self.num_variables):
            table_widget.setItem(row_pos, i + 1, QTableWidgetItem(payload[i]))

    def handle_request_complete(self, index: int, response: requests.Response, timing_ms: int):
        resp = StoredResponse.from_py_response(response, timing_ms, self.config)
        self.table_widget.setItem(index, self.num_variables + 1, make_int_item(resp.status_code))
        if self.config.store_timing:
            self.table_widget.setItem(index, self.num_variables + 2, make_int_item(timing_ms))
        if self.config.store_content_length:
            self.table_widget.setItem(index, self.num_variables + 3, make_int_item(resp.content_length))
        self.responses[index] = resp
        # Definitely no race condition here
        self.num_done += 1
        self.progress.emit(self.num_done)
        if self.num_reqs == self.num_done:
            self.table_widget.setSortingEnabled(True)

    def show_response(self, index):
        resp = self.responses[index]
        if resp is None:
            return
        resp_detail = ResponseDetail(index, resp)
        resp_detail.exec()

    def start(self):
        loop = asyncio.get_event_loop()
        worker = HttpWorker(self.http_request, self.request_payloads,
                            lambda i, res, timing: self.handle_request_complete(i, res, timing))
        self.worker = worker
        asyncio.ensure_future(worker.run(), loop=loop)

    def cancel(self):
        try:
            self.worker.cancel()
            self.table_widget.setSortingEnabled(True)
            for i, response in enumerate(self.responses):
                if response is None:
                    self.table_widget.setItem(i, self.num_variables + 1, QTableWidgetItem("Cancelled"))
            pb: QProgressBar = self.ui.progress_bar
            pb.setDisabled(True)
            stop_btn: QPushButton = self.ui.stop_btn
            stop_btn.setDisabled(True)
        except Exception as e:
            print(e)
