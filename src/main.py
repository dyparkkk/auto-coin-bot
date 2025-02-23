# main.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout
from gui.market_status import MarketStatus
from gui.trading_ui import TradingTab
from gui.future import FutureTab
from trading_manager import tm

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("코인 자동 매매 봇")
        self.setGeometry(100, 100, 1100, 800)
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
        tab_widget.setCurrentIndex(1)
        
        layout.addWidget(tab_widget)
        self.setLayout(layout)

    def closeEvent(self, event):
        # 창이 닫힐 때 tm.stop() 호출
        tm.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    tm.start()
    sys.exit( app.exec_())

