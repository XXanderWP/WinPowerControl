"""
Main application window
Provides user interface for battery monitoring and shutdown control
"""

import time
import psutil
import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QCheckBox, QPushButton, QGroupBox,
                             QSystemTrayIcon, QMenu, QDialog, QScrollArea)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor

from src.core.config import ConfigManager
from src.core.monitor import BatteryMonitor
from src.gui.settings_dialog import SettingsDialog
from src.gui.help_dialog import HelpDialog
from src.gui.error_dialog import show_error
from src.gui.shutdown_dialog import ShutdownDialog
from src.i18n.translations import translator
from src.utils.system import execute_shutdown


debug_mode = '--debug' in sys.argv

class WorkerSignals(QObject):
    """Signals for communication between threads"""
    shutdown_triggered = pyqtSignal()


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize configuration
        self.config_manager = ConfigManager()
        
        # Apply language setting if specified
        if self.config_manager.get('language'):
            translator.set_language(self.config_manager.get('language'))
            
        battery = psutil.sensors_battery()
        if not battery:
            show_error(translator.get('battery_not_detected_dialog') if not debug_mode else [translator.get('battery_not_detected_dialog'), "!!! Ignored in debug mode"], parent=self)
            if not debug_mode:
                exit(0)
            
        
        # Setup signals
        self.signals = WorkerSignals()
        self.signals.shutdown_triggered.connect(self.show_shutdown_dialog)
        
        # Start battery monitor
        self.monitor = BatteryMonitor(self.config_manager.config, self.signals)
        self.monitor.start()
        
        # Initialize UI
        self.init_ui()
        self.init_tray()
        
        # Setup status update timer
        self.update_status_timer = QTimer()
        self.update_status_timer.timeout.connect(self.update_status)
        self.update_status_timer.start(1000)
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(translator.get('main_window_title'))
        self.setFixedSize(450, 350)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Control group
        control_group = QGroupBox(translator.get('control_group'))
        control_layout = QVBoxLayout()
        
        self.enable_checkbox = QCheckBox(translator.get('enable_auto_shutdown'))
        self.enable_checkbox.setChecked(self.config_manager.get('enabled'))
        self.enable_checkbox.stateChanged.connect(self.on_enable_changed)
        control_layout.addWidget(self.enable_checkbox)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Status group with scroll area
        status_group = QGroupBox(translator.get('current_status'))
        status_group_layout = QVBoxLayout()
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(120)
        scroll_area.setMaximumHeight(120)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        status_widget = QWidget()
        status_widget_layout = QVBoxLayout(status_widget)
        status_widget_layout.setContentsMargins(5, 5, 5, 5)
        
        self.status_label = QLabel(translator.get('loading'))
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        status_widget_layout.addWidget(self.status_label)
        status_widget_layout.addStretch()
        
        scroll_area.setWidget(status_widget)
        status_group_layout.addWidget(scroll_area)
        status_group.setLayout(status_group_layout)
        layout.addWidget(status_group)
        
        layout.addStretch()
        
        # Buttons
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Settings button
        settings_button = QPushButton(translator.get('settings_button'))
        settings_button.clicked.connect(self.show_settings)
        settings_button.setStyleSheet(
            'QPushButton { background-color: #3498db; color: white; padding: 8px; }'
        )
        buttons_layout.addWidget(settings_button)
        
        # Help button
        help_button = QPushButton(translator.get('help_button'))
        help_button.clicked.connect(self.show_help)
        help_button.setStyleSheet(
            'QPushButton { background-color: #95a5a6; color: white; padding: 8px; }'
        )
        buttons_layout.addWidget(help_button)
        
        # Exit button
        exit_button = QPushButton(translator.get('exit_button'))
        exit_button.clicked.connect(self.quit_application)
        exit_button.setStyleSheet(
            'QPushButton { background-color: #ff4444; color: white; padding: 8px; }'
        )
        buttons_layout.addWidget(exit_button)
        
        layout.addLayout(buttons_layout)
        
        self.update_status()
    
    def init_tray(self):
        """Initialize system tray icon"""
        icon = self.create_icon()
        
        self.tray_icon = QSystemTrayIcon(icon, self)
        
        # Tray menu
        tray_menu = QMenu()
        show_action = tray_menu.addAction(translator.get('settings_button').replace('⚙️ ', ''))
        show_action.triggered.connect(self.show)
        
        quit_action = tray_menu.addAction(translator.get('exit_button'))
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def create_icon(self):
        """Create simple battery icon"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw battery
        painter.setBrush(QColor(100, 150, 255))
        painter.setPen(QColor(50, 100, 200))
        painter.drawRoundedRect(8, 20, 40, 24, 4, 4)
        painter.drawRect(48, 28, 8, 8)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
    
    def on_enable_changed(self):
        """Handle enable checkbox change"""
        self.config_manager.set('enabled', self.enable_checkbox.isChecked())
        self.config_manager.save()
        
        if self.config_manager.get('enabled'):
            self.tray_icon.showMessage(
                translator.get('auto_shutdown_on'),
                translator.get('function_enabled'),
                QSystemTrayIcon.Information,
                2000
            )
    
    def show_settings(self):
        """Show settings dialog"""
        dialog = SettingsDialog(self, self.config_manager)
        dialog.exec_()
    
    def show_help(self):
        """Show help dialog"""
        help_dialog = HelpDialog(self)
        help_dialog.exec_()
    
    def update_status(self):
        """Update status display"""
        battery = psutil.sensors_battery()
        
        if battery:
            status = translator.get('power_connected') if battery.power_plugged else translator.get('power_battery')
            percent = battery.percent
            
            status_text = f'{translator.get("battery_charge")}: {status}\n'
            status_text += f'{translator.get("battery_charge")}: {percent}%\n'
            
            if self.config_manager.get('enabled'):
                status_text += f'\n{translator.get("auto_shutdown_enabled")}'
                if not battery.power_plugged and self.monitor.timer_started:
                    remaining = int(self.monitor.shutdown_time - time.time())
                    if remaining > 0:
                        mins = remaining // 60
                        secs = remaining % 60
                        status_text += f'\n{translator.get("time_until_shutdown")}: '
                        status_text += f'{mins} {translator.get("minutes_short")} '
                        status_text += f'{secs} {translator.get("seconds_short")}'
            else:
                status_text += f'\n{translator.get("auto_shutdown_disabled")}'
            
            self.status_label.setText(status_text)
        else:
            self.status_label.setText(translator.get('battery_not_detected'))
    
    def show_shutdown_dialog(self):
        """Show shutdown warning dialog"""
        dialog = ShutdownDialog(self, self.config_manager.get('sound_enabled'))
        result = dialog.exec_()
        
        if dialog.cancelled:
            # User cancelled shutdown
            self.config_manager.set('enabled', False)
            self.enable_checkbox.setChecked(False)
            self.config_manager.save()
            
            self.tray_icon.showMessage(
                translator.get('shutdown_cancelled'),
                translator.get('auto_shutdown_disabled_msg'),
                QSystemTrayIcon.Information,
                3000
            )
        elif result == QDialog.Accepted:
            # Timer expired, execute shutdown
            execute_shutdown()
    
    def closeEvent(self, event):
        """Handle window close event - minimize to tray"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            translator.get('app_minimized'),
            translator.get('app_running_in_tray'),
            QSystemTrayIcon.Information,
            2000
        )
    
    def quit_application(self):
        """Completely quit application"""
        self.monitor.stop()
        self.tray_icon.hide()
        from PyQt5.QtWidgets import QApplication
        QApplication.quit()