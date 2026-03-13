"""
StatusItem - 
、
"""
from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QFont


class StatusItem(QFrame):
    """"""
    
    def __init__(self, icon: str, label: str, value: str = "---", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 2px solid #7CDAFF;
                border-radius: 20px;
            }
        """)
        self.setFixedHeight(120)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(20)
        
        icon_label = QLabel(icon)
        icon_font = QFont("Noto Color Emoji", 40)
        icon_label.setFont(icon_font)
        icon_label.setStyleSheet("border: none;")
        icon_label.setFixedWidth(80)
        layout.addWidget(icon_label)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)
        
        label_widget = QLabel(label)
        label_font = QFont("Silkscreen", 18)
        label_widget.setFont(label_font)
        label_widget.setStyleSheet("color: #888888; border: none;")
        text_layout.addWidget(label_widget)
        
        self.value_label = QLabel(value)
        value_font = QFont("Silkscreen", 28)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        self.value_label.setStyleSheet("color: #7CDAFF; border: none;")
        text_layout.addWidget(self.value_label)
        
        layout.addLayout(text_layout)
        layout.addStretch()
    
    def set_value(self, value: str, color: str = "#7CDAFF"):
        """"""
        self.value_label.setText(value)
        self.value_label.setStyleSheet(f"color: {color}; border: none;")
