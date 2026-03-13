
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap


class MapPanel(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000000;")
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout.addStretch(1)
        
        map_title = QLabel("MAP")
        map_title_font = QFont("Silkscreen", 48)
        map_title_font.setBold(True)
        map_title.setFont(map_title_font)
        map_title.setStyleSheet("color: #7CDAFF;")
        map_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(map_title)
        
        layout.addSpacing(50)
        
        self.map_label = QLabel()
        self.map_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        map_path = os.path.join(script_dir, "Map.png")
        
        if os.path.exists(map_path):
            pixmap = QPixmap(map_path)
            scaled_pixmap = pixmap.scaledToWidth(980, Qt.TransformationMode.SmoothTransformation)
            if scaled_pixmap.height() > 1600:
                scaled_pixmap = pixmap.scaledToHeight(1600, Qt.TransformationMode.SmoothTransformation)
            self.map_label.setPixmap(scaled_pixmap)
        else:
            self.map_label.setText("Map.png not found")
            self.map_label.setStyleSheet("color: #ef4444; font-size: 24px;")
        
        layout.addWidget(self.map_label)
        
        layout.addStretch(1)
    
    def update_map(self, map_path: str):
        if os.path.exists(map_path):
            pixmap = QPixmap(map_path)
            scaled_pixmap = pixmap.scaledToWidth(980, Qt.TransformationMode.SmoothTransformation)
            if scaled_pixmap.height() > 1600:
                scaled_pixmap = pixmap.scaledToHeight(1600, Qt.TransformationMode.SmoothTransformation)
            self.map_label.setPixmap(scaled_pixmap)
        else:
            self.map_label.setText("Map not found")
            self.map_label.setStyleSheet("color: #ef4444; font-size: 24px;")
