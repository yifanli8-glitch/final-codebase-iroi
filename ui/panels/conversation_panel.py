
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ConversationPanel(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000000;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(50, 100, 50, 100)
        layout.setSpacing(50)
        
        self.user_text_label = QLabel("")
        self.user_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_text_label.setWordWrap(True)
        user_font = QFont("Silkscreen", 36)
        self.user_text_label.setFont(user_font)
        self.user_text_label.setStyleSheet("color: #888888;")
        self.user_text_label.setFixedWidth(980)
        layout.addWidget(self.user_text_label)
        
        layout.addStretch(1)
        
        self.robot_text_label = QLabel("")
        self.robot_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.robot_text_label.setWordWrap(True)
        robot_font = QFont("Silkscreen", 56)
        robot_font.setBold(True)
        self.robot_text_label.setFont(robot_font)
        self.robot_text_label.setStyleSheet("color: #7CDAFF;")
        self.robot_text_label.setFixedWidth(980)
        layout.addWidget(self.robot_text_label)
        
        layout.addStretch(1)
        
        self.status_label = QLabel("🎤 Listening...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        status_font = QFont("Silkscreen", 24)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #4ade80;")
        layout.addWidget(self.status_label)
    
    def set_user_text(self, text: str):
        self.user_text_label.setText(f'"{text}"')
    
    def set_robot_text(self, text: str):
        self.robot_text_label.setText(text)
    
    def set_status(self, status: str):
        self.status_label.setText(status)
    
    def clear(self):
        self.user_text_label.setText("")
        self.robot_text_label.setText("")
        self.status_label.setText("🎤 Listening...")
