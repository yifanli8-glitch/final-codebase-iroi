from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class BackButton(QPushButton):
    
    def __init__(self, parent=None):
        super().__init__("◀", parent)
        self.setFixedSize(60, 60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Silkscreen", 20))
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(124, 218, 255, 0.8);
                color: #FFFFFF;
                border: none;
                border-radius: 30px;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: rgba(124, 218, 255, 0.95);
            }
            QPushButton:pressed {
                background-color: rgba(100, 180, 220, 0.9);
            }
            QPushButton:focus {
                outline: none;
                border: none;
            }
        """)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
