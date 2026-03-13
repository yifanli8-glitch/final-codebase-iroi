from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..widgets import LabButton, BackButton


class LabSelectPanel(QWidget):
    
    lab_selected = pyqtSignal(int)
    back_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000011;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)
        
        back_btn = BackButton()
        back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        layout.addSpacing(30)
        
        title = QLabel("PLEASE SELECT\nA LAB SECTION")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Silkscreen", 48)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #C9D9E8;")
        layout.addWidget(title)
        
        layout.addSpacing(80)
        
        section_title = QLabel("SENSOR AND CIRCUIT")
        section_title.setFont(QFont("Silkscreen", 32))
        section_title.setStyleSheet("color: #C9D9E8;")
        section_title.setContentsMargins(65, 0, 0, 0)
        layout.addWidget(section_title, alignment=Qt.AlignmentFlag.AlignLeft)
        
        layout.addSpacing(30)
        
        grid_container = QWidget()
        grid_layout = QGridLayout(grid_container)
        grid_layout.setSpacing(50)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        
        for i in range(8):
            btn = LabButton(f"LAB {i + 1}")
            btn.clicked.connect(lambda checked, lab=i+1: self.lab_selected.emit(lab))
            row = i // 3
            col = i % 3
            grid_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(grid_container, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch()
