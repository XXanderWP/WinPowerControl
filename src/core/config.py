"""
Configuration management module
Handles loading and saving application settings
"""

import os
import json
from pathlib import Path


class ConfigManager:
    """Manages application configuration"""
    
    DEFAULT_CONFIG = {
        'enabled': False,
        'delay_minutes': 5,
        'battery_percent': 50,
        'sound_enabled': True,
        'language': None  # None means auto-detect
    }
    
    def __init__(self):
        self.config_file = self._get_config_path()
        self.config = self.load()
    
    def _get_config_path(self):
        """Get path to configuration file in user's home directory"""
        app_data_dir = Path.home() / '.battery_shutdown'
        app_data_dir.mkdir(exist_ok=True)
        return str(app_data_dir / 'config.json')
    
    def load(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Add new settings if they don't exist
                    for key in self.DEFAULT_CONFIG:
                        if key not in loaded:
                            loaded[key] = self.DEFAULT_CONFIG[key]
                    return loaded
            except Exception as e:
                print(f"Error loading config: {e}")
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key, default=None):
        """Get configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set configuration value"""
        self.config[key] = value
    
    def update(self, updates):
        """Update multiple configuration values"""
        self.config.update(updates)