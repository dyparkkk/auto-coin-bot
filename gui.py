# gui.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QTextEdit, QPushButton
)
from fileStorage import save_input_values  # 입력값 저장 함수
from gateIoApi import get_uni_currencies  # Gate API 함수

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
        self.input_box1.setPlaceholderText("첫 번째 입력을 여기에 입력하세요.")
        
        # 두 번째 입력 박스
        self.input_box2 = QLineEdit(self)
        self.input_box2.setPlaceholderText("두 번째 입력을 여기에 입력하세요.")
        
        # 출력 박스 (여러 줄 텍스트 표시, 읽기 전용)
        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        
        # 기존 버튼들
        self.btn_transfer = QPushButton("전송", self)
        self.btn_clear = QPushButton("클리어", self)
        # 새로 추가한 Gate API 호출 버튼
        self.btn_gate_api = QPushButton("Gate API 요청", self)
        
        # 버튼 클릭 이벤트 연결
        self.btn_transfer.clicked.connect(self.transfer_text)
        self.btn_clear.clicked.connect(self.clear_text)
        self.btn_gate_api.clicked.connect(self.call_gate_api)
        
        # 레이아웃 구성
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_box1)
        main_layout.addWidget(self.input_box2)
        main_layout.addWidget(self.output_box)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_transfer)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_gate_api)
        
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
    
    def transfer_text(self):
        # 두 입력 박스의 텍스트 가져오기
        text1 = self.input_box1.text()
        text2 = self.input_box2.text()
        
        # 출력 박스에 두 입력값 표시
        self.output_box.setPlainText(f"첫 번째 입력: {text1}\n두 번째 입력: {text2}")
        
        # 입력값 저장 함수 호출
        save_input_values(text1, text2)
    
    def clear_text(self):
        # 입력 박스와 출력 박스 내용 초기화
        self.input_box1.clear()
        self.input_box2.clear()
        self.output_box.clear()
    
    def call_gate_api(self):
        # Gate API 함수를 호출하여 응답 결과를 출력 박스에 표시
        result = get_uni_currencies()
        self.output_box.setPlainText(result)
