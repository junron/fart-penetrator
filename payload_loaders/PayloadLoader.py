from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from penetrator import PenetratorWindow


class PayloadLoader:
    def __init__(self, penetrator: PenetratorWindow):
        self.penetrator = penetrator
        self.ui = self.penetrator.ui
