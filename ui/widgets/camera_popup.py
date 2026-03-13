"""
CameraPopup - 
 QA Chat 
（7）
"""
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread
from PyQt6.QtGui import QFont, QPixmap, QImage


class CameraThread(QThread):
    """ - 7LocalCameraThread"""
    frame_received = pyqtSignal(object)  # numpy array
    connection_status = pyqtSignal(str)  # "connected", "error: xxx"
    
    def __init__(self, device_index=0):
        super().__init__()
        self.device_index = device_index
        self.running = True
        self.cap = None
    
    def run(self):
        """"""
        print(f"📷 [CameraThread] Starting camera thread, device={self.device_index}")
        self.connection_status.emit("connecting")
        
        self.cap = cv2.VideoCapture(self.device_index)
        print(f"📷 [CameraThread] VideoCapture({self.device_index}) isOpened: {self.cap.isOpened()}")
        
        if not self.cap.isOpened():
            print("📷 [CameraThread] Trying device 1...")
            self.cap = cv2.VideoCapture(1)
            print(f"📷 [CameraThread] VideoCapture(1) isOpened: {self.cap.isOpened()}")
        
        if not self.cap.isOpened():
            self.connection_status.emit("error: Cannot open camera")
            print("❌ [CameraThread] Cannot open any camera")
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.connection_status.emit("connected")
        print("✅ [CameraThread] Camera connected!")
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_received.emit(frame_rgb)
            else:
                self.connection_status.emit("error: Failed to read frame")
                break
            
            import time
            time.sleep(0.033)
        
        if self.cap:
            self.cap.release()
            print("📷 [CameraThread] Camera released")
    
    def stop(self):
        """"""
        print("📷 [CameraThread] Stopping...")
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None


class CameraPopup(QWidget):
    """ - """
    
    image_uploaded = pyqtSignal(np.ndarray)
    closed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.mode = "preview"
        self.captured_frame = None
        self.current_frame = None
        self.camera_thread = None
        
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.overlay = QWidget()
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 17, 0.85);")
        self.overlay.setFixedSize(1080, 1920)
        
        overlay_layout = QVBoxLayout(self.overlay)
        overlay_layout.setContentsMargins(50, 300, 50, 200)
        overlay_layout.setSpacing(20)
        
        top_bar = QHBoxLayout()
        
        self.back_btn = QPushButton("<")
        self.back_btn.setFixedSize(50, 50)
        self.back_btn.setFont(QFont("Silkscreen", 24))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d4ff;
                color: #000011;
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00a8cc;
            }
        """)
        self.back_btn.clicked.connect(self.back_to_preview)
        self.back_btn.hide()
        top_bar.addWidget(self.back_btn)
        
        top_bar.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(50, 50)
        close_btn.setFont(QFont("Silkscreen", 28))
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #444466;
                color: white;
                border: none;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: #666688;
            }
        """)
        close_btn.clicked.connect(self.close_popup)
        top_bar.addWidget(close_btn)
        
        overlay_layout.addLayout(top_bar)
        
        self.action_btn = QPushButton("CONFIRM")
        self.action_btn.setFixedSize(200, 50)
        self.action_btn.setFont(QFont("Silkscreen", 18))
        self.action_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d4ff;
                color: #000011;
                border: none;
                border-radius: 25px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00a8cc;
            }
        """)
        self.action_btn.clicked.connect(self.on_action_click)
        overlay_layout.addWidget(self.action_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        
        overlay_layout.addSpacing(20)
        
        self.camera_frame = QFrame()
        self.camera_frame.setFixedSize(900, 700)
        self.camera_frame.setStyleSheet("""
            QFrame {
                background-color: #333344;
                border-radius: 20px;
            }
        """)
        
        camera_layout = QVBoxLayout(self.camera_frame)
        camera_layout.setContentsMargins(20, 20, 20, 20)
        
        self.camera_label = QLabel("Loading camera...")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_label.setStyleSheet("color: #888888; font-size: 24px;")
        self.camera_label.setFixedSize(860, 660)
        camera_layout.addWidget(self.camera_label)
        
        overlay_layout.addWidget(self.camera_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        overlay_layout.addStretch()
        
        main_layout.addWidget(self.overlay)
    
    def show_popup(self):
        """"""
        print("📷 [CameraPopup] show_popup() called")
        self.mode = "preview"
        self.action_btn.setText("CONFIRM")
        self.back_btn.hide()
        self.camera_label.setText("Loading camera...")
        self.show()
        print("📷 [CameraPopup] Widget shown, starting camera thread...")
        self.start_camera()
    
    def start_camera(self):
        """"""
        self.stop_camera()
        
        self.camera_thread = CameraThread(device_index=0)
        self.camera_thread.frame_received.connect(self.on_frame_received)
        self.camera_thread.connection_status.connect(self.on_camera_status)
        self.camera_thread.start()
        print("📷 [CameraPopup] Camera thread started")
    
    def on_frame_received(self, frame_rgb):
        """（ UI）"""
        self.current_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        scaled_pixmap = pixmap.scaled(860, 660, Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation)
        self.camera_label.setPixmap(scaled_pixmap)
    
    def on_camera_status(self, status):
        """"""
        print(f"📷 [CameraPopup] Camera status: {status}")
        if status == "connected":
            pass
        elif status == "connecting":
            self.camera_label.setText("Connecting to camera...")
        elif status.startswith("error"):
            self.camera_label.setText(f"Cannot open camera\nMay be in use by another panel")
    
    def on_action_click(self):
        """"""
        if self.mode == "preview":
            self.capture_frame()
        else:
            self.upload_image()
    
    def capture_frame(self):
        """"""
        if self.current_frame is not None:
            self.captured_frame = self.current_frame.copy()
            
            self.stop_camera()
            
            self.mode = "confirm"
            self.action_btn.setText("UPLOAD")
            self.back_btn.show()
            
            frame_rgb = cv2.cvtColor(self.captured_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(860, 660, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.camera_label.setPixmap(scaled_pixmap)
            print("📷 [CameraPopup] Frame captured, switched to confirm mode")
    
    def back_to_preview(self):
        """"""
        self.mode = "preview"
        self.action_btn.setText("CONFIRM")
        self.back_btn.hide()
        self.captured_frame = None
        
        self.start_camera()
    
    def upload_image(self):
        """"""
        if self.captured_frame is not None:
            print("📷 [CameraPopup] Image uploaded!")
            self.image_uploaded.emit(self.captured_frame)
            self.close_popup()
    
    def close_popup(self):
        """"""
        self.stop_camera()
        self.hide()
        self.closed.emit()
    
    def stop_camera(self):
        """"""
        if self.camera_thread is not None:
            self.camera_thread.stop()
            self.camera_thread.wait(2000)
            self.camera_thread = None
            print("📷 [CameraPopup] Camera thread stopped")
