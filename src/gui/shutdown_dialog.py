"""
Shutdown warning dialog
Displays countdown before shutdown with cancel option
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QProgressBar
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
from src.i18n.translations import translator
from src.utils.system import play_alert_sound


class ShutdownDialog(QDialog):
    """Dialog that warns user about impending shutdown"""
    
    COUNTDOWN_SECONDS = 30
    
    def __init__(self, parent=None, play_sound=False):
        super().__init__(parent)
        self.cancelled = False
        self.remaining_time = self.COUNTDOWN_SECONDS
        self.play_sound = play_sound
        
        self.init_ui()
        self.setup_timer()
        
        if self.play_sound:
            play_alert_sound()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(translator.get('shutdown_warning_title'))
        self.setFixedSize(450, 250)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Warning icon and text
        warning_label = QLabel(translator.get('warning_attention'))
        warning_label.setAlignment(Qt.AlignCenter)
        warning_font = QFont()
        warning_font.setPointSize(16)
        warning_font.setBold(True)
        warning_label.setFont(warning_font)
        layout.addWidget(warning_label)
        
        # Message label
        self.message_label = QLabel()
        self.update_message()
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        message_font = QFont()
        message_font.setPointSize(11)
        self.message_label.setFont(message_font)
        layout.addWidget(self.message_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(self.COUNTDOWN_SECONDS)
        self.progress_bar.setValue(self.COUNTDOWN_SECONDS)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimumHeight(30)
        layout.addWidget(self.progress_bar)
        
        # Cancel button
        cancel_button = QPushButton(translator.get('cancel_shutdown_button'))
        cancel_button.clicked.connect(self.cancel_shutdown)
        cancel_button.setMinimumHeight(50)
        cancel_button.setStyleSheet('''
            QPushButton {
                background-color: #ff4444;
                color: white;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #ff6666;
            }
        ''')
        layout.addWidget(cancel_button)
    
    def setup_timer(self):
        """Setup countdown timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)
    
    def update_message(self):
        """Update message label text"""
        self.message_label.setText(
            translator.get('computer_shutdown_in', seconds=self.remaining_time)
        )
    
    def update_countdown(self):
        """Update countdown timer"""
        self.remaining_time -= 1
        self.progress_bar.setValue(self.remaining_time)
        self.update_message()
        
        if self.remaining_time <= 0:
            self.timer.stop()
            self.accept()
    
    def cancel_shutdown(self):
        """Cancel shutdown when user clicks button"""
        self.cancelled = True
        self.timer.stop()
        self.reject()