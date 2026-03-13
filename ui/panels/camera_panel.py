"""
CameraPanel - 
、 MJPEG 
"""
import random
import urllib.request
from datetime import datetime

import cv2
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QImage, QPainter, QColor, QPen


class MJPEGStreamThread(QThread):
    """MJPEG"""
    frame_received = pyqtSignal(bytes)
    connection_status = pyqtSignal(str)
    
    def __init__(self, stream_url):
        super().__init__()
        self.stream_url = stream_url
        self.running = True
    
    def run(self):
        """MJPEG"""
        while self.running:
            try:
                self.connection_status.emit("connecting")
                stream = urllib.request.urlopen(self.stream_url, timeout=5)
                self.connection_status.emit("connected")
                
                buffer = b''
                while self.running:
                    chunk = stream.read(4096)
                    if not chunk:
                        break
                    buffer += chunk
                    
                    start = buffer.find(b'\xff\xd8')
                    end = buffer.find(b'\xff\xd9')
                    
                    if start != -1 and end != -1 and end > start:
                        jpg_data = buffer[start:end + 2]
                        buffer = buffer[end + 2:]
                        self.frame_received.emit(jpg_data)
                        
            except Exception as e:
                self.connection_status.emit(f"error: {str(e)[:30]}")
                if self.running:
                    import time
                    time.sleep(2)
    
    def stop(self):
        self.running = False


class LocalCameraThread(QThread):
    """"""
    frame_received = pyqtSignal(object)  # numpy array
    connection_status = pyqtSignal(str)
    
    def __init__(self, device_index=0):
        super().__init__()
        self.device_index = device_index
        self.running = True
        self.cap = None
    
    def run(self):
        """"""
        self.connection_status.emit("connecting")
        
        self.cap = cv2.VideoCapture(self.device_index)
        
        if not self.cap.isOpened():
            self.connection_status.emit(f"error:  {self.device_index}")
            return
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        
        self.connection_status.emit("connected")
        
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame_received.emit(frame_rgb)
            else:
                self.connection_status.emit("error: ")
                break
            
            import time
            time.sleep(0.033)  # ~30 FPS
        
        if self.cap:
            self.cap.release()
    
    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()


