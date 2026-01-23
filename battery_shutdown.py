import sys
import os
import json
import threading
import time
import winreg
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QCheckBox, QSpinBox, 
                             QPushButton, QSystemTrayIcon, QMenu, QGroupBox,
                             QDialog, QProgressBar, QTextBrowser, QScrollArea)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
import psutil

class WorkerSignals(QObject):
    shutdown_triggered = pyqtSignal()

class ShutdownDialog(QDialog):
    def __init__(self, parent=None, play_sound=False):
        super().__init__(parent)
        self.cancelled = False
        self.remaining_time = 30
        self.play_sound = play_sound
        
        self.init_ui()
        self.setup_timer()
        
        if self.play_sound:
            self.play_alert_sound()
    
    def init_ui(self):
        self.setWindowTitle('Предупреждение о выключении')
        self.setFixedSize(450, 250)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.Dialog)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Иконка предупреждения и текст
        warning_label = QLabel('⚠️ ВНИМАНИЕ!')
        warning_label.setAlignment(Qt.AlignCenter)
        warning_font = QFont()
        warning_font.setPointSize(16)
        warning_font.setBold(True)
        warning_label.setFont(warning_font)
        layout.addWidget(warning_label)
        
        self.message_label = QLabel('Компьютер будет выключен через 30 секунд')
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        message_font = QFont()
        message_font.setPointSize(11)
        self.message_label.setFont(message_font)
        layout.addWidget(self.message_label)
        
        # Прогресс-бар
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(30)
        self.progress_bar.setValue(30)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setMinimumHeight(30)
        layout.addWidget(self.progress_bar)
        
        # Кнопка отмены
        cancel_button = QPushButton('ОТМЕНИТЬ ВЫКЛЮЧЕНИЕ')
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
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)
    
    def update_countdown(self):
        self.remaining_time -= 1
        self.progress_bar.setValue(self.remaining_time)
        self.message_label.setText(f'Компьютер будет выключен через {self.remaining_time} секунд')
        
        if self.remaining_time <= 0:
            self.timer.stop()
            self.accept()
    
    def cancel_shutdown(self):
        self.cancelled = True
        self.timer.stop()
        self.reject()
    
    def play_alert_sound(self):
        """Воспроизводит системный звук предупреждения"""
        try:
            if sys.platform == 'win32':
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            pass

