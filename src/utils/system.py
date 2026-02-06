"""
System utilities module
Contains system-specific functions for shutdown, autostart, etc.
"""

import sys
import os
import winreg


def execute_shutdown():
    """Execute system shutdown command"""
    if sys.platform == 'win32':
        os.system('shutdown /s /t 0')
    elif sys.platform == 'darwin':
        os.system('sudo shutdown -h now')
    else:
        os.system('shutdown -h now')


def play_alert_sound():
    """Play system alert sound"""
    try:
        if sys.platform == 'win32':
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
    except Exception as e:
        print(f"Error playing sound: {e}")


def is_autostart_enabled():
    """Check if autostart is enabled (Windows only)"""
    if sys.platform != 'win32':
        return False
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\Microsoft\Windows\CurrentVersion\Run',
            0,
            winreg.KEY_READ
        )
        try:
            winreg.QueryValueEx(key, 'BatteryShutdown')
            winreg.CloseKey(key)
            return True
        except WindowsError:
            winreg.CloseKey(key)
            return False
    except Exception as e:
        print(f"Error checking autostart: {e}")
        return False


def set_autostart(enable):
    """Enable or disable autostart (Windows only)"""
    if sys.platform != 'win32':
        return False
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Software\Microsoft\Windows\CurrentVersion\Run',
            0,
            winreg.KEY_SET_VALUE
        )
        
        if enable:
            exe_path = sys.executable
            if getattr(sys, 'frozen', False):
                # Running from .exe
                exe_path = sys.executable
            else:
                # Running from .py
                exe_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
            
            winreg.SetValueEx(key, 'BatteryShutdown', 0, winreg.REG_SZ, exe_path)
        else:
            try:
                winreg.DeleteValue(key, 'BatteryShutdown')
            except:
                pass
        
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Error setting autostart: {e}")
        return False