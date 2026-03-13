#!/usr/bin/env python3

import argparse
import sys
import os
import signal
import time
from datetime import datetime
from pathlib import Path
from enum import Enum
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, 
    QVBoxLayout, QHBoxLayout, QGraphicsView, QGraphicsScene,
    QGraphicsProxyWidget, QFrame, QPushButton, QScrollArea,
    QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, QRectF, QSize, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QMovie, QPixmap, QImage, QPainter, QColor, QPen, QFontDatabase
import random
import urllib.request
import threading
import cv2

import tts_player
from ui.widgets import StatusItem, LabButton, BackButton
from ui.panels import (
    StatusPanel, 
    CameraPanel, 
    LabSelectPanel, 
    LabDetailPanel, 
    QAChatPanel,
    DefaultPanel,
    MapPanel,
    ConversationPanel
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


class RobotMode(Enum):
    DEFAULT = "default"
    COMING = "coming"             # I AM COMING
    LISTENING = "listening"       # I AM LISTENING
    FOLLOW = "follow"             # FOLLOW ME
    STATUS = "status"
    MAP = "map"
    CAMERA = "camera"
    CONVERSATION = "conversation"
    LAB_SELECT = "lab_select"
    LAB_DETAIL = "lab_detail"
    QA_CHAT = "qa_chat"



# - StatusItem -> ui/widgets/status_item.py  
# - StatusPanel -> ui/panels/status_panel.py



class RobotContent(QWidget):
    qa_message_signal = pyqtSignal(str, bool)  # (message_text, is_user)
    fc_tts_done_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000000;")
        self.current_mode = RobotMode.DEFAULT
        self.qa_voice = None
        self.qa_listening_thread = None
        self.qa_listening_active = False
        self.main_voice_assistant = None
        self.qa_voice_mode = "realtime"  # "realtime" or "legacy", set from main()
        self.fc_session = None  # Realtime API + Function Calling session
        self.fc_tts_unmute_delay_ms = 1000
        self._orig_analyze_image = None  # backup for monkey-patch
        self.init_ui()
        self.qa_message_signal.connect(self._on_qa_message_received)
        self.fc_tts_done_signal.connect(self._on_fc_tts_done)
    
    def set_main_voice_assistant(self, voice_assistant):
        self.main_voice_assistant = voice_assistant
        if hasattr(self, 'qa_chat_panel') and self.qa_chat_panel:
            print("🖼️ [Robot] Setting voice assistant for QA Chat Panel...")
            self.qa_chat_panel.voice_assistant = voice_assistant
    
    def _start_qa_conversation_loop(self):
        if not self.main_voice_assistant:
            return
        
        import threading
        
        def conversation_loop():
            import os
            
            while self.current_mode == RobotMode.QA_CHAT:
                try:
                    wav_path = self.main_voice_assistant.record_audio(duration=10)
                    if not wav_path or not os.path.exists(wav_path):
                        time.sleep(1)
                        continue
                    
                    user_text = self.main_voice_assistant.transcribe_audio(wav_path)
                    os.unlink(wav_path)
                    
                    if not user_text or len(user_text.strip()) == 0:
                        time.sleep(1)
                        continue
                    
                    self.qa_message_signal.emit(user_text, True)
                    print(f"\n💬 [User] {user_text}")
                    
                    image_paths = None
                    if hasattr(self, "qa_chat_panel") and getattr(self.qa_chat_panel, "pending_image", None):
                        image_paths = [self.qa_chat_panel.pending_image]
                        print(f"🖼️ [QA Loop] Using pending image: {self.qa_chat_panel.pending_image}")
                    response = self.main_voice_assistant.chat_with_rag(
                        user_text,
                        image_paths=image_paths,
                    )
                    
                    self.qa_message_signal.emit(response, False)
                    print(f"🤖 [AI] {response}\n")
                    
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"❌ [Error] {e}")
                    time.sleep(2)
        
        qa_thread = threading.Thread(target=conversation_loop, daemon=True)
        qa_thread.start()
    
    def _start_fc_session(self):
        """Start Realtime API session with function calling for QA Chat."""
        if not self.main_voice_assistant:
            return
        try:
            from voice.realtime_fc import RealtimeFCSession
        except ImportError as e:
            print(f"❌ [FC] Import failed: {e}")
            return

        va = self.main_voice_assistant
        va.stop_listening()

        use_tts = self.qa_voice_mode == "realtime_tts"
        self.fc_session = RealtimeFCSession(
            api_key=va.api_key,
            device_name=va.device_name,
            rag_retriever=va.rag_retriever,
            use_tts_playback=use_tts,
        )

        self.fc_session.speech_recognized.connect(
            lambda t: self.qa_chat_panel.add_message(t, is_user=True)
        )
        self.fc_session.listening_changed.connect(
            lambda on: self.qa_chat_panel.status_label.setText(
                "🎤 Listening..." if on else "🤖 Speaking..."
            )
        )
        if use_tts:
            def on_response(text):
                self.qa_chat_panel.add_message(text, is_user=False)
                self.qa_chat_panel.status_label.setText("🤖 Speaking...")
                tts_player.speak_async(text.strip(), on_done=lambda: self.fc_tts_done_signal.emit())
            self.fc_session.response_ready.connect(on_response)
            self.qa_chat_panel.status_label.setText("🤖 Speaking...")
        else:
            self.fc_session.response_ready.connect(
                lambda t: self.qa_chat_panel.add_message(t, is_user=False)
            )
            self.qa_chat_panel.status_label.setText("🤖 Speaking...")

        # Redirect image analysis to function-calling path
        self._orig_analyze_image = self.qa_chat_panel.analyze_image
        self.qa_chat_panel.analyze_image = (
            lambda path: self.fc_session.notify_image_uploaded(path)
        )

        self.fc_session.start()
        print("✅ [FC] Session started for QA Chat")

    def _on_fc_tts_done(self):
        """TTS playback finished (realtime_tts mode): delay then request mic reopen."""
        self.qa_chat_panel.status_label.setText("🕒 Reopening mic...")
        QTimer.singleShot(self.fc_tts_unmute_delay_ms, self._unmute_fc_mic_after_tts)

    def _unmute_fc_mic_after_tts(self):
        if self.fc_session:
            self.fc_session.notify_tts_playback_finished()

    def _stop_fc_session(self):
        """Stop the Realtime FC session if running."""
        if self.fc_session:
            self.fc_session.stop()
            self.fc_session = None
        if self._orig_analyze_image is not None:
            self.qa_chat_panel.analyze_image = self._orig_analyze_image
            self._orig_analyze_image = None

    def init_ui(self):
        self.default_panel = DefaultPanel(self)
        self.default_panel.hide()
        
        self.status_panel = StatusPanel(self)
        self.status_panel.hide()
        
        self.map_panel = MapPanel(self)
        self.map_panel.hide()
        
        self.camera_panel = CameraPanel(self, stream_url=None, local_camera_index=0, use_local_camera=False)
        self.camera_panel.hide()
        
        self.conversation_panel = ConversationPanel(self)
        self.conversation_panel.hide()
        
        self.lab_select_panel = LabSelectPanel(self)
        self.lab_select_panel.lab_selected.connect(self._on_lab_selected)
        self.lab_select_panel.back_clicked.connect(lambda: self.set_mode(RobotMode.DEFAULT))
        self.lab_select_panel.hide()
        
        self.lab_detail_panel = LabDetailPanel(self)
        self.lab_detail_panel.question_selected.connect(self._on_question_selected)
        self.lab_detail_panel.back_clicked.connect(lambda: self.set_mode(RobotMode.LAB_SELECT))
        self.lab_detail_panel.hide()
        
        self.qa_chat_panel = QAChatPanel(self)
        self.qa_chat_panel.back_clicked.connect(lambda: self.set_mode(RobotMode.LAB_DETAIL))
        self.qa_chat_panel.hide()
        
        self.default_panel.show()
    
    def _on_lab_selected(self, lab_num: int):
        self.lab_detail_panel.set_lab(lab_num)
        self.set_mode(RobotMode.LAB_DETAIL)
    
    def _on_question_selected(self, lab_name: str, section_name: str, question_num: int):
        section_display = section_name.upper().replace("_", " ")
        path = f"{lab_name}/{section_display}/Q{question_num}"
        
        questions = {
            ("power_supply", 1): "DRAW A DIAGRAM OF THE SETUP TO READ DC VOLTAGE WITH A MULTIMETER (DC VOLTAGE: >>). THE DIAGRAM SHOULD SHOW WHICH COMPONENTS ARE USED, WITH LINES SHOWING HOW THEY ARE CONNECTED.",
            ("power_supply", 2): "WHAT IS THE MAXIMUM VOLTAGE OUTPUT OF THE POWER SUPPLY?",
            ("power_supply", 3): "HOW DO YOU SET THE MULTIMETER TO MEASURE DC VOLTAGE?",
            ("power_supply", 4): "WHAT SAFETY PRECAUTIONS SHOULD YOU TAKE?",
            ("oscilloscope", 1): "DRAW A DIAGRAM SHOWING HOW TO CONNECT AN OSCILLOSCOPE TO MEASURE A SIGNAL.",
            ("oscilloscope", 2): "WHAT IS THE FUNCTION OF THE SIGNAL GENERATOR?",
            ("oscilloscope", 3): "HOW DO YOU ADJUST THE TIME BASE ON AN OSCILLOSCOPE?",
        }
        
        question_text = questions.get((section_name, question_num), f"Question {question_num} content here...")
        
        self.qa_chat_panel.set_question(path, question_num, question_text)
        
        self.qa_chat_panel.clear_chat()
        self.set_mode(RobotMode.QA_CHAT)
    
    def set_mode(self, mode: RobotMode):

        lab_modes_no_voice = {RobotMode.LAB_SELECT, RobotMode.LAB_DETAIL}
        
        if self.current_mode in lab_modes_no_voice and mode not in lab_modes_no_voice:
            if self.main_voice_assistant:
                if mode != RobotMode.QA_CHAT:
                    self.main_voice_assistant.stop_listening()
                    print("🎙️ [Robot] Resuming voice assistant (wake word on mode 1)...")
                    self.main_voice_assistant.start_listening(audio_mode=True)
                else:
                    if self.qa_voice_mode in ("realtime", "realtime_tts"):
                        print("🎙️ [QA Chat] Starting Realtime FC session...")
                        QTimer.singleShot(500, lambda: self._start_fc_session())
                    else:
                        print("🎙️ [QA Chat] Starting legacy conversation loop...")
                        QTimer.singleShot(500, lambda: self._start_qa_conversation_loop())
        
        if self.current_mode == RobotMode.QA_CHAT and mode != RobotMode.QA_CHAT:
            print("🎙️ [Robot] Leaving QA Chat mode...")
            if self.qa_voice_mode in ("realtime", "realtime_tts"):
                self._stop_fc_session()
            if self.main_voice_assistant and hasattr(self.main_voice_assistant, "clear_image_context"):
                self.main_voice_assistant.clear_image_context()
            if hasattr(self, "qa_chat_panel") and hasattr(self.qa_chat_panel, "pending_image"):
                self.qa_chat_panel.pending_image = None
            if self.main_voice_assistant and mode not in lab_modes_no_voice:
                print("🎙️ [Robot] Resuming voice assistant (wake word on mode 1)...")
                self.main_voice_assistant.start_listening(audio_mode=True)

        if mode in lab_modes_no_voice and self.current_mode not in lab_modes_no_voice:
            if self.main_voice_assistant:
                print("🎙️ [Robot] Pausing voice assistant for Lab Select/Detail...")
                self.main_voice_assistant.stop_listening()
        
        if self.current_mode == RobotMode.CAMERA and mode != RobotMode.CAMERA:
            print("📷 [Robot] Leaving CAMERA mode, releasing camera...")
            self.camera_panel.stop_simulation()
        
        self.current_mode = mode
        
        self.default_panel.hide()
        self.status_panel.hide()
        self.map_panel.hide()
        self.camera_panel.hide()
        self.conversation_panel.hide()
        self.lab_select_panel.hide()
        self.lab_detail_panel.hide()
        self.qa_chat_panel.hide()
        
        if mode == RobotMode.STATUS:
            self.status_panel.show()
        elif mode == RobotMode.MAP:
            self.map_panel.show()
        elif mode == RobotMode.CAMERA:
            self.camera_panel.show()
            print("📷 [Robot] Entering CAMERA mode, starting local camera...")
            self.camera_panel.start_local_camera()
        elif mode == RobotMode.CONVERSATION:
            self.conversation_panel.show()
        elif mode == RobotMode.LAB_SELECT:
            self.lab_select_panel.show()
        elif mode == RobotMode.LAB_DETAIL:
            self.lab_detail_panel.show()
        elif mode == RobotMode.QA_CHAT:
            self.qa_chat_panel.show()
        else:
            self.default_panel.show()
            self.default_panel.start_animation()
            
            if mode == RobotMode.DEFAULT:
                self.default_panel.set_speech_text("")
            elif mode == RobotMode.COMING:
                self.default_panel.set_speech_text("I AM COMING")
            elif mode == RobotMode.LISTENING:
                self.default_panel.set_speech_text("I AM LISTENING")
            elif mode == RobotMode.FOLLOW:
                self.default_panel.set_speech_text("FOLLOW ME")
    
    def set_user_text(self, text: str):
        self.conversation_panel.set_user_text(text)
    
    def set_robot_text(self, text: str):
        self.conversation_panel.set_robot_text(text)
    
    def set_conversation_status(self, status: str):
        self.conversation_panel.set_status(status)
    
    def get_mode(self) -> RobotMode:
        return self.current_mode
    
    def get_status_panel(self) -> StatusPanel:
        return self.status_panel
    
    def get_camera_panel(self) -> CameraPanel:
        return self.camera_panel
    
    def get_lab_select_panel(self) -> LabSelectPanel:
        return self.lab_select_panel
    
    def get_lab_detail_panel(self) -> LabDetailPanel:
        return self.lab_detail_panel
    
    def get_qa_chat_panel(self) -> QAChatPanel:
        return self.qa_chat_panel
    
    def get_default_panel(self) -> DefaultPanel:
        return self.default_panel
    
    def get_map_panel(self) -> MapPanel:
        return self.map_panel
    
    def get_conversation_panel(self) -> ConversationPanel:
        return self.conversation_panel
    
    def set_camera_stream(self, stream_url: str):
        self.camera_panel.set_stream_url(stream_url)
    
    def add_qa_message(self, text: str, is_user: bool = False):
        self.qa_chat_panel.add_message(text, is_user)
        if not is_user and text and text.strip():
            tts_player.speak_async(text.strip())

    def _on_qa_message_received(self, text: str, is_user: bool):
        self.add_qa_message(text, is_user)
    
    def set_qa_voice_assistant(self, voice_assistant):
        self.qa_voice = voice_assistant
    
    def start_qa_voice_listening(self):
        if not self.qa_voice or self.qa_listening_active:
            return
        
        self.qa_listening_active = True
        import threading
        
        def listen_loop():
            while self.qa_listening_active and self.current_mode == RobotMode.QA_CHAT:
                try:
                    wav_path = self.qa_voice._record_user_input()
                    if wav_path and os.path.exists(wav_path):
                        user_text = self.qa_voice.transcribe_audio(wav_path)
                        if user_text and len(user_text.strip()) > 0:
                            QTimer.singleShot(0, lambda: self.add_qa_message(user_text, is_user=True))
                            
                            response = self.qa_voice.chat_with_rag(user_text)
                            QTimer.singleShot(0, lambda: self.add_qa_message(response, is_user=False))
                        
                        os.unlink(wav_path)
                except Exception as e:
                    print(f"QA listening error: {e}")
                    import traceback
                    traceback.print_exc()
                    break
        
        self.qa_listening_thread = threading.Thread(target=listen_loop, daemon=True)
        self.qa_listening_thread.start()
    
    def stop_qa_voice_listening(self):
        self.qa_listening_active = False