class SettingsDialog(QDialog):
    def __init__(self, parent, config):
        super().__init__(parent)
        self.config = config
        self.parent_window = parent
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Настройки')
        self.setFixedSize(500, 400)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Группа основных настроек
        main_group = QGroupBox('Основные настройки')
        main_layout = QVBoxLayout()
        
        # Задержка
        delay_layout = QHBoxLayout()
        delay_label = QLabel('Задержка перед выключением:')
        self.delay_spinbox = QSpinBox()
        self.delay_spinbox.setMinimum(1)
        self.delay_spinbox.setMaximum(60)
        self.delay_spinbox.setValue(self.config['delay_minutes'])
        self.delay_spinbox.setSuffix(' мин.')
        delay_layout.addWidget(delay_label)
        delay_layout.addStretch()
        delay_layout.addWidget(self.delay_spinbox)
        main_layout.addLayout(delay_layout)
        
        # Процент батареи
        battery_layout = QHBoxLayout()
        battery_label = QLabel('Минимальный заряд батареи:')
        self.battery_spinbox = QSpinBox()
        self.battery_spinbox.setMinimum(1)
        self.battery_spinbox.setMaximum(100)
        self.battery_spinbox.setValue(self.config['battery_percent'])
        self.battery_spinbox.setSuffix(' %')
        battery_layout.addWidget(battery_label)
        battery_layout.addStretch()
        battery_layout.addWidget(self.battery_spinbox)
        main_layout.addLayout(battery_layout)
        
        main_group.setLayout(main_layout)
        layout.addWidget(main_group)
        
        # Группа дополнительных настроек
        extra_group = QGroupBox('Дополнительные настройки')
        extra_layout = QVBoxLayout()
        
        # Звуковые оповещения
        self.sound_checkbox = QCheckBox('Звуковые оповещения')
        self.sound_checkbox.setChecked(self.config['sound_enabled'])
        extra_layout.addWidget(self.sound_checkbox)
        
        # Автозапуск
        self.autostart_checkbox = QCheckBox('Автозапуск при старте Windows')
        self.autostart_checkbox.setChecked(self.is_autostart_enabled())
        self.autostart_checkbox.stateChanged.connect(self.on_autostart_changed)
        extra_layout.addWidget(self.autostart_checkbox)
        
        extra_group.setLayout(extra_layout)
        layout.addWidget(extra_group)
        
        layout.addStretch()
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        save_button = QPushButton('Сохранить')
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet('QPushButton { background-color: #27ae60; color: white; padding: 10px; font-size: 13px; }')
        buttons_layout.addWidget(save_button)
        
        cancel_button = QPushButton('Отмена')
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet('QPushButton { padding: 10px; font-size: 13px; }')
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
    
    def is_autostart_enabled(self):
        """Проверяет, включен ли автозапуск"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'Software\Microsoft\Windows\CurrentVersion\Run', 
                                0, winreg.KEY_READ)
            try:
                winreg.QueryValueEx(key, 'BatteryShutdown')
                winreg.CloseKey(key)
                return True
            except WindowsError:
                winreg.CloseKey(key)
                return False
        except:
            return False
    
    def set_autostart(self, enable):
        """Включает или отключает автозапуск"""
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                               r'Software\Microsoft\Windows\CurrentVersion\Run',
                               0, winreg.KEY_SET_VALUE)
            
            if enable:
                exe_path = sys.executable
                if getattr(sys, 'frozen', False):
                    # Если запущено из .exe
                    exe_path = sys.executable
                else:
                    # Если запущено из .py
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
            print(f"Ошибка настройки автозапуска: {e}")
            return False
    
    def on_autostart_changed(self):
        """Обработчик изменения автозапуска"""
        success = self.set_autostart(self.autostart_checkbox.isChecked())
        if not success:
            # Если не удалось, возвращаем обратно
            self.autostart_checkbox.setChecked(not self.autostart_checkbox.isChecked())
    
    def save_settings(self):
        """Сохраняет настройки"""
        self.config['delay_minutes'] = self.delay_spinbox.value()
        self.config['battery_percent'] = self.battery_spinbox.value()
        self.config['sound_enabled'] = self.sound_checkbox.isChecked()
        
        self.parent_window.save_config()
        self.accept()

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Помощь - Автовыключение при работе от батареи')
        self.setFixedSize(600, 500)
        
        layout = QVBoxLayout(self)
        
        # Текстовый браузер для отображения справки
        help_text = QTextBrowser()
        help_text.setOpenExternalLinks(True)
        help_text.setHtml(self.get_help_content())
        layout.addWidget(help_text)
        
        # Кнопка закрытия
        close_button = QPushButton('Закрыть')
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
    
    def get_help_content(self):
        return """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; }
                h2 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 5px; }
                h3 { color: #34495e; margin-top: 20px; }
                .important { background-color: #fff3cd; padding: 10px; border-left: 4px solid #ffc107; margin: 10px 0; }
                ul { margin-left: 20px; }
            </style>
        </head>
        <body>
            <h2>Назначение программы</h2>
            <p>Данная программа предназначена для автоматического выключения компьютера при переходе 
            на питание от аккумуляторной батареи. Это полезно в ситуациях, когда вы хотите предотвратить 
            полную разрядку батареи ноутбука при случайном отключении зарядного устройства.</p>
            
            <h2>Как работает программа</h2>
            <p>Программа постоянно отслеживает состояние питания вашего компьютера. Когда происходит 
            отключение от электрической сети и компьютер начинает работать от батареи, запускается 
            специальный таймер обратного отсчёта.</p>
            
            <p>Если по истечении установленного времени компьютер всё ещё работает от батареи и уровень 
            её заряда снижается до указанного вами значения, программа инициирует процедуру выключения 
            компьютера.</p>
            
            <h2>Описание настроек</h2>
            
            <h3>Включить автовыключение</h3>
            <p>Основной переключатель программы. Когда он включён, программа активно отслеживает 
            состояние питания. Когда выключен — программа работает в фоновом режиме, но не выполняет 
            никаких действий.</p>
            
            <h3>Задержка перед выключением</h3>
            <p>Время в минутах, которое должно пройти после отключения компьютера от электрической сети, 
            прежде чем будет запущена процедура выключения. Минимальное значение: 1 минута. 
            Максимальное значение: 60 минут.</p>
            
            <div class="important">
                <strong>Важно:</strong> Таймер запускается только при переходе на батарею. Если вы снова 
                подключите зарядное устройство, таймер автоматически отменяется.
            </div>
            
            <h3>Минимальный заряд батареи</h3>
            <p>Процент заряда аккумуляторной батареи, при достижении которого (или ниже) компьютер 
            будет выключен. Например, если установлено значение 50%, то выключение произойдёт только 
            в том случае, если заряд батареи составляет 50% или менее.</p>
            
            <p>Это дополнительное условие защиты. Даже если истекло установленное время задержки, 
            компьютер не будет выключен, пока заряд батареи не опустится до указанного уровня.</p>
            
            <h3>Звуковые оповещения</h3>
            <p>Когда данная настройка включена, при появлении окна предупреждения о выключении 
            будет воспроизводиться звуковой сигнал. Это помогает привлечь ваше внимание, если вы 
            не находитесь непосредственно перед экраном компьютера.</p>
            
            <h3>Автозапуск при старте Windows</h3>
            <p>Когда данная настройка включена, программа будет автоматически запускаться при загрузке 
            операционной системы Windows. Это удобно, если вы хотите, чтобы защита от разрядки батареи 
            работала постоянно, без необходимости вручную запускать программу каждый раз.</p>
            
            <h2>Окно предупреждения о выключении</h2>
            <p>За 30 секунд до выключения компьютера появляется специальное окно предупреждения. 
            В этом окне:</p>
            <ul>
                <li>Отображается обратный отсчёт времени до выключения</li>
                <li>Присутствует кнопка "ОТМЕНИТЬ ВЫКЛЮЧЕНИЕ"</li>
            </ul>
            
            <p><strong>Если вы нажмёте кнопку отмены:</strong></p>
            <ul>
                <li>Выключение компьютера будет отменено</li>
                <li>Функция автовыключения автоматически отключится</li>
                <li>Вам потребуется вручную включить её снова, если она понадобится</li>
            </ul>
            
            <p><strong>Если вы проигнорируете окно:</strong></p>
            <ul>
                <li>По истечении 30 секунд компьютер будет выключен</li>
            </ul>
            
            <h2>Работа в системном трее</h2>
            <p>Когда вы закрываете главное окно программы, она не завершает свою работу, а сворачивается 
            в область уведомлений (системный трей) возле часов.</p>
            
            <p><strong>Двойной щелчок левой кнопкой мыши</strong> по значку программы в трее — 
            открывает главное окно программы.</p>
            
            <p><strong>Щелчок правой кнопкой мыши</strong> по значку программы — открывает меню 
            с пунктами "Показать" (открыть окно) и "Выход" (полностью закрыть программу).</p>
            
            <h2>Текущий статус</h2>
            <p>В главном окне программы отображается следующая информация:</p>
            <ul>
                <li><strong>Питание:</strong> показывает, подключён ли компьютер к электрической сети 
                или работает от батареи</li>
                <li><strong>Заряд батареи:</strong> текущий уровень заряда в процентах</li>
                <li><strong>Состояние автовыключения:</strong> включена ли функция</li>
                <li><strong>Таймер обратного отсчёта:</strong> если компьютер работает от батареи 
                и таймер активен, отображается оставшееся время до выключения</li>
            </ul>
            
            <div class="important">
                <strong>Примечание:</strong> Программа сохраняет все настройки автоматически. 
                При следующем запуске программы ваши настройки будут восстановлены.
            </div>
            
            <h2>Полное закрытие программы</h2>
            <p>Для полного завершения работы программы используйте кнопку "Полностью закрыть приложение" 
            в нижней части главного окна. Это полностью остановит работу программы и удалит её из 
            системного трея.</p>
        </body>
        </html>
        """

class BatteryMonitor(threading.Thread):
    def __init__(self, config, signals):
        super().__init__()
        self.config = config
        self.signals = signals
        self.running = True
        self.daemon = True
        self.was_on_ac = True
        self.timer_started = False
        self.shutdown_time = None

    def run(self):
        while self.running:
            if self.config['enabled']:
                battery = psutil.sensors_battery()
                
                if battery:
                    on_ac = battery.power_plugged
                    percent = battery.percent
                    
                    # Переход с сети на батарею
                    if self.was_on_ac and not on_ac:
                        if not self.timer_started:
                            self.timer_started = True
                            self.shutdown_time = time.time() + (self.config['delay_minutes'] * 60)
                            print(f"Переход на батарею. Таймер запущен на {self.config['delay_minutes']} мин.")
                    
                    # Вернулись на сеть - отменяем таймер
                    if not self.was_on_ac and on_ac:
                        if self.timer_started:
                            self.timer_started = False
                            self.shutdown_time = None
                            print("Подключено к сети. Таймер отменён.")
                    
                    # Проверяем условия выключения
                    if self.timer_started and not on_ac:
                        if time.time() >= self.shutdown_time and percent <= self.config['battery_percent']:
                            print(f"Выключение! Заряд: {percent}%")
                            self.signals.shutdown_triggered.emit()
                            self.timer_started = False
                    
                    self.was_on_ac = on_ac
                    
            time.sleep(2)
    
    def stop(self):
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config_file = self.get_config_path()
        self.config = self.load_config()
        
        self.signals = WorkerSignals()
        self.signals.shutdown_triggered.connect(self.show_shutdown_dialog)
        
        self.monitor = BatteryMonitor(self.config, self.signals)
        self.monitor.start()
        
        self.init_ui()
        self.init_tray()
        self.update_status_timer = QTimer()
        self.update_status_timer.timeout.connect(self.update_status)
        self.update_status_timer.start(1000)
    
    def get_config_path(self):
        """Получает путь к файлу конфигурации в папке пользователя"""
        app_data_dir = Path.home() / '.battery_shutdown'
        app_data_dir.mkdir(exist_ok=True)
        return str(app_data_dir / 'config.json')
        
    def load_config(self):
        default_config = {
            'enabled': False,
            'delay_minutes': 5,
            'battery_percent': 50,
            'sound_enabled': True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    # Добавляем новые настройки если их нет
                    for key in default_config:
                        if key not in loaded:
                            loaded[key] = default_config[key]
                    return loaded
            except:
                return default_config
        return default_config
    
    def save_config(self):
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def init_ui(self):
        self.setWindowTitle('Автовыключение при работе от батареи')
        self.setFixedSize(450, 350)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Группа управления
        control_group = QGroupBox('Управление')
        control_layout = QVBoxLayout()
        
        self.enable_checkbox = QCheckBox('Включить автовыключение')
        self.enable_checkbox.setChecked(self.config['enabled'])
        self.enable_checkbox.stateChanged.connect(self.on_enable_changed)
        control_layout.addWidget(self.enable_checkbox)
        
        control_group.setLayout(control_layout)
        layout.addWidget(control_group)
        
        # Группа статуса с прокруткой
        status_group = QGroupBox('Текущий статус')
        status_group_layout = QVBoxLayout()
        
        # Создаём область прокрутки для статуса
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(120)
        scroll_area.setMaximumHeight(120)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        
        status_widget = QWidget()
        status_widget_layout = QVBoxLayout(status_widget)
        status_widget_layout.setContentsMargins(5, 5, 5, 5)
        
        self.status_label = QLabel('Загрузка...')
        self.status_label.setWordWrap(True)
        self.status_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        status_widget_layout.addWidget(self.status_label)
        status_widget_layout.addStretch()
        
        scroll_area.setWidget(status_widget)
        status_group_layout.addWidget(scroll_area)
        status_group.setLayout(status_group_layout)
        layout.addWidget(status_group)
        
        layout.addStretch()
        
        # Кнопки
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Кнопка настроек
        settings_button = QPushButton('⚙️ Настройки')
        settings_button.clicked.connect(self.show_settings)
        settings_button.setStyleSheet('QPushButton { background-color: #3498db; color: white; padding: 8px; }')
        buttons_layout.addWidget(settings_button)
        
        # Кнопка помощи
        help_button = QPushButton('📖 Помощь (FAQ)')
        help_button.clicked.connect(self.show_help)
        help_button.setStyleSheet('QPushButton { background-color: #95a5a6; color: white; padding: 8px; }')
        buttons_layout.addWidget(help_button)
        
        # Кнопка выхода
        exit_button = QPushButton('Полностью закрыть приложение')
        exit_button.clicked.connect(self.quit_application)
        exit_button.setStyleSheet('QPushButton { background-color: #ff4444; color: white; padding: 8px; }')
        buttons_layout.addWidget(exit_button)
        
        layout.addLayout(buttons_layout)
        
        self.update_status()
    
    def init_tray(self):
        # Создаём иконку для трея
        icon = self.create_icon()
        
        self.tray_icon = QSystemTrayIcon(icon, self)
        
        # Меню трея
        tray_menu = QMenu()
        show_action = tray_menu.addAction('Показать')
        show_action.triggered.connect(self.show)
        
        quit_action = tray_menu.addAction('Выход')
        quit_action.triggered.connect(self.quit_application)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()
    
    def create_icon(self):
        """Создаёт простую иконку"""
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Рисуем батарею
        painter.setBrush(QColor(100, 150, 255))
        painter.setPen(QColor(50, 100, 200))
        painter.drawRoundedRect(8, 20, 40, 24, 4, 4)
        painter.drawRect(48, 28, 8, 8)
        
        painter.end()
        
        return QIcon(pixmap)
    
    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.activateWindow()
    
    def on_enable_changed(self):
        self.config['enabled'] = self.enable_checkbox.isChecked()
        self.save_config()
        
        if self.config['enabled']:
            self.tray_icon.showMessage(
                'Автовыключение',
                'Функция автовыключения включена',
                QSystemTrayIcon.Information,
                2000
            )
    
    def show_settings(self):
        """Открывает окно настроек"""
        dialog = SettingsDialog(self, self.config)
        if dialog.exec_() == QDialog.Accepted:
            # Настройки сохранены
            pass
    
    def show_help(self):
        """Показывает окно помощи"""
        help_dialog = HelpDialog(self)
        help_dialog.exec_()
    
    def update_status(self):
        battery = psutil.sensors_battery()
        
        if battery:
            status = 'Подключено к сети' if battery.power_plugged else 'Работа от батареи'
            percent = battery.percent
            
            status_text = f'Питание: {status}\n'
            status_text += f'Заряд батареи: {percent}%\n'
            
            if self.config['enabled']:
                status_text += f'\n✓ Автовыключение включено'
                if not battery.power_plugged and self.monitor.timer_started:
                    remaining = int(self.monitor.shutdown_time - time.time())
                    if remaining > 0:
                        status_text += f'\n⏱ До выключения: {remaining // 60} мин {remaining % 60} сек'
            else:
                status_text += f'\n✗ Автовыключение выключено'
            
            self.status_label.setText(status_text)
        else:
            self.status_label.setText('Батарея не обнаружена')
    
    def show_shutdown_dialog(self):
        """Показывает диалог с предупреждением о выключении"""
        dialog = ShutdownDialog(self, self.config['sound_enabled'])
        result = dialog.exec_()
        
        if dialog.cancelled:
            # Пользователь отменил выключение
            self.config['enabled'] = False
            self.enable_checkbox.setChecked(False)
            self.save_config()
            
            self.tray_icon.showMessage(
                'Выключение отменено',
                'Автовыключение было отключено',
                QSystemTrayIcon.Information,
                3000
            )
        elif result == QDialog.Accepted:
            # Таймер истёк, выключаем компьютер
            self.execute_shutdown()
    
    def execute_shutdown(self):
        """Выполняет выключение компьютера"""
        if sys.platform == 'win32':
            os.system('shutdown /s /t 0')
        elif sys.platform == 'darwin':
            os.system('sudo shutdown -h now')
        else:
            os.system('shutdown -h now')
    
    def closeEvent(self, event):
        """При закрытии окна сворачиваем в трей"""
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            'Приложение свёрнуто',
            'Приложение продолжает работать в трее',
            QSystemTrayIcon.Information,
            2000
        )
    
    def quit_application(self):
        """Полное закрытие приложения"""
        self.monitor.stop()
        self.tray_icon.hide()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())