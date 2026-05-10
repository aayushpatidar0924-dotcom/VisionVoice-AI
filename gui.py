from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QLabel
)

from PyQt5.QtCore import Qt
import threading

from gesture import GestureController
from voice import VoiceController


class App(QWidget):

    def __init__(self):
        super().__init__()

        # Controllers
        self.gesture = GestureController()
        self.voice = VoiceController()

        # States
        self.mouse_running = False
        self.voice_running = False
        self.camera_running = False

        # Window
        self.setWindowTitle("VisionVoice AI")
        self.setGeometry(1000, 180, 280, 320)

        self.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint
        )

        # STYLE
        self.setStyleSheet("""
            QWidget {
                background-color: #111827;
                border: 2px solid #2563eb;
                border-radius: 20px;
            }

            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 15px;
                font-weight: bold;
                padding: 12px;
                border-radius: 12px;
            }

            QPushButton:hover {
                background-color: #1d4ed8;
            }

            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)

        # Layout
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Title
        self.title = QLabel("💻 VisionVoice AI")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Mouse Button
        self.mouse_btn = QPushButton("🖐️ Mouse ON")
        self.mouse_btn.clicked.connect(self.toggle_mouse)
        layout.addWidget(self.mouse_btn)

        # Voice Button
        self.voice_btn = QPushButton("🎤 Voice ON")
        self.voice_btn.clicked.connect(self.toggle_voice)
        layout.addWidget(self.voice_btn)

        # Camera Button
        self.camera_btn = QPushButton("📷 Camera Preview OFF")
        self.camera_btn.clicked.connect(self.toggle_camera)
        layout.addWidget(self.camera_btn)

        # Close Button
        self.close_btn = QPushButton("❌ Close")
        self.close_btn.clicked.connect(self.close_all)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    # Mouse


    def toggle_mouse(self):

        if not self.mouse_running:

            self.mouse_running = True
            self.mouse_btn.setText("🖐️ Mouse OFF")

            threading.Thread(
                target=self.gesture.start,
                daemon=True
            ).start()

        else:

            self.mouse_running = False
            self.mouse_btn.setText("🖐️ Mouse ON")

            self.gesture.stop()

    # Voice


    def toggle_voice(self):

        if not self.voice_running:

            self.voice_running = True
            self.voice_btn.setText("🎤 Voice OFF")

            threading.Thread(
                target=self.voice.start,
                daemon=True
            ).start()

        else:

            self.voice_running = False
            self.voice_btn.setText("🎤 Voice ON")

            self.voice.stop()

    # Camera Preview


    def toggle_camera(self):

        self.camera_running = not self.camera_running

        self.gesture.show_camera = self.camera_running

        if self.camera_running:
            self.camera_btn.setText("📷 Camera Preview ON")
        else:
            self.camera_btn.setText("📷 Camera Preview OFF")

    # Close


    def close_all(self):

        self.gesture.stop()
        self.voice.stop()

        self.close()


    # Drag Window


    def mousePressEvent(self, event):

        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):

        delta = event.globalPos() - self.old_pos

        self.move(
            self.x() + delta.x(),
            self.y() + delta.y()
        )

        self.old_pos = event.globalPos()