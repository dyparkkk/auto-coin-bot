# market_status.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class MarketStatus(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("시장현황 탭 내용 (추후 구현)")
        layout.addWidget(label)
        self.setLayout(layout)