class ScalableGraphicsView(QGraphicsView):
    
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setStyleSheet("background-color: #000000; border: none;")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setRenderHints(self.renderHints())
        
        self.base_width = 1080
        self.base_height = 1920
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fit_content()
    
    def fit_content(self):
        view_width = self.viewport().width()
        view_height = self.viewport().height()
        
        if view_width <= 0 or view_height <= 0:
            return
        
        scale_w = view_width / self.base_width
        scale_h = view_height / self.base_height
        scale = min(scale_w, scale_h)
        
        self.resetTransform()
        self.scale(scale, scale)
        
        self.centerOn(self.base_width / 2, self.base_height / 2)


class RobotUI(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("DOGU & GIX")
        self.resize(540, 960)
        self.setMinimumSize(270, 480)
        self.setStyleSheet("QMainWindow { background-color: #000000; }")
        
        self.scene = QGraphicsScene()
        self.content = RobotContent()
        self.proxy = self.scene.addWidget(self.content)
        
        self.scene.setSceneRect(0, 0, 1080, 1920)
        
        self.view = ScalableGraphicsView(self.scene)
        self.setCentralWidget(self.view)
    
    def set_mode_default(self):
        self.content.set_mode(RobotMode.DEFAULT)
    
    def set_mode_coming(self):
        self.content.set_mode(RobotMode.COMING)
    
    def set_mode_listening(self):
        self.content.set_mode(RobotMode.LISTENING)
    
    def set_mode_follow(self):
        self.content.set_mode(RobotMode.FOLLOW)
    
    def set_mode_status(self):
        self.content.set_mode(RobotMode.STATUS)
    
    def set_mode_map(self):
        self.content.set_mode(RobotMode.MAP)
    
    def set_mode_camera(self):
        self.content.set_mode(RobotMode.CAMERA)
    
    def set_mode_conversation(self):
        self.content.set_mode(RobotMode.CONVERSATION)
    
    def set_mode_lab_select(self):
        self.content.set_mode(RobotMode.LAB_SELECT)
    
    def set_mode_lab_detail(self):
        self.content.set_mode(RobotMode.LAB_DETAIL)
    
    def set_mode_qa_chat(self):
        self.content.set_mode(RobotMode.QA_CHAT)
    
    def add_qa_message(self, text: str, is_user: bool = False):
        self.content.add_qa_message(text, is_user)
    
    def set_user_text(self, text: str):
        self.content.set_user_text(text)
    
    def set_robot_text(self, text: str):
        self.content.set_robot_text(text)
    
    def set_conversation_status(self, status: str):
        self.content.set_conversation_status(status)
    
    def get_current_mode(self) -> RobotMode:
        return self.content.get_mode()
    
    def set_battery(self, level: int):
        self.content.get_status_panel().set_battery(level)
    
    def set_mic_status(self, status: bool):
        self.content.get_status_panel().set_mic_status(status)
    
    def set_video_status(self, status: bool):
        self.content.get_status_panel().set_video_status(status)
    
    def set_wave_detected(self, detected: bool):
        self.content.get_status_panel().set_wave_detected(detected)
    
    def set_camera_stream(self, stream_url: str):
        self.content.set_camera_stream(stream_url if stream_url else None)
    
    def keyPressEvent(self, event):
        key = event.key()
        
        if key == Qt.Key.Key_Escape:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.close()
        elif key == Qt.Key.Key_F or key == Qt.Key.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()
        elif key == Qt.Key.Key_1:
            self.set_mode_default()
        elif key == Qt.Key.Key_2:
            self.set_mode_coming()
        elif key == Qt.Key.Key_3:
            self.set_mode_listening()
        elif key == Qt.Key.Key_4:
            self.set_mode_follow()
        elif key == Qt.Key.Key_5:
            self.set_mode_status()
        elif key == Qt.Key.Key_6:
            self.set_mode_map()
        elif key == Qt.Key.Key_7:
            self.set_mode_camera()
        elif key == Qt.Key.Key_8:
            self.set_mode_conversation()
        elif key == Qt.Key.Key_9:
            self.set_mode_lab_select()
        elif key == Qt.Key.Key_0:
            self.set_mode_lab_detail()


def main():
    # ── CLI args ─────────────────────────────────────────────────────────
    parser = argparse.ArgumentParser(description="DOGU Robot UI")
    parser.add_argument(
        "--voice-mode",
        choices=["realtime", "realtime_tts", "legacy"],
        default="realtime",
        help="QA Chat: realtime (WebRTC audio), realtime_tts (TTS playback), legacy",
    )
    args, qt_args = parser.parse_known_args()
    voice_mode = args.voice_mode
    print(f"\n🔊 Voice mode: {voice_mode}")

    try:
        from config import OPENAI_API_KEY
        if OPENAI_API_KEY and OPENAI_API_KEY != "API Key":
            os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
            print(f"API Key loaded: {OPENAI_API_KEY[:8]}...")
    except ImportError:
        pass
    
    app = QApplication([sys.argv[0]] + qt_args)
    app.setStyle("Fusion")

    # Let Ctrl+C work: Python signal handlers only run when the interpreter
    # regains control. A periodic no-op timer forces Qt to yield briefly so
    # Python can process the pending SIGINT.
    signal.signal(signal.SIGINT, lambda s, f: app.quit())
    _keepalive = QTimer()
    _keepalive.timeout.connect(lambda: None)
    _keepalive.start(200)

    fonts_dir = Path(__file__).parent / "fonts"
    if fonts_dir.exists():
        for font_file in fonts_dir.glob("*.ttf"):
            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id >= 0:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"✅ Font loaded: {font_file.name} -> {families}")
            else:
                print(f"❌ Failed to load font: {font_file.name}")
        for font_file in fonts_dir.glob("*.otf"):
            font_id = QFontDatabase.addApplicationFont(str(font_file))
            if font_id >= 0:
                families = QFontDatabase.applicationFontFamilies(font_id)
                print(f"✅ Font loaded: {font_file.name} -> {families}")
            else:
                print(f"❌ Failed to load font: {font_file.name}")
    
    window = RobotUI()
    window.content.qa_voice_mode = voice_mode
    window.show()
    
    voice_enabled = False
    try:
        import subprocess
        
        from voice.realtime_voice_assistant_rag import RealtimeVoiceAssistantRAG
        wake_word_hint = "Say 'iroi' to wake up"
        print(f"\nUsing Realtime Voice Assistant with OpenWakeWord + RAG + Realtime API")
        
        try:
            result = subprocess.run(['which', 'arecord'], capture_output=True, text=True)
            arecord_available = result.returncode == 0
        except:
            arecord_available = False
        
        api_key_available = os.getenv("OPENAI_API_KEY") or (
            hasattr(__import__('config', fromlist=['OPENAI_API_KEY']), 'OPENAI_API_KEY') and
            __import__('config', fromlist=['OPENAI_API_KEY']).OPENAI_API_KEY and
            __import__('config', fromlist=['OPENAI_API_KEY']).OPENAI_API_KEY != "API Key"
        )
        
        if arecord_available and api_key_available:
            voice = RealtimeVoiceAssistantRAG()
            
            if not voice.oww_model:
                print("\nWarning: OpenWakeWord model not loaded, voice feature will be unavailable")
                print("   Please check:")
                print("   1) openwakeword library is correctly installed: pip install openwakeword")
                print("   2) Model file exists: DOOOGU/model/eyeroeee.onnx (OpenWakeWord needs .onnx, not .tflite)")
                print("   3) Base models are downloaded")
                voice_enabled = False
            else:
                print("✅ QA Chat will use main Realtime Voice Assistant")
                
                def on_wake_word(recognized_text):
                    print(f"🔔 Wake word detected! (recognized: {recognized_text})")
                    window.set_mode_lab_select()
                
                def on_speech_recognized(text):
                    print(f"👤 [User] {text}")
                    if window.get_current_mode() == RobotMode.QA_CHAT:
                        window.add_qa_message(text, is_user=True)
                    elif window.get_current_mode() == RobotMode.CONVERSATION:
                        window.set_user_text(text)
                        window.set_robot_text("...")
                        window.set_conversation_status("🤔 Thinking...")
                
                def on_response_ready(response):
                    print(f"🤖 [AI] {response}")
                    if window.get_current_mode() == RobotMode.QA_CHAT:
                        window.add_qa_message(response, is_user=False)
                    elif window.get_current_mode() == RobotMode.CONVERSATION:
                        window.set_robot_text(response)
                        window.set_conversation_status("🔊 Speaking...")
                        if response and response.strip():
                            tts_player.speak_async(response.strip(), on_done=lambda: QTimer.singleShot(0, lambda: window.set_conversation_status("🎤 Listening...")))
                
                def on_speaking_finished():
                    if window.get_current_mode() == RobotMode.CONVERSATION:
                        window.set_conversation_status("🎤 Listening...")
                
                voice.wake_word_detected.connect(on_wake_word)
                voice.speech_recognized.connect(on_speech_recognized)
                voice.response_ready.connect(on_response_ready)
                voice.speaking_finished.connect(on_speaking_finished)
                
                window.content.set_main_voice_assistant(voice)
                print("✅ Main voice assistant connected for wake word control")
                
                QTimer.singleShot(4000, lambda: voice.start_listening(audio_mode=True))
                
                voice_enabled = True
                print(f"\nVoice feature enabled! {wake_word_hint}")
        else:
            if not arecord_available:
                print("\nWarning: Voice feature unavailable: arecord not installed")
                print("   Run: sudo apt install alsa-utils")
            if not api_key_available:
                print("\nWarning: Voice feature unavailable: Please set OPENAI_API_KEY in config.py")
    except ImportError as e:
        print(f"\nWarning: Voice module loading failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nControl keys:")
    print("   1-8 - Switch modes (Default/Coming/Listening/Follow/Status/Map/Camera/Conversation)")
    print("   9   - Lab selection")
    print("   0   - Lab details")
    print("   F/F11 - Fullscreen")
    print("   ESC - Exit")
    print(f"\n   QA voice mode: {voice_mode}")
    print("     Switch with: --voice-mode realtime | realtime_tts | legacy")
    if voice_enabled:
        print(f"\n{wake_word_hint}!\n")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
