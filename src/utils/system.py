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
        elif sys.platform == 'darwin':
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        else:  # Linux
            if os.system('which beep') == 0:
                os.system('beep')
            else:
                os.system('echo -e "\a"')
    except Exception as e:
        print(f"Error playing sound: {e}")



def is_autostart_enabled():
    """Check if autostart is enabled"""
    try:
        if sys.platform == 'win32':
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
        
        elif sys.platform == 'darwin':
            # macOS через launch agents (plist)
            try:
                plist_path = os.path.expanduser('~/Library/LaunchAgents/com.batteryshutdown.plist')
                return os.path.exists(plist_path)
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
            
        else:  # Linux
            autostart_file = os.path.expanduser('~/.config/autostart/batteryshutdown.desktop')
            return os.path.exists(autostart_file)
    except Exception as e:
        print(f"Error checking autostart: {e}")
        return False


def set_autostart(enable):
    """Enable or disable autostart"""

    
    try:
        if sys.platform == 'win32':
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
        elif sys.platform == 'darwin':
            plist_path = os.path.expanduser('~/Library/LaunchAgents/com.batteryshutdown.plist')
            if enable:
                plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
                <plist version="1.0">
                <dict>
                    <key>Label</key><string>com.batteryshutdown</string>
                    <key>ProgramArguments</key><array>
                        <string>{sys.executable}</string>
                        <string>{os.path.abspath(__file__)}</string>
                    </array>
                    <key>RunAtLoad</key><true/>
                </dict>
                </plist>"""
                with open(plist_path, 'w') as f:
                    f.write(plist_content)
            else:
                if os.path.exists(plist_path):
                    os.remove(plist_path)
            return True
        else:  # Linux
            autostart_dir = os.path.expanduser('~/.config/autostart')
            os.makedirs(autostart_dir, exist_ok=True)
            autostart_file = os.path.join(autostart_dir, 'batteryshutdown.desktop')
            if enable:
                desktop_content = f"""[Desktop Entry]
Type=Application
Exec={sys.executable} {os.path.abspath(__file__)}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=BatteryShutdown
Comment=Battery shutdown script
"""
                with open(autostart_file, 'w') as f:
                    f.write(desktop_content)
            else:
                if os.path.exists(autostart_file):
                    os.remove(autostart_file)
            return True
    except Exception as e:
        print(f"Error setting autostart: {e}")
        return False