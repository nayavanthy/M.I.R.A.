import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextBrowser, QLineEdit, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont, QMouseEvent

import mira_backend
import subprocesses

class CustomTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()
        self.offset = None

    def init_ui(self):
        self.setFixedHeight(30)
        self.setStyleSheet("background-color: black; color: white;")
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 0, 0)
        
        self.title = QLabel("M.I.R.A.")
        self.title.setFont(QFont("Montserrat", 14))
        self.title.setStyleSheet("color: #00aaff;")
        layout.addWidget(self.title)
        layout.addStretch()
        
        self.close_btn = QPushButton("✖")
        self.close_btn.setStyleSheet("background: red; border: none; color: white;")
        self.close_btn.clicked.connect(self.parent.close)
        layout.addWidget(self.close_btn)
        
        self.setLayout(layout)

    def close_application(self):
        self.parent.close()  # Close UI
        subprocesses.kill_operations()  # Stop backend
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.globalPos() - self.parent.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        if self.offset and event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.offset)

class MiraChatUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowFlag(Qt.FramelessWindowHint)  # Remove default title bar
        self.setGeometry(100, 100, 700, 800)  # Adjusted height
        self.setStyleSheet("background-color: #121212; border: 2px solid #1E90FF; border-radius: 10px;")

        layout = QVBoxLayout()

        self.title_bar = CustomTitleBar(self)
        layout.addWidget(self.title_bar)

        self.chat_display = QTextBrowser()
        self.chat_display.setStyleSheet("background-color: #1C1C1C; color: white; border: none;")
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setStyleSheet("background-color: #222; color: white; border: 1px solid #1E90FF; padding: 5px;")
        self.input_field.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_field)

        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("background-color: #1E90FF; color: white; border-radius: 5px; padding: 5px;")
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.chat_display.append(f"<b>You:</b> {user_message}")
            self.input_field.clear()
            response = self.get_mira_response(user_message)
            self.chat_display.append(f"<b>MIRA:</b> {response}")

    def get_mira_response(self, message):
        return mira_backend.preliminary_interpret(message)
    
if __name__ == "__main__":
    subprocesses.start_operations()  # Start backend

    app = QApplication(sys.argv)
    window = MiraChatUI()
    window.show()
    
    exit_code = app.exec_()

    subprocesses.kill_operations()  # Ensure backend stops when UI exits
    sys.exit(exit_code)