class CameraPanel(QWidget):
    """ - 、"""
    
    def __init__(self, parent=None, stream_url=None, local_camera_index=0, use_local_camera=True):
        super().__init__(parent)
        self.setFixedSize(1080, 1920)
        self.setStyleSheet("background-color: #000000;")
        
        self.camera_width = 640
        self.camera_height = 480
        self.fps = 30
        self.frame_count = 0
        self.is_recording = False
        
        self.local_camera_index = local_camera_index
        self.use_local_camera = use_local_camera
        self.local_camera_thread = None
        self.current_frame = None  # numpy array for local camera
        
        self.stream_url = stream_url
        self.stream_thread = None
        self.is_connected = False
        self.current_frame_data = None
        
        self.init_ui()
        
        if self.stream_url:
            self.start_stream()
        elif self.use_local_camera:
            self.start_local_camera()
        else:
            self.start_camera_simulation()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 60, 50, 60)
        layout.setSpacing(20)
        
        title = QLabel("📷 CAMERA VIEW")
        title_font = QFont("Silkscreen", 42)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #7CDAFF;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        camera_frame = QFrame()
        camera_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 3px solid #7CDAFF;
                border-radius: 15px;
            }
        """)
        camera_frame.setFixedSize(980, 740)
        camera_layout = QVBoxLayout(camera_frame)
        camera_layout.setContentsMargins(10, 10, 10, 10)
        
        self.camera_display = QLabel()
        self.camera_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_display.setFixedSize(960, 720)
        self.camera_display.setStyleSheet("""
            QLabel {
                background-color: #0d0d1a;
                border: none;
                border-radius: 10px;
            }
        """)
        camera_layout.addWidget(self.camera_display)
        layout.addWidget(camera_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(20)
        
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
                border: 2px solid #4ade80;
                border-radius: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_frame)
        info_layout.setContentsMargins(30, 20, 30, 20)
        info_layout.setSpacing(15)
        
        info_title = QLabel("CAMERA INFO")
        info_title_font = QFont("Silkscreen", 24)
        info_title_font.setBold(True)
        info_title.setFont(info_title_font)
        info_title.setStyleSheet("color: #4ade80; border: none;")
        info_layout.addWidget(info_title)
        
        res_layout = QHBoxLayout()
        res_icon = QLabel("📐")
        res_icon.setFont(QFont("Noto Color Emoji", 24))
        res_icon.setStyleSheet("border: none;")
        res_layout.addWidget(res_icon)
        res_label = QLabel("Resolution:")
        res_label.setFont(QFont("Silkscreen", 18))
        res_label.setStyleSheet("color: #888888; border: none;")
        res_layout.addWidget(res_label)
        self.res_value = QLabel(f"{self.camera_width} x {self.camera_height}")
        self.res_value.setFont(QFont("Silkscreen", 18))
        self.res_value.setStyleSheet("color: #7CDAFF; border: none;")
        res_layout.addWidget(self.res_value)
        res_layout.addStretch()
        info_layout.addLayout(res_layout)
        
        # FPS
        fps_layout = QHBoxLayout()
        fps_icon = QLabel("⏱️")
        fps_icon.setFont(QFont("Noto Color Emoji", 24))
        fps_icon.setStyleSheet("border: none;")
        fps_layout.addWidget(fps_icon)
        fps_label = QLabel("FPS:")
        fps_label.setFont(QFont("Silkscreen", 18))
        fps_label.setStyleSheet("color: #888888; border: none;")
        fps_layout.addWidget(fps_label)
        self.fps_value = QLabel(f"{self.fps}")
        self.fps_value.setFont(QFont("Silkscreen", 18))
        self.fps_value.setStyleSheet("color: #4ade80; border: none;")
        fps_layout.addWidget(self.fps_value)
        fps_layout.addStretch()
        info_layout.addLayout(fps_layout)
        
        frame_layout = QHBoxLayout()
        frame_icon = QLabel("🎞️")
        frame_icon.setFont(QFont("Noto Color Emoji", 24))
        frame_icon.setStyleSheet("border: none;")
        frame_layout.addWidget(frame_icon)
        frame_label = QLabel("Frame:")
        frame_label.setFont(QFont("Silkscreen", 18))
        frame_label.setStyleSheet("color: #888888; border: none;")
        frame_layout.addWidget(frame_label)
        self.frame_value = QLabel("0")
        self.frame_value.setFont(QFont("Silkscreen", 18))
        self.frame_value.setStyleSheet("color: #fbbf24; border: none;")
        frame_layout.addWidget(self.frame_value)
        frame_layout.addStretch()
        info_layout.addLayout(frame_layout)
        
        status_layout = QHBoxLayout()
        status_icon = QLabel("🔴")
        status_icon.setFont(QFont("Noto Color Emoji", 24))
        status_icon.setStyleSheet("border: none;")
        self.status_icon = status_icon
        status_layout.addWidget(status_icon)
        status_label = QLabel("Status:")
        status_label.setFont(QFont("Silkscreen", 18))
        status_label.setStyleSheet("color: #888888; border: none;")
        status_layout.addWidget(status_label)
        self.status_value = QLabel("SIMULATED")
        self.status_value.setFont(QFont("Silkscreen", 18))
        self.status_value.setStyleSheet("color: #fbbf24; border: none;")
        status_layout.addWidget(self.status_value)
        status_layout.addStretch()
        info_layout.addLayout(status_layout)
        
        layout.addWidget(info_frame)
        
        layout.addStretch()
        
        self.hint_label = QLabel("Press 1-6 to switch mode | Simulated Camera")
        hint_font = QFont("Silkscreen", 18)
        self.hint_label.setFont(hint_font)
        self.hint_label.setStyleSheet("color: #555555;")
        self.hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.hint_label)
    
    def start_stream(self):
        """"""
        self.status_value.setText("CONNECTING...")
        self.status_value.setStyleSheet("color: #fbbf24; border: none;")
        self.hint_label.setText(f"Connecting to: {self.stream_url}")
        
        self.stream_thread = MJPEGStreamThread(self.stream_url)
        self.stream_thread.frame_received.connect(self.on_frame_received)
        self.stream_thread.connection_status.connect(self.on_connection_status)
        self.stream_thread.start()
        
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_stream_frame)
        self.camera_timer.start(33)  # ~30 FPS
    
    def on_frame_received(self, jpg_data):
        """"""
        self.current_frame_data = jpg_data
        self.frame_count += 1
    
    def on_connection_status(self, status):
        """"""
        if status == "connected":
            self.is_connected = True
            self.status_value.setText("CONNECTED")
            self.status_value.setStyleSheet("color: #4ade80; border: none;")
            self.status_icon.setText("🟢")
            self.hint_label.setText(f"Stream: {self.stream_url}")
        elif status == "connecting":
            self.status_value.setText("CONNECTING...")
            self.status_value.setStyleSheet("color: #fbbf24; border: none;")
            self.status_icon.setText("🟡")
        elif status.startswith("error"):
            self.is_connected = False
            self.status_value.setText("DISCONNECTED")
            self.status_value.setStyleSheet("color: #ef4444; border: none;")
            self.status_icon.setText("🔴")
            self.hint_label.setText(f"Error: {status[7:]}")
    
    def update_stream_frame(self):
        """"""
        self.frame_value.setText(str(self.frame_count))
        
        if self.current_frame_data:
            image = QImage()
            if image.loadFromData(self.current_frame_data):
                self.camera_width = image.width()
                self.camera_height = image.height()
                self.res_value.setText(f"{self.camera_width} x {self.camera_height}")
                
                pixmap = QPixmap.fromImage(image)
                scaled_pixmap = pixmap.scaled(960, 720, Qt.AspectRatioMode.KeepAspectRatio, 
                                              Qt.TransformationMode.SmoothTransformation)
                self.camera_display.setPixmap(scaled_pixmap)
        else:
            self.show_waiting_frame()
    
    def show_waiting_frame(self):
        """"""
        width, height = 960, 720
        image = QImage(width, height, QImage.Format.Format_RGB32)
        painter = QPainter(image)
        
        image.fill(QColor(13, 13, 26))
        
        painter.setPen(QColor(124, 218, 255))
        painter.setFont(QFont("Silkscreen", 32))
        text = "[ CONNECTING TO CAMERA... ]"
        text_width = painter.fontMetrics().horizontalAdvance(text)
        painter.drawText((width - text_width) // 2, height // 2, text)
        
        dots = "." * ((self.frame_count // 10) % 4)
        painter.drawText((width - text_width) // 2 + text_width, height // 2, dots)
        
        painter.end()
        
        pixmap = QPixmap.fromImage(image)
        self.camera_display.setPixmap(pixmap)
        self.frame_count += 1
    
    def set_stream_url(self, url):
        """URL"""
        self.stop_simulation()
        
        self.stream_url = url
        self.frame_count = 0
        self.current_frame_data = None
        
        if url:
            self.start_stream()
        else:
            self.start_camera_simulation()
    
    def start_local_camera(self):
        """"""
        self.status_value.setText("CONNECTING...")
        self.status_value.setStyleSheet("color: #fbbf24; border: none;")
        self.hint_label.setText(f" /dev/video{self.local_camera_index}...")
        
        self.local_camera_thread = LocalCameraThread(self.local_camera_index)
        self.local_camera_thread.frame_received.connect(self.on_local_frame_received)
        self.local_camera_thread.connection_status.connect(self.on_local_camera_status)
        self.local_camera_thread.start()
        
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_local_camera_frame)
        self.camera_timer.start(33)  # ~30 FPS
    
    def on_local_frame_received(self, frame):
        """"""
        self.current_frame = frame
        self.frame_count += 1
    
    def on_local_camera_status(self, status):
        """"""
        if status == "connected":
            self.is_connected = True
            self.status_value.setText("LIVE")
            self.status_value.setStyleSheet("color: #4ade80; border: none;")
            self.status_icon.setText("🟢")
            self.hint_label.setText(f" /dev/video{self.local_camera_index} |  1-6 ")
        elif status == "connecting":
            self.status_value.setText("CONNECTING...")
            self.status_value.setStyleSheet("color: #fbbf24; border: none;")
            self.status_icon.setText("🟡")
        elif status.startswith("error"):
            self.is_connected = False
            self.status_value.setText("ERROR")
            self.status_value.setStyleSheet("color: #ef4444; border: none;")
            self.status_icon.setText("🔴")
            self.hint_label.setText(f": {status[7:]}")
            print(f"[Camera] : {status}")
            self.start_camera_simulation()
    
    def update_local_camera_frame(self):
        """"""
        self.frame_value.setText(str(self.frame_count))
        
        if self.current_frame is not None:
            h, w, ch = self.current_frame.shape
            self.camera_width = w
            self.camera_height = h
            self.res_value.setText(f"{w} x {h}")
            
            bytes_per_line = ch * w
            q_image = QImage(self.current_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            
            pixmap = QPixmap.fromImage(q_image)
            scaled_pixmap = pixmap.scaled(960, 720, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            self.camera_display.setPixmap(scaled_pixmap)
        else:
            self.show_waiting_frame()
    
    def start_camera_simulation(self):
        """"""
        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self.update_camera_frame)
        self.camera_timer.start(33)  # ~30 FPS
    
    def update_camera_frame(self):
        """"""
        self.frame_count += 1
        self.frame_value.setText(str(self.frame_count))
        
        width, height = 960, 720
        
        image = QImage(width, height, QImage.Format.Format_RGB32)
        painter = QPainter(image)
        
        base_color = 20 + random.randint(-5, 5)
        image.fill(QColor(base_color, base_color + 5, base_color + 10))
        
        painter.setPen(QPen(QColor(40, 60, 80), 1))
        grid_size = 60
        for x in range(0, width, grid_size):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, grid_size):
            painter.drawLine(0, y, width, y)
        
        painter.setPen(QPen(QColor(124, 218, 255), 2))
        center_x, center_y = width // 2, height // 2
        cross_size = 40
        painter.drawLine(center_x - cross_size, center_y, center_x + cross_size, center_y)
        painter.drawLine(center_x, center_y - cross_size, center_x, center_y + cross_size)
        
        painter.setPen(QPen(QColor(74, 222, 128), 2))
        painter.drawEllipse(center_x - 80, center_y - 80, 160, 160)
        
        scan_y = (self.frame_count * 3) % height
        painter.setPen(QPen(QColor(124, 218, 255, 100), 3))
        painter.drawLine(0, scan_y, width, scan_y)
        
        corner_size = 50
        painter.setPen(QPen(QColor(251, 191, 36), 2))
        painter.drawLine(10, 10, 10 + corner_size, 10)
        painter.drawLine(10, 10, 10, 10 + corner_size)
        painter.drawLine(width - 10, 10, width - 10 - corner_size, 10)
        painter.drawLine(width - 10, 10, width - 10, 10 + corner_size)
        painter.drawLine(10, height - 10, 10 + corner_size, height - 10)
        painter.drawLine(10, height - 10, 10, height - 10 - corner_size)
        painter.drawLine(width - 10, height - 10, width - 10 - corner_size, height - 10)
        painter.drawLine(width - 10, height - 10, width - 10, height - 10 - corner_size)
        
        painter.setPen(QColor(124, 218, 255))
        painter.setFont(QFont("Silkscreen", 16))
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        painter.drawText(20, height - 20, f"SIMULATED | {timestamp}")
        
        painter.drawText(width - 150, height - 20, f"FRAME: {self.frame_count}")
        
        painter.setPen(QColor(251, 191, 36))
        painter.setFont(QFont("Silkscreen", 32))
        text = "[ SIMULATED CAMERA ]"
        text_width = painter.fontMetrics().horizontalAdvance(text)
        painter.drawText((width - text_width) // 2, 50, text)
        
        painter.setPen(QColor(255, 255, 255, 30))
        for _ in range(50):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            painter.drawPoint(x, y)
        
        painter.end()
        
        pixmap = QPixmap.fromImage(image)
        self.camera_display.setPixmap(pixmap)
    
    def stop_simulation(self):
        """//"""
        if hasattr(self, 'camera_timer') and self.camera_timer:
            self.camera_timer.stop()
        if hasattr(self, 'stream_thread') and self.stream_thread:
            self.stream_thread.stop()
            self.stream_thread.wait(1000)
            self.stream_thread = None
        if hasattr(self, 'local_camera_thread') and self.local_camera_thread:
            self.local_camera_thread.stop()
            self.local_camera_thread.wait(1000)
            self.local_camera_thread = None
