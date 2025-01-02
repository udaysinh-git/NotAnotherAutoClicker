import os
import random
import sys
import threading
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QSpinBox,
)

from pynput import keyboard, mouse

class AutoClicker(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.left_running = False
        self.right_running = False
        self.current_hotkeys = {'left': 'x2', 'right': 'x1'}
        
        self.mouse_listener = mouse.Listener(on_click=self.on_mouse_click)
        self.mouse_listener.start()
        
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()
        
    def init_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QGridLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        bg_label = QLabel(self)
        if getattr(sys, 'frozen', False):
            backgrounds_path = os.path.join(sys._MEIPASS, '_internals/backgrounds')
        else:
            backgrounds_path = os.path.join(os.path.dirname(__file__), 'backgrounds')
        gif_files = [f for f in os.listdir(backgrounds_path) if f.endswith('.gif')]
        if gif_files:
            selected_gif = random.choice(gif_files)
            movie = QMovie(os.path.join(backgrounds_path, selected_gif))
            bg_label.setMovie(movie)
            movie.start()
            bg_label.setScaledContents(True)
        else:
            bg_label.setStyleSheet("background-color: #f0f0f0;")
        main_layout.addWidget(bg_label, 0, 0)
        
        content_widget = QWidget(self)
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color: #2E3440;")
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(10)
        
        title = QLabel("AutoClicker")
        title.setStyleSheet("color: white; font: bold 16px;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        minimize_button = QPushButton("–")
        minimize_button.setFixedSize(20, 20)
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #E5E9F0;
                border: none;
                border-radius: 10px;
                font: bold 14px;
            }
            QPushButton:hover {
                background-color: #A3BE8C;
            }
        """)
        minimize_button.clicked.connect(self.showMinimized)
        title_layout.addWidget(minimize_button)
        
        close_button = QPushButton("✕")
        close_button.setFixedSize(20, 20)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #BF616A;
                border: none;
                border-radius: 10px;
                font: bold 14px;
                color: white;
            }
            QPushButton:hover {
                background-color: #D08770;
            }
        """)
        close_button.clicked.connect(self.close)
        title_layout.addWidget(close_button)
        
        title_bar.setLayout(title_layout)
        content_layout.addWidget(title_bar)
        
        main_content = QWidget()
        main_content_layout = QVBoxLayout()
        main_content_layout.setContentsMargins(20, 20, 20, 20)
        main_content_layout.setSpacing(15)
        
        font = QFont("San Francisco", 10)
        main_content.setFont(font)
        
        main_content.setStyleSheet("""
            QWidget {
                background-color: rgba(0, 0, 0, 0); /* Fully transparent */
            }
            QLabel {
                color: #ffffff; /* White text for visibility */
                font-weight: bold;
                background-color: rgba(0, 0, 0, 0); /* Transparent background */
            }
            QPushButton {
                background-color: rgba(0, 0, 0, 0); /* Transparent background */
                color: #ffffff; /* White text */
                border: 2px solid #ffffff; /* White border for visibility */
                padding: 10px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100); /* Semi-transparent on hover */
                color: #000000; /* Black text on hover */
            }
            QSpinBox {
                padding: 5px;
                border: 1px solid #ffffff; /* White border */
                border-radius: 6px;
                background-color: rgba(255, 255, 255, 100); /* Semi-transparent background */
                color: #000000; /* Black text for visibility */
            }
        """)
        
        cps_layout = QGridLayout()
        cps_layout.addWidget(QLabel("Left CPS:"), 0, 0, Qt.AlignRight)
        self.left_cps = QSpinBox()
        self.left_cps.setRange(1, 1000)
        self.left_cps.setValue(10)
        cps_layout.addWidget(self.left_cps, 0, 1)
        
        cps_layout.addWidget(QLabel("Right CPS:"), 1, 0, Qt.AlignRight)
        self.right_cps = QSpinBox()
        self.right_cps.setRange(1, 1000)
        self.right_cps.setValue(10)
        cps_layout.addWidget(self.right_cps, 1, 1)
        
        main_content_layout.addLayout(cps_layout)
        
        self.start_button = QPushButton("Start Left")
        self.start_button.clicked.connect(self.toggle_left)
        main_content_layout.addWidget(self.start_button, 0, Qt.AlignCenter)
        
        self.start_button_right = QPushButton("Start Right")
        self.start_button_right.clicked.connect(self.toggle_right)
        main_content_layout.addWidget(self.start_button_right, 0, Qt.AlignCenter)
        
        main_content.setLayout(main_content_layout) 
        content_layout.addWidget(main_content)
        
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 0, 0)
        
        self.setLayout(main_layout)
        self.setWindowTitle("AutoClicker")
        self.setFixedSize(800, 600)
        self.show()
        
        title_bar.mousePressEvent = self.title_bar_mouse_press_event
        title_bar.mouseMoveEvent = self.title_bar_mouse_move_event
        
    def title_bar_mouse_press_event(self, event):
        if event.button() == Qt.LeftButton:
            self.old_position = event.globalPos()
    
    def title_bar_mouse_move_event(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = QPoint(event.globalPos() - self.old_position)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_position = event.globalPos()
    
    def toggle_left(self):
        self.left_running = not self.left_running
        if self.left_running:
            threading.Thread(target=self.click, args=('left', self.left_cps.value()), daemon=True).start()
            self.start_button.setText("Stop Left")
        else:
            self.start_button.setText("Start Left")
            
    def toggle_right(self):
        self.right_running = not self.right_running
        if self.right_running:
            threading.Thread(target=self.click, args=('right', self.right_cps.value()), daemon=True).start()
            self.start_button_right.setText("Stop Right")
        else:
            self.start_button_right.setText("Start Right")
            
    def click(self, button, cps):
        with mouse.Controller() as controller:
            while (self.left_running and button == 'left') or (self.right_running and button == 'right'):
                if button == 'left':
                    controller.click(mouse.Button.left)
                else:
                    controller.click(mouse.Button.right)
                time.sleep(1 / cps)
                
    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            if button == mouse.Button.x2 and self.current_hotkeys['left'] == 'x2':
                self.toggle_left()
            elif button == mouse.Button.x1 and self.current_hotkeys['right'] == 'x1':
                self.toggle_right()
                
    def on_press(self, key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                pressed_key = key.char.lower()
            else:
                pressed_key = key.name.lower()
        except AttributeError:
            pressed_key = str(key).lower()
        
        if pressed_key == self.current_hotkeys['left']:
            self.toggle_left()
        elif pressed_key == self.current_hotkeys['right']:
            self.toggle_right()

def main():
    app = QApplication(sys.argv)
    autoclicker = AutoClicker()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()