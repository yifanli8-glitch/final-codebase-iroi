"""
LabDetailPanel - 

"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..widgets import LabButton, BackButton


class LabDetailPanel(QWidget):
    """"""
    
    question_selected = pyqtSignal(str, str, int)  # (lab_name, section_name, question_num)
    back_clicked = pyqtSignal()
    lecture_review_clicked = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000011;")
        self.current_lab = 1
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        
        back_btn = BackButton()
        back_btn.clicked.connect(self.back_clicked.emit)
        top_bar.addWidget(back_btn)
        
        self.lab_label = QLabel("LAB 1")
        self.lab_label.setFont(QFont("Silkscreen", 14))
        self.lab_label.setStyleSheet("color: #888888;")
        top_bar.addWidget(self.lab_label)
        top_bar.addStretch()
        
        layout.addLayout(top_bar)
        
        layout.addSpacing(30)
        
        self.title_label = QLabel("LAB 1")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Silkscreen", 48)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #7CDAFF;")
        layout.addWidget(self.title_label)
        
        layout.addSpacing(40)
        
        lecture_btn = QPushButton("LECTURE REVIEW")
        lecture_btn.setFixedSize(380, 70)
        lecture_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        lecture_btn.setFont(QFont("Silkscreen", 24))
        lecture_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(124, 218, 255, 0.8);
                color: #FFFFFF;
                border: none;
                border-radius: 35px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(124, 218, 255, 1.0);
            }
        """)
        lecture_btn.clicked.connect(self.lecture_review_clicked.emit)
        layout.addWidget(lecture_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(50)
        
        # Section 1: POWER SUPPLY & MULTIMETER
        self._add_section(layout, "🔋", "POWER SUPPLY & MULTIMETER", 4, "power_supply")
        
        layout.addSpacing(30)
        
        # Section 2: OSCILLOSCOPE & SIGNAL GENERATOR
        self._add_section(layout, "📟", "OSCILLOSCOPE &\nSIGNAL GENERATOR", 3, "oscilloscope")
        
        layout.addStretch()
    
    def _add_section(self, parent_layout, icon: str, title: str, num_questions: int, section_id: str):
        """"""
        title_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Noto Color Emoji", 20))
        icon_label.setStyleSheet("color: #4ade80;")
        title_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Silkscreen", 20))
        title_label.setStyleSheet("color: #FFFFFF;")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        parent_layout.addLayout(title_layout)
        parent_layout.addSpacing(20)
        
        btn_container = QWidget()
        btn_layout = QGridLayout(btn_container)
        btn_layout.setSpacing(50)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        
        for i in range(num_questions):
            btn = LabButton(f"Q {i + 1}")
            btn.clicked.connect(
                lambda checked, q=i+1, s=section_id: 
                self.question_selected.emit(f"LAB {self.current_lab}", s, q)
            )
            row = i // 3
            col = i % 3
            btn_layout.addWidget(btn, row, col, alignment=Qt.AlignmentFlag.AlignLeft)
        
        parent_layout.addWidget(btn_container)
    
    def set_lab(self, lab_num: int):
        """"""
        self.current_lab = lab_num
        self.lab_label.setText(f"LAB {lab_num}")
        self.title_label.setText(f"LAB {lab_num}")
