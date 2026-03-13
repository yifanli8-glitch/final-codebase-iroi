"""
QAChatPanel - 
， RAG 
"""
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QPushButton
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap
import threading
import os
import tempfile
import cv2

from ..widgets import BackButton, CameraPopup


class QAChatPanel(QWidget):
    """"""
    
    back_clicked = pyqtSignal()
    message_sent = pyqtSignal(str)
    chat_clicked = pyqtSignal()
    
    _add_user_message = pyqtSignal(str)
    _add_bot_message = pyqtSignal(str)
    _set_status = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000011;")
        self.current_path = ""
        self.question_text = ""
        self.question_num = 1
        self.conversation_stage = 0
        self.messages = []  # [(is_user, text, has_image), ...]
        
        self.voice_assistant = None
        self.is_listening = False
        self.listen_thread = None
        
        self.camera_popup = None
        self.pending_image = None
        
        self._add_user_message.connect(lambda text: self.add_message(text, is_user=True))
        self._add_bot_message.connect(lambda text: self.add_message(text, is_user=False))
        self._set_status.connect(self._update_status_label)
        
        self.init_ui()
        self.init_camera_popup()
    
    def mousePressEvent(self, event):
        """"""
        super().mousePressEvent(event)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 40, 50, 50)
        layout.setSpacing(15)
        
        top_bar = QHBoxLayout()
        
        self.path_label = QLabel("LAB 1/POWER SUPPLY AND MULTIMETER/Q1")
        self.path_label.setFont(QFont("Sans Serif", 14))
        self.path_label.setStyleSheet("color: #888888;")
        top_bar.addWidget(self.path_label)
        
        top_bar.addStretch()
        
        self.camera_btn = QPushButton("📷")
        self.camera_btn.setFixedSize(60, 60)
        self.camera_btn.setFont(QFont("Noto Color Emoji", 24))
        self.camera_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d4ff;
                color: white;
                border: none;
                border-radius: 30px;
            }
            QPushButton:hover {
                background-color: #00a8cc;
            }
        """)
        self.camera_btn.clicked.connect(self.show_camera_popup)
        top_bar.addWidget(self.camera_btn)
        
        layout.addLayout(top_bar)
        
        back_btn = BackButton()
        back_btn.clicked.connect(self.back_clicked.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        
        layout.addSpacing(20)
        
        question_frame = QWidget()
        question_layout = QHBoxLayout(question_frame)
        question_layout.setContentsMargins(0, 0, 0, 0)
        question_layout.setSpacing(20)
        
        self.q_label = QLabel("Q 1")
        self.q_label.setFont(QFont("Sans Serif", 24))
        self.q_label.setStyleSheet("color: #7CDAFF;")
        self.q_label.setFixedWidth(70)
        question_layout.addWidget(self.q_label, alignment=Qt.AlignmentFlag.AlignTop)
        
        self.question_label = QLabel()
        self.question_label.setFont(QFont("Sans Serif", 18))
        self.question_label.setStyleSheet("color: #FFFFFF;")
        self.question_label.setWordWrap(True)
        self.question_label.setTextFormat(Qt.TextFormat.RichText)
        question_layout.addWidget(self.question_label, stretch=1)
        
        layout.addWidget(question_frame)
        
        layout.addSpacing(30)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #1a1a2e;
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #7CDAFF;
                border-radius: 5px;
                min-height: 30px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(25)
        self.chat_layout.setContentsMargins(0, 0, 20, 0)
        self.chat_layout.addStretch()
        
        self.scroll_area.setWidget(self.chat_container)
        layout.addWidget(self.scroll_area, stretch=1)
        
        self.status_label = QLabel("🎤 Listening...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Sans Serif", 20))
        self.status_label.setStyleSheet("color: #4ade80;")
        layout.addWidget(self.status_label)
    
    def init_camera_popup(self):
        """"""
        print("📷 [QA Chat] Initializing camera popup...")
        try:
            self.camera_popup = CameraPopup(self)
            self.camera_popup.image_uploaded.connect(self.on_image_uploaded)
            self.camera_popup.hide()
            print("📷 [QA Chat] Camera popup initialized successfully")
        except Exception as e:
            print(f"❌ [QA Chat] Failed to init camera popup: {e}")
            import traceback
            traceback.print_exc()
    
    def show_camera_popup(self):
        """"""
        print("📷 [QA Chat] show_camera_popup() called")
        print(f"📷 [QA Chat] camera_popup exists: {self.camera_popup is not None}")
        if self.camera_popup:
            print("📷 [QA Chat] Calling camera_popup.show_popup()...")
            self.camera_popup.show_popup()
        else:
            print("❌ [QA Chat] camera_popup is None!")
    
    def on_image_uploaded(self, image_array):
        """"""
        print("📷 [QA Chat] Image received, analyzing...")
        
        temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        cv2.imwrite(temp_file.name, image_array)
        self.pending_image = temp_file.name
        print(f"📷 [QA Chat] Image saved to: {temp_file.name}")
        
        self.add_message("", is_user=True, has_image=True, image_path=temp_file.name)
        
        self.analyze_image(temp_file.name)
    
    def analyze_image(self, image_path: str):
        """ RAG + """
        if not self.voice_assistant:
            self.add_message("Sorry, I cannot analyze images right now.", is_user=False)
            return
        
        self._set_status.emit("🔍 Analyzing image...")
        
        def analyze_thread():
            try:
                print(f"\n{'='*50}")
                print(f"🖼️ [Image Analysis] Starting analysis...")
                print(f"🖼️ [Image Analysis] Image path: {image_path}")
                
                response = self.voice_assistant.chat_with_rag(
                    "Please analyze this diagram and tell me if there are any issues with it.",
                    image_paths=[image_path]
                )
                
                print(f"\n🤖 [Image Analysis Result]:")
                print(f"{'='*50}")
                print(response)
                print(f"{'='*50}\n")
                
                self._add_bot_message.emit(response)
            except Exception as e:
                print(f"❌ [Image Analysis] Error: {e}")
                import traceback
                traceback.print_exc()
                self._add_bot_message.emit(f"Sorry, I encountered an error analyzing the image.")
            finally:
                self._set_status.emit("🎤 Listening...")
        
        threading.Thread(target=analyze_thread, daemon=True).start()
    
    def _update_status_label(self, text: str):
        """"""
        self.status_label.setText(text)
    
    def set_voice_assistant(self, voice_assistant):
        """（ - ）"""
        print("⚠️  [QA Chat] set_voice_assistant is deprecated - using main voice assistant")
    
    def start_voice_listening(self):
        """（ - Realtime API ）"""
        print("✅ [QA Chat] Using Realtime Voice Assistant (already listening)")
        self._set_status.emit("🎤 Listening (Realtime API)...")
        return
        
        def listen_loop_deprecated():
            hallucination_phrases = [
                "thanks for watching",
                "thank you for watching", 
                "subscribe",
                "see you next time",
                "bye bye",
                "goodbye",
                "like and subscribe",
                "please subscribe",
                "don't forget to subscribe",
                "thank you",
                "you",
            ]
            
            while self.is_listening:
                try:
                    self._set_status.emit("🎤 Listening...")
                    wav_path = self.voice_assistant._record_user_input()
                    
                    if not wav_path or not os.path.exists(wav_path):
                        continue
                    
                    self._set_status.emit("📝 Transcribing...")
                    user_text = self.voice_assistant.transcribe_audio(wav_path)
                    
                    if os.path.exists(wav_path):
                        os.unlink(wav_path)
                    
                    if not user_text or len(user_text.strip()) < 2:
                        continue
                    
                    text_lower = user_text.lower().strip()
                    is_hallucination = any(phrase in text_lower for phrase in hallucination_phrases)
                    if is_hallucination:
                        print(f"🚫 [QA Chat] Filtered hallucination: '{user_text}'")
                        continue
                    
                    print(f"\n👤 [User]: {user_text}")
                    self._add_user_message.emit(user_text)
                    
                    diagram_keywords = ["diagram", "drawing", "circuit", "schematic", "wrong", "issue", "problem", "mistake"]
                    if any(kw in user_text.lower() for kw in diagram_keywords):
                        response = "Can you show your diagram to me? Click the camera icon (📷) in the top right corner to upload a photo."
                        print(f"🤖 [Robot]: {response}\n")
                        self._add_bot_message.emit(response)
                        continue
                    
                    self._set_status.emit("🤔 Thinking...")
                    response = self.voice_assistant.chat_with_rag(user_text)
                    
                    print(f"🤖 [Robot]: {response}\n")
                    self._add_bot_message.emit(response)
                    
                except Exception as e:
                    print(f"Voice listening error: {e}")
                    import traceback
                    traceback.print_exc()
            
            self._set_status.emit("🔇 Stopped")
        
        self.listen_thread = threading.Thread(target=listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_voice_listening(self):
        """"""
        print("🔇 [QA Chat] Stopping voice listening...")
        self.is_listening = False
    
    def set_question(self, path: str, question_num: int, question_text: str):
        """"""
        self.current_path = path
        self.question_num = question_num
        self.path_label.setText(path)
        self.q_label.setText(f"Q {question_num}")
        
        formatted_text = question_text.replace(
            "READ DC VOLTAGE WITH A MULTIMETER", 
            "<u>READ DC VOLTAGE WITH A MULTIMETER</u>"
        )
        self.question_label.setText(formatted_text)
        self.clear_chat()
    
    def add_message(self, text: str, is_user: bool = False, has_image: bool = False, image_path: str = None):
        """。has_image  image_path 。"""
        msg_widget = QWidget()
        msg_layout = QHBoxLayout(msg_widget)
        msg_layout.setContentsMargins(0, 0, 0, 0)
        msg_layout.setSpacing(15)
        
        if is_user:
            msg_layout.addStretch()
            
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(10)
            content_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
            
            if text:
                text_label = QLabel(text)
                text_label.setFont(QFont("Sans Serif", 18))
                text_label.setStyleSheet("color: #FFFFFF;")
                text_label.setWordWrap(True)
                text_label.setMaximumWidth(700)
                text_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                content_layout.addWidget(text_label)
            
            if has_image and image_path and os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    max_w = 400
                    if pixmap.width() > max_w:
                        pixmap = pixmap.scaledToWidth(max_w, Qt.TransformationMode.SmoothTransformation)
                    img_label = QLabel()
                    img_label.setPixmap(pixmap)
                    img_label.setStyleSheet("border-radius: 8px; background-color: #1a1a2e;")
                    img_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                    content_layout.addWidget(img_label, alignment=Qt.AlignmentFlag.AlignRight)
            
            msg_layout.addWidget(content_widget)
            
            avatar = QLabel("👤")
            avatar.setFont(QFont("Noto Color Emoji", 28))
            avatar.setFixedWidth(60)
            avatar.setAlignment(Qt.AlignmentFlag.AlignTop)
            msg_layout.addWidget(avatar)
        else:
            avatar = QLabel("🎧")
            avatar.setFont(QFont("Noto Color Emoji", 28))
            avatar.setStyleSheet("color: #7CDAFF;")
            avatar.setFixedWidth(60)
            msg_layout.addWidget(avatar, alignment=Qt.AlignmentFlag.AlignTop)
            
            content_widget = QWidget()
            content_layout = QVBoxLayout(content_widget)
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(15)
            
            text_label = QLabel(text)
            text_label.setFont(QFont("Sans Serif", 18))
            text_label.setStyleSheet("color: #FFFFFF;")
            text_label.setWordWrap(True)
            text_label.setMaximumWidth(800)
            content_layout.addWidget(text_label)
            
            if has_image:
                image_placeholder = QFrame()
                image_placeholder.setFixedSize(600, 300)
                image_placeholder.setStyleSheet("""
                    QFrame {
                        background-color: #CCCCCC;
                        border-radius: 10px;
                    }
                """)
                content_layout.addWidget(image_placeholder)
            
            msg_layout.addWidget(content_widget)
            msg_layout.addStretch()
        
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, msg_widget)
        self.messages.append((is_user, text, has_image))
        
        QTimer.singleShot(50, self._scroll_to_bottom)
    
    def _scroll_to_bottom(self):
        """"""
        scrollbar = self.scroll_area.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def clear_chat(self):
        """"""
        self.messages.clear()
        self.conversation_stage = 0
        while self.chat_layout.count() > 1:
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def advance_conversation(self):
        """"""
        if self.conversation_stage == 0:
            self.add_message("YES, I THINK I DRAW A WRONG ONE.", is_user=True)
            self.conversation_stage = 1
        elif self.conversation_stage == 1:
            self.add_message("CAN YOU SHOW YOUR DIAGRAM TO ME?", is_user=False)
            self.conversation_stage = 2
        elif self.conversation_stage == 2:
            self.add_message(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", is_user=False, has_image=True)
            self.conversation_stage = 3
        elif self.conversation_stage == 3:
            self.add_message("DO YOU HAVE ANY MORE QUESTIONS?", is_user=False)
            self.conversation_stage = 4
        elif self.conversation_stage == 4:
            self.add_message("NO, THANKS", is_user=True)
            self.conversation_stage = 5
