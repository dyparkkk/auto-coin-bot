from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton, QComboBox, QLabel, QCheckBox
)
from trading_strategy.breakthrough import breakthrough_strategy
from gateIoApi import  get_candlesticks, get_list_unified_accounts  
from trading import trading
from trading_manager import tm

class TradingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.get_my_usdt()
    
    def init_ui(self):
        # --- 상단 한 줄: 입력, 검색 버튼, 드롭다운, amount, USDT 정보 ---
        self.coin_name = QComboBox(self)
        self.coin_name.addItems(["btc", "eth", "sol", ""])
        self.coin_name.setFixedWidth(100)
        
        self.btn_transfer = QPushButton("검색", self)
        
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(['1d', "15m", "1h", "4h"])
        self.combo_box.currentIndexChanged.connect(self.handle_dropdown_change)

        self.amount = QLineEdit(self)
        self.amount.setPlaceholderText("amount")

        label_usdt = QLabel("available USDT", self)
        self.my_usdt = QLineEdit(self)
        self.my_usdt.setPlaceholderText("my usdt")
        self.my_usdt.setReadOnly(True)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.coin_name, 6)
        top_layout.addWidget(self.btn_transfer, 1)
        top_layout.addWidget(self.combo_box, 1)
        top_layout.addWidget(self.amount, 1)
        top_layout.addWidget(label_usdt)
        top_layout.addWidget(self.my_usdt, 1)
        
        # --- 중간 영역: 좌우로 나눈 출력 영역 ---
        # 왼쪽 영역: Long/Short 및 breakthrough strategy 항목 추가
        left_layout = QVBoxLayout()
        left_label = QLabel("Long/Short", self)
        left_layout.addWidget(left_label)
        
        # breakthrough strategy 체크박스 추가
        self.breakthrough_checkbox = QCheckBox("Breakthrough Strategy", self)
        left_layout.addWidget(self.breakthrough_checkbox)
        
        # 단기 이평선 입력 칸 (예: 20)
        short_ma_layout = QHBoxLayout()
        short_ma_label = QLabel("단기 이평선:", self)
        self.short_ma_input = QLineEdit(self)
        self.short_ma_input.setPlaceholderText("예: 20")
        short_ma_layout.addWidget(short_ma_label)
        short_ma_layout.addWidget(self.short_ma_input)
        left_layout.addLayout(short_ma_layout)
        
        # 장기 이평선 입력 칸 (예: 50)
        long_ma_layout = QHBoxLayout()
        long_ma_label = QLabel("장기 이평선:", self)
        self.long_ma_input = QLineEdit(self)
        self.long_ma_input.setPlaceholderText("예: 50")
        long_ma_layout.addWidget(long_ma_label)
        long_ma_layout.addWidget(self.long_ma_input)
        left_layout.addLayout(long_ma_layout)
        
        # 기존 출력 영역 (예: 전략 결과 등 출력)
        self.long_output = QTextEdit(self)
        self.long_output.setReadOnly(True)
        left_layout.addWidget(self.long_output)
        
        # 오른쪽 영역: 매매 진행중인 전략 출력
        right_layout = QVBoxLayout()
        right_label = QLabel("working tradings", self)  
        right_layout.addWidget(right_label)
        self.short_output = QTextEdit(self)
        self.short_output.setReadOnly(True)
        right_layout.addWidget(self.short_output)
        
        middle_layout = QHBoxLayout()
        middle_layout.addLayout(left_layout)
        middle_layout.addLayout(right_layout)
        
        # --- 하단 영역: 추가 버튼들 ---
        self.btn_start = QPushButton("매매 시작", self)
        self.btn_refresh = QPushButton("새로고침", self)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.btn_start)
        bottom_layout.addWidget(self.btn_refresh)
        
        # --- 이벤트 연결 ---
        self.btn_transfer.clicked.connect(self.search_coin)
        self.btn_start.clicked.connect(self.start)
        self.btn_refresh.clicked.connect(self.refresh)
        
        # --- 전체 레이아웃 구성 ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
    
    def search_coin(self):
        text1 = self.coin_name.currentText()
        result = get_candlesticks(text1, "1h")
        header = (
            "각 데이터의 의미:\n"
            "1. 초 단위 유닉스 타임스탬프\n"
            "2. 견적 통화 거래량\n"
            "3. 종가\n"
            "4. 최고가\n"
            "5. 최저가\n"
            "6. 시가\n"
            "7. 기저 통화 거래량\n"
            "8. 캔들 완성 여부 (true: 완료, false: 미완료)\n\n"
            "결과:\n"
        )
        formatted_result = header + "\n".join(["\t".join(item) for item in result])
        self.long_output.setPlainText(formatted_result)
    
    def start(self):
        
        print(self.coin_name.currentText())
        print(self.amount.text())
        trading_id = tm.add_trading(coin=self.coin_name.currentText(), amount=self.amount.text(), position="none")
        pass
        

    def refresh(self):
        # USDT 값을 새로고침
        self.get_my_usdt()
        # TradingManager에 등록된 트레이딩 목록을 가져와서 표시
        tradings = tm.get_tradings()
        if tradings:
            formatted = "\n".join([f"ID: {tid}, {data}" for tid, data in tradings.items()])
        else:
            formatted = "등록된 트레이딩 없음."
        self.short_output.setPlainText(formatted)
    
    def handle_dropdown_change(self, index):
        selected_option = self.combo_box.currentText()
        # 필요시 선택된 옵션에 따른 동작 구현 가능
        pass
    
    def get_my_usdt(self):
        accounts = get_list_unified_accounts()
        value = accounts.balances.get('USDT').available
        formatted_value = "{:.2f}".format(float(value))
        self.my_usdt.setText(formatted_value)
