"""
Help dialog
Displays user documentation and FAQ
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QTextBrowser
from src.i18n.translations import translator
from src.i18n.help_content import HELP_CONTENT


class HelpDialog(QDialog):
    """Help and FAQ dialog"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(translator.get('help_title'))
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Text browser for displaying help content
        help_text = QTextBrowser()
        help_text.setOpenExternalLinks(True)
        help_text.setHtml(self.get_help_content())
        layout.addWidget(help_text)
        
        # Close button
        close_button = QPushButton(translator.get('cancel_button'))
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def get_help_content(self):
        """Get help content in current language"""
        lang = translator.current_language
        return HELP_CONTENT.get(lang, HELP_CONTENT['en'])