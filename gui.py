# gui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton
)
from fileStorage import save_input_values  # 입력값 저장 함수
from gateIoApi import get_uni_currencies, get_candlesticks  # Gate API 함수

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 GUI 앱")
        # 높이를 조금 늘려서 버튼이 많아도 잘 보이도록 함
        self.setGeometry(100, 100, 400, 400)
        self.init_ui()
    
    def init_ui(self):
        # 첫 번째 입력 박스
        self.input_box1 = QLineEdit(self)
        self.input_box1.setPlaceholderText("coin 이름")
        self.btn_transfer = QPushButton("검색", self)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.input_box1, 6)
        h_layout.addWidget(self.btn_transfer, 1)
        
        
        # 두 번째 입력 박스
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("두 번째 입력을 여기에 입력하세요.")
        
        # 출력 박스 (여러 줄 텍스트 표시, 읽기 전용)
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        
       
        self.btn_clear = QPushButton("클리어", self)
        # 새로 추가한 Gate API 호출 버튼
        self.btn_gate_api = QPushButton("Gate API 요청", self)
        
        # 버튼 클릭 이벤트 연결
        self.btn_transfer.clicked.connect(self.search_coin)
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_gate_api.clicked.connect(self.call_gate_api)
        
        # =====================================================================================
        # 레이아웃 구성
        # =====================================================================================
        main_layout = QVBoxLayout()
        main_layout.addLayout(h_layout)
        

        main_layout.addWidget(self.input_box2)
        main_layout.addWidget(self.output_box)
        
        btn_layout = QHBoxLayout()
        
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_gate_api)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
    
    def search_coin(self):
        text1 = self.input_box1.text()
        result = get_candlesticks(text1, "1h")
        formatted_result = "\n".join(["\t".join(item) for item in result])
        self.output_box.setPlainText(formatted_result) 
    
    def clear_text(self):
        # 입력 박스와 출력 박스 내용 초기화
        self.input_box1.clear()
        self.input_box2.clear()
        self.output_box.clear()
    
    def call_gate_api(self):
        # Gate API 함수를 호출하여 응답 결과를 출력 박스에 표시
        result = get_uni_currencies()
        self.output_box.setPlainText(result)
