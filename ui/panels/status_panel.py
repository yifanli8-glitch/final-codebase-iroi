from datetime import datetime
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from ..widgets import StatusItem


class StatusPanel(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000000;")
        
        self.battery_level = 85
        self.mic_status = True
        self.video_status = True
        self.wave_detected = False
        
        self.init_ui()
        self.start_timer()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 80, 50, 80)
        layout.setSpacing(30)
        
        title = QLabel("SYSTEM STATUS")
        title_font = QFont("Silkscreen", 48)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #7CDAFF;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(50)
        
        self.time_item = StatusItem("🕐", "TIME", "00:00:00")
        layout.addWidget(self.time_item)
        
        self.date_item = StatusItem("📅", "DATE", "2024-01-01")
        layout.addWidget(self.date_item)
        
        self.battery_item = StatusItem("🔋", "BATTERY", "85%")
        layout.addWidget(self.battery_item)
        
        self.mic_item = StatusItem("🎤", "MICROPHONE", "READY")
        layout.addWidget(self.mic_item)
        
        self.video_item = StatusItem("📷", "CAMERA", "READY")
        layout.addWidget(self.video_item)
        
        self.wave_item = StatusItem("👋", "WAVE DETECT", "NO")
        layout.addWidget(self.wave_item)
        
        layout.addStretch()
        
        hint = QLabel("Press 1-4 to switch mode")
        hint_font = QFont("Silkscreen", 20)
        hint.setFont(hint_font)
        hint.setStyleSheet("color: #555555;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)
    
    def start_timer(self):
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_status)
        self.update_timer.start(1000)
        self.update_status()
    
    def update_status(self):
        now = datetime.now()
        self.time_item.set_value(now.strftime("%H:%M:%S"))
        self.date_item.set_value(now.strftime("%Y-%m-%d"))
        
        battery_color = "#4ade80" if self.battery_level > 50 else "#fbbf24" if self.battery_level > 20 else "#ef4444"
        self.battery_item.set_value(f"{self.battery_level}%", battery_color)
        
        mic_text = "READY" if self.mic_status else "OFF"
        mic_color = "#4ade80" if self.mic_status else "#ef4444"
        self.mic_item.set_value(mic_text, mic_color)
        
        video_text = "READY" if self.video_status else "OFF"
        video_color = "#4ade80" if self.video_status else "#ef4444"
        self.video_item.set_value(video_text, video_color)
        
        wave_text = "YES!" if self.wave_detected else "NO"
        wave_color = "#4ade80" if self.wave_detected else "#888888"
        self.wave_item.set_value(wave_text, wave_color)
    
    def set_battery(self, level: int):
        self.battery_level = level
    
    def set_mic_status(self, status: bool):
        self.mic_status = status
    
    def set_video_status(self, status: bool):
        self.video_status = status
    
    def set_wave_detected(self, detected: bool):
        self.wave_detected = detected
