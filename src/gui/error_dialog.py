"""
Error dialog
Displays only an error message with a close button
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
from src.i18n.translations import translator

def show_error(messages, parent=None):
    """
    messages: str or list[str]
    """
    if isinstance(messages, list):
        text = "\n".join(messages)
    else:
        text = messages

    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(translator.get('error_dialog_title'))
    msg_box.setText(text)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()


class ErrorDialog(QDialog):
    """Minimal error dialog displaying one or multiple error messages"""
    
    def __init__(self, parent=None, error_messages=None):
        """
        :param error_messages: str or list[str]
        """
        super().__init__(parent)
        
        # Приводим всё к списку строк
        if error_messages is None:
            self.error_messages = [translator.get("unknown_error_occurred")]
        elif isinstance(error_messages, str):
            self.error_messages = [error_messages]
        else:
            self.error_messages = error_messages
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(translator.get('error_dialog_title'))
        self.setFixedSize(500, 200)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        
        # Объединяем строки с переносами для QLabel
        error_text = "\n".join(self.error_messages)
        error_label = QLabel(error_text)
        error_label.setWordWrap(True)
        error_label.setAlignment(Qt.AlignCenter)
        error_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
        layout.addWidget(error_label)
        
        # Close button (red)
        close_button = QPushButton(translator.get('close_button'))
        close_button.setStyleSheet("background-color: red; color: white; font-weight: bold;")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
