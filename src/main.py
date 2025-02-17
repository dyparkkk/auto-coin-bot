# main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from gui.market_status import MarketStatus
from gui.trading_ui import TradingTab
from gui.future import FutureTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("코인 자동 매매 봇")
        self.setGeometry(100, 100, 600, 400)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        tab_widget = QTabWidget()
        
        # 각 탭에 해당하는 위젯 생성
        market_tab = MarketStatus()
        trading_tab = TradingTab()
        future_tab = FutureTab()
        
        # 탭 추가 (탭 이름 지정)
        tab_widget.addTab(market_tab, "시장현황")
        tab_widget.addTab(trading_tab, "매매")
        tab_widget.addTab(future_tab, "미정")
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
