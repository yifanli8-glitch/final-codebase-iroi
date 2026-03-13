
import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import QFont, QMovie


class DefaultPanel(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000000;")
        
        self.hint_messages = [
            'Say "Hi Iroi" to wake me up',
            "I can help you with your lab",
            "I'm your TA robot"
        ]
        self.current_hint_index = 0
        self.current_char_index = 0
        self.typing_timer = None
        self.display_timer = None
        
        self.init_ui()
        
        QTimer.singleShot(3000, self.show_eyes)
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(80)
        main_layout.setContentsMargins(50, 50, 50, 50)
        
        main_layout.addStretch(1)
        
        self.speech_label = QLabel("", self)
        self.speech_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        speech_font = QFont("Silkscreen", 48)
        speech_font.setBold(True)
        self.speech_label.setFont(speech_font)
        self.speech_label.setStyleSheet("color: #C9D9E8;")
        self.speech_label.setFixedSize(1080, 100)
        self.speech_label.move(0, 200)
        self.speech_label.hide()
        
        self.hint_label = QLabel("", self)
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hint_label.setWordWrap(True)
        hint_font = QFont("Silkscreen", 42)
        self.hint_label.setFont(hint_font)
        self.hint_label.setStyleSheet("color: #7CDAFF;")
        self.hint_label.setFixedSize(1000, 150)
        self.hint_label.move(40, 320)
        self.hint_label.hide()
        
        self.welcome_label = QLabel("WELCOME\nTO DOGIX")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Silkscreen", 96)
        font.setBold(True)
        self.welcome_label.setFont(font)
        self.welcome_label.setStyleSheet("color: #C9D9E8;")
        main_layout.addWidget(self.welcome_label)
        
        self.eyes_label = QLabel()
        self.eyes_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        gif_path = os.path.join(script_dir, "Basic_blink.gif")
        self.eyes_movie = QMovie(gif_path)
        
        self.eyes_movie.jumpToFrame(0)
        original_size = self.eyes_movie.currentImage().size()
        
        if original_size.width() > 0:
            max_width = 980
            scale_factor = min(0.6, max_width / original_size.width())
            new_width = int(original_size.width() * scale_factor)
            new_height = int(original_size.height() * scale_factor)
            self.eyes_movie.setScaledSize(QSize(new_width, new_height))
        
        self.eyes_label.setMovie(self.eyes_movie)
        self.eyes_label.hide()
        main_layout.addWidget(self.eyes_label)
        
        main_layout.addStretch(1)
    
    def show_eyes(self):
        self.welcome_label.hide()
        self.eyes_label.show()
        self.eyes_movie.start()
        
        self.hint_label.show()
        self.start_hint_carousel()
    
    def set_speech_text(self, text: str):
        if text:
            self.speech_label.setText(text)
            self.speech_label.show()
        else:
            self.speech_label.hide()
    
    def start_animation(self):
        self.eyes_movie.start()
    
    def stop_animation(self):
        self.eyes_movie.stop()
    
    
    def start_hint_carousel(self):
        self.current_hint_index = 0
        self.start_typing_effect()
    
    def start_typing_effect(self):
        self.current_char_index = 0
        self.hint_label.setText("")
        
        if self.typing_timer:
            self.typing_timer.stop()
        if self.display_timer:
            self.display_timer.stop()
        
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.type_next_char)
        self.typing_timer.start(50)
    
    def type_next_char(self):
        current_message = self.hint_messages[self.current_hint_index]
        
        if self.current_char_index < len(current_message):
            self.hint_label.setText(current_message[:self.current_char_index + 1])
            self.current_char_index += 1
        else:
            self.typing_timer.stop()
            
            self.display_timer = QTimer()
            self.display_timer.setSingleShot(True)
            self.display_timer.timeout.connect(self.next_hint_message)
            self.display_timer.start(3000)
    
    def next_hint_message(self):
        self.current_hint_index = (self.current_hint_index + 1) % len(self.hint_messages)
        self.start_typing_effect()
    
    def stop_hint_carousel(self):
        if self.typing_timer:
            self.typing_timer.stop()
        if self.display_timer:
            self.display_timer.stop()
        self.hint_label.hide()