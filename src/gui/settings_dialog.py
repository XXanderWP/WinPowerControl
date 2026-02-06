"""
Settings dialog
Allows user to configure application settings
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QCheckBox, QSpinBox, QPushButton, QGroupBox)
from src.i18n.translations import translator
from src.utils.system import is_autostart_enabled, set_autostart


class SettingsDialog(QDialog):
    """Settings configuration dialog"""
    
    def __init__(self, parent, config_manager):
        super().__init__(parent)
        self.config_manager = config_manager
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle(translator.get('settings_title'))
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Main settings group
        main_group = QGroupBox(translator.get('main_settings'))
        main_layout = QVBoxLayout()
        
        # Delay setting
        delay_layout = QHBoxLayout()
        delay_label = QLabel(translator.get('delay_before_shutdown'))
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setMinimum(1)
        self.delay_spinbox.setMaximum(60)
        self.delay_spinbox.setValue(self.config_manager.get('delay_minutes'))
        self.delay_spinbox.setSuffix(' ' + translator.get('minutes_short'))
        delay_layout.addWidget(delay_label)
        delay_layout.addStretch()
        delay_layout.addWidget(self.delay_spinbox)
        main_layout.addLayout(delay_layout)
        
        # Battery percent setting
        battery_layout = QHBoxLayout()
        battery_label = QLabel(translator.get('min_battery_percent'))
        self.battery_spinbox = QSpinBox()
        self.battery_spinbox.setMinimum(1)
        self.battery_spinbox.setMaximum(100)
        self.battery_spinbox.setValue(self.config_manager.get('battery_percent'))
        self.battery_spinbox.setSuffix(' %')
        battery_layout.addWidget(battery_label)
        battery_layout.addStretch()
        battery_layout.addWidget(self.battery_spinbox)
        main_layout.addLayout(battery_layout)
        
        main_group.setLayout(main_layout)
        layout.addWidget(main_group)
        
        # Additional settings group
        extra_group = QGroupBox(translator.get('additional_settings'))
        extra_layout = QVBoxLayout()
        
        # Sound notifications
        self.sound_checkbox = QCheckBox(translator.get('sound_notifications'))
        self.sound_checkbox.setChecked(self.config_manager.get('sound_enabled'))
        extra_layout.addWidget(self.sound_checkbox)
        
        # Autostart
        self.autostart_checkbox = QCheckBox(translator.get('autostart_system'))
        self.autostart_checkbox.setChecked(is_autostart_enabled())
        self.autostart_checkbox.stateChanged.connect(self.on_autostart_changed)
        extra_layout.addWidget(self.autostart_checkbox)
        
        extra_group.setLayout(extra_layout)
        layout.addWidget(extra_group)
        
        layout.addStretch()
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton(translator.get('save_button'))
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet(
            'QPushButton { background-color: #27ae60; color: white; padding: 10px; font-size: 13px; }'
        )
        buttons_layout.addWidget(save_button)
        
        cancel_button = QPushButton(translator.get('cancel_button'))
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet('QPushButton { padding: 10px; font-size: 13px; }')
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
    
    def on_autostart_changed(self):
        """Handle autostart checkbox change"""
        success = set_autostart(self.autostart_checkbox.isChecked())
        if not success:
            # Revert if failed
            self.autostart_checkbox.setChecked(not self.autostart_checkbox.isChecked())
    
    def save_settings(self):
        """Save settings and close dialog"""
        self.config_manager.update({
            'delay_minutes': self.delay_spinbox.value(),
            'battery_percent': self.battery_spinbox.value(),
            'sound_enabled': self.sound_checkbox.isChecked()
        })
        
        self.config_manager.save()
        self.accept()