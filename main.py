"""
Battery Shutdown - Main Application Entry Point
Automatically shuts down the computer when running on battery power
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()