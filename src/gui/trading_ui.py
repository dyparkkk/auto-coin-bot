from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton, QComboBox, QLabel
)
from trading_strategy.breakthrough import breakthrough_strategy
from gateIoApi import get_uni_currencies, get_candlesticks, get_list_unified_accounts  

class TradingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.get_my_usdt()
    
    def init_ui(self):
        # --- 상단 한 줄: 입력, 검색 버튼, 드롭다운 ---
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("coin 이름")
        self.input_box1.setFixedWidth(100)
        
        self.btn_transfer = QPushButton("검색", self)
        
        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["1h", "4h", "1d"])
        self.combo_box.currentIndexChanged.connect(self.handle_dropdown_change)

        label_usdt = QLabel("available USDT", self)
        self.my_usdt = QLineEdit(self)
        self.my_usdt.setPlaceholderText("my usdt")
        self.my_usdt.setReadOnly(True)
        
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.input_box1, 6)
        top_layout.addWidget(self.btn_transfer, 1)
        top_layout.addWidget(self.combo_box, 2)
        top_layout.addWidget(label_usdt)
        top_layout.addWidget(self.my_usdt, 1)
        
        # --- 중간 영역: 좌우로 나눈 출력 영역 ---
        # 왼쪽: Long 영역
        left_layout = QVBoxLayout()
        left_label = QLabel("Long", self)
        left_layout.addWidget(left_label)
        self.long_output = QTextEdit(self)
        self.long_output.setReadOnly(True)
        left_layout.addWidget(self.long_output)
        
        # 오른쪽: Short 영역
        right_layout = QVBoxLayout()
        right_label = QLabel("Short", self)
        right_layout.addWidget(right_label)
        self.short_output = QTextEdit(self)
        self.short_output.setReadOnly(True)
        right_layout.addWidget(self.short_output)
        
        middle_layout = QHBoxLayout()
        middle_layout.addLayout(left_layout)
        middle_layout.addLayout(right_layout)
        
        # --- 하단 영역: 추가 버튼들 ---
        self.btn_test = QPushButton("test", self)
        self.btn_gate_api = QPushButton("Gate API 요청", self)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.btn_test)
        bottom_layout.addWidget(self.btn_gate_api)
        
        # --- 이벤트 연결 ---
        self.btn_transfer.clicked.connect(self.search_coin)
        self.btn_test.clicked.connect(self.test_api)
        self.btn_gate_api.clicked.connect(self.call_gate_api)
        
        # --- 전체 레이아웃 구성 ---
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(middle_layout)
        main_layout.addLayout(bottom_layout)
        
        self.setLayout(main_layout)
    
    def search_coin(self):
        text1 = self.input_box1.text()
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
        # 왼쪽(LONG) 출력 영역에 결과 출력
        self.long_output.setPlainText(formatted_result)
    
    def test_api(self):
        
        print(breakthrough_strategy('btc', '1h', 1, 'long'))


    def call_gate_api(self):
        result = get_uni_currencies()
        # 오른쪽(SHORT) 출력 영역에 결과 출력
        self.short_output.setPlainText(result)
    
    def handle_dropdown_change(self, index):
        selected_option = self.combo_box.currentText()
        # 드롭다운 선택에 따른 동작 예시 (여기서는 왼쪽 영역에 메시지 출력)
        if selected_option == "1h":
            self.long_output.append("옵션1 선택됨: 추가 정보를 표시합니다.")
        elif selected_option == "4h":
            self.long_output.append("옵션2 선택됨: 다른 동작을 수행합니다.")
        elif selected_option == "1d":
            self.long_output.append("옵션3 선택됨: 기본 동작입니다.")
        
    def get_my_usdt(self):
        accounts = get_list_unified_accounts()
        value = accounts.balances.get('USDT').available
        formatted_value = "{:.2f}".format(float(value))
        self.my_usdt.setText(formatted_value) 
    