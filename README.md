# Battery Auto-Shutdown

<center>
<a href="https://github.com/XXanderWP/WinPowerControl"><img src="./icon.ico"/></a>
</center>

<center>

[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FXXanderWP%2FWinPowerControl%2Frefs%2Fheads%2Fmain%2Fpyproject.toml&query=%24.project.version&logo=gitforwindows&label=App%20version)](https://github.com/XXanderWP/WinPowerControl/releases/latest)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FXXanderWP%2FWinPowerControl%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</center>

A lightweight desktop application that automatically shuts down your computer when running on battery power. Perfect for preventing accidental battery drain if your charger gets disconnected.

## 🌍 Multi-Language Support

The application automatically detects your system language and supports:
- 🇬🇧 English
- 🇷🇺 Russian (Русский)
- 🇺🇦 Ukrainian (Українська)

If your system language isn't supported, the app defaults to English.

## ✨ Features

- **🔋 Automatic Battery Monitoring** - Continuously monitors your laptop's power status
- **⏱️ Configurable Delay** - Set a delay (1-60 minutes) before shutdown occurs
- **📊 Battery Threshold** - Set minimum battery percentage for shutdown trigger
- **🔔 Warning Dialog** - 30-second countdown with cancel option before shutdown
- **🔊 Sound Alerts** - Optional audio notifications (can be disabled)
- **🚀 Auto-Start** - Option to run at Windows startup
- **💾 Persistent Settings** - All configurations are automatically saved
- **🎨 System Tray Integration** - Minimizes to tray, runs in background

## 📋 Requirements

- Windows 7/8/10/11
- Python 3.7 or higher (for running from source)
- PyQt5
- psutil

## 🚀 Quick Start

### Option 1: Using Pre-built Executable (Recommended)

1. Download the latest EXE file from [Releases](../../releases)
2. Run the executable
3. Configure your settings
4. Enable auto-shutdown

### Option 2: Running from Source

1. **Clone the repository:**
   ```bash
   git clone https://github.com/XXanderWP/WinPowerControl.git
   cd battery-shutdown
   ```

2. **Create and activate virtual environment:**
   
   Windows:
   ```bash
   setup_venv.bat
   venv\Scripts\activate
   ```


3. **Run the application:**
   ```bash
   python main.py
   ```

## 🛠️ Building from Source

To create a standalone executable:

1. **Activate virtual environment** (if not already activated)
   ```bash
   venv\Scripts\activate  # Windows
   ```

2. **Run build script:**
   
   Windows:
   ```bash
   build.bat
   ```
   

The executable will be created in the `dist` folder.

## 📖 How It Works

1. **Power Monitoring**: The app continuously monitors your computer's power status
2. **Battery Transition**: When disconnected from AC power, a countdown timer starts
3. **Threshold Check**: If battery drops below your set percentage and time expires, shutdown is triggered
4. **Warning Dialog**: A 30-second warning appears before shutdown
5. **Cancel Option**: You can cancel the shutdown at any time

### Example Scenario

- **Settings**: 5-minute delay, 50% battery threshold
- **Event**: Charger disconnects, battery at 75%
- **Process**: 
  - Timer starts (5 minutes)
  - After 5 minutes, if battery ≤ 50%, warning dialog appears
  - 30-second countdown begins
  - Computer shuts down (unless cancelled)

## ⚙️ Configuration

### Main Settings

- **Enable Auto-Shutdown**: Master on/off switch
- **Delay Before Shutdown**: 1-60 minutes (time after AC disconnect)
- **Minimum Battery Charge**: 1-100% (shutdown threshold)

### Additional Settings

- **Sound Notifications**: Enable/disable audio alerts
- **Auto-Start**: Launch at Windows startup

### Configuration File

Settings are stored in: `%USERPROFILE%\.win_power_control\config.json`

Example configuration:
```json
{
  "enabled": true,
  "delay_minutes": 5,
  "battery_percent": 50,
  "sound_enabled": true,
  "language": null
}
```

## 🎯 Use Cases

- **Accidental Disconnect Protection**: Prevent battery drain if charger unplugs
- **Power Outage Safety**: Auto-shutdown during extended power outages
- **Battery Longevity**: Avoid deep discharge cycles
- **Remote Systems**: Automatically manage power on unattended machines

## 🔒 Safety Features

- **Cancellable Shutdown**: Always get 30 seconds to cancel
- **Auto-Disable on Cancel**: If you cancel once, feature turns off
- **Persistent Status**: System tray icon shows current state
- **Multiple Conditions**: Both time AND battery level must be met

## 📂 Project Structure

```
battery-shutdown/
├── main.py                 # Application entry point
├── src/
│   ├── core/
│   │   ├── config.py      # Configuration management
│   │   └── monitor.py     # Battery monitoring thread
│   ├── gui/
│   │   ├── main_window.py        # Main application window
│   │   ├── settings_dialog.py   # Settings dialog
│   │   ├── help_dialog.py        # Help/FAQ dialog
│   │   └── shutdown_dialog.py   # Shutdown warning dialog
│   ├── i18n/
│   │   ├── translations.py       # Translation system
│   │   └── help_content.py       # Multi-language help text
│   └── utils/
│       └── system.py      # System utilities (shutdown, autostart)
├── requirements.txt       # Python dependencies
├── setup_venv.bat        # Virtual environment setup (Windows)
├── build.bat             # Build script (Windows)
└── README.md             # This file
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding a New Language

To add support for a new language:

1. Edit `src/i18n/translations.py`
2. Add your language code and translations to `TRANSLATIONS` dictionary
3. Edit `src/i18n/help_content.py`
4. Add help content in your language to `HELP_CONTENT` dictionary

## 🐛 Troubleshooting

### App doesn't start
- Ensure Python 3.7+ is installed
- Check that all dependencies are installed: `pip install -r requirements.txt`
- Try running with admin privileges

### Battery not detected
- This app requires a laptop with a battery
- Desktop computers are not supported
- Check if Windows detects your battery in Device Manager

### Auto-start not working
- Ensure you have necessary permissions
- Check Windows Registry: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
- Try running the app as administrator

### Shutdown doesn't work
- Check Windows Event Viewer for shutdown errors
- Ensure you have permission to shutdown the system
- Test manual shutdown command: `shutdown /s /t 0`

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Created with ❤️ for better battery management

## 🙏 Acknowledgments

- **PyQt5** - Cross-platform GUI framework
- **psutil** - System and process utilities
- **Python community** - For amazing tools and libraries

## 📞 Support

- **Issues**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Email**: xanderwp@protonmail.com

---

⭐ If you find this project useful, please consider giving it a star!

## 🗺️ Roadmap

- [ ] macOS support
- [ ] Linux support
- [ ] Hibernate option (instead of shutdown)
- [ ] Sleep mode trigger
- [ ] Battery statistics
- [ ] Custom shutdown scripts
