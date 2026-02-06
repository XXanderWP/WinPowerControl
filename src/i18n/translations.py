"""
Internationalization module for Battery Shutdown
Supports English, Russian, and Ukrainian languages
"""

import locale

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Window titles
        'main_window_title': 'Battery Auto-Shutdown',
        'settings_title': 'Settings',
        'help_title': 'Help - Battery Auto-Shutdown',
        'shutdown_warning_title': 'Shutdown Warning',
        
        # Main window
        'control_group': 'Control',
        'enable_auto_shutdown': 'Enable auto-shutdown',
        'current_status': 'Current Status',
        'loading': 'Loading...',
        'settings_button': '⚙️ Settings',
        'help_button': '📖 Help (FAQ)',
        'exit_button': 'Completely close application',
        
        # Status messages
        'power_connected': 'Connected to AC power',
        'power_battery': 'Running on battery',
        'battery_charge': 'Battery charge',
        'auto_shutdown_enabled': '✓ Auto-shutdown enabled',
        'auto_shutdown_disabled': '✗ Auto-shutdown disabled',
        'time_until_shutdown': '⏱ Time until shutdown',
        'minutes_short': 'min',
        'seconds_short': 'sec',
        'battery_not_detected': '⚠️ Battery not detected',
        
        # Settings dialog
        'main_settings': 'Main Settings',
        'delay_before_shutdown': 'Delay before shutdown:',
        'min_battery_percent': 'Minimum battery charge:',
        'additional_settings': 'Additional Settings',
        'sound_notifications': 'Sound notifications',
        'autostart_system': 'Run at system startup',
        'save_button': 'Save',
        'cancel_button': 'Cancel',
        
        # Shutdown dialog
        'warning_attention': '⚠️ WARNING!',
        'computer_shutdown_in': 'Computer will shut down in {seconds} seconds',
        'cancel_shutdown_button': 'CANCEL SHUTDOWN',
        
        # Tray notifications
        'app_minimized': 'Application minimized',
        'app_running_in_tray': 'Application continues running in tray',
        'auto_shutdown_on': 'Auto-shutdown',
        'function_enabled': 'Auto-shutdown function enabled',
        'shutdown_cancelled': 'Shutdown cancelled',
        'auto_shutdown_disabled_msg': 'Auto-shutdown has been disabled',
        
        # Help content keys
        'help_purpose_title': 'Purpose of the Program',
        'help_how_it_works_title': 'How the Program Works',
        'help_settings_title': 'Settings Description',
        'help_warning_dialog_title': 'Shutdown Warning Dialog',
        'help_tray_title': 'System Tray Operation',
        'help_current_status_title': 'Current Status',
        'help_full_exit_title': 'Complete Program Shutdown',
    },
    'ru': {
        # Заголовки окон
        'main_window_title': 'Автовыключение при работе от батареи',
        'settings_title': 'Настройки',
        'help_title': 'Помощь - Автовыключение при работе от батареи',
        'shutdown_warning_title': 'Предупреждение о выключении',
        
        # Главное окно
        'control_group': 'Управление',
        'enable_auto_shutdown': 'Включить автовыключение',
        'current_status': 'Текущий статус',
        'loading': 'Загрузка...',
        'settings_button': '⚙️ Настройки',
        'help_button': '📖 Помощь (FAQ)',
        'exit_button': 'Полностью закрыть приложение',
        
        # Статусные сообщения
        'power_connected': 'Подключено к сети',
        'power_battery': 'Работа от батареи',
        'battery_charge': 'Заряд батареи',
        'auto_shutdown_enabled': '✓ Автовыключение включено',
        'auto_shutdown_disabled': '✗ Автовыключение выключено',
        'time_until_shutdown': '⏱ До выключения',
        'minutes_short': 'мин',
        'seconds_short': 'сек',
        'battery_not_detected': '⚠️ Батарея не обнаружена',
        
        # Диалог настроек
        'main_settings': 'Основные настройки',
        'delay_before_shutdown': 'Задержка перед выключением:',
        'min_battery_percent': 'Минимальный заряд батареи:',
        'additional_settings': 'Дополнительные настройки',
        'sound_notifications': 'Звуковые оповещения',
        'autostart_system': 'Автозапуск при старте системы',
        'save_button': 'Сохранить',
        'cancel_button': 'Отмена',
        
        # Диалог выключения
        'warning_attention': '⚠️ ВНИМАНИЕ!',
        'computer_shutdown_in': 'Компьютер будет выключен через {seconds} секунд',
        'cancel_shutdown_button': 'ОТМЕНИТЬ ВЫКЛЮЧЕНИЕ',
        
        # Уведомления трея
        'app_minimized': 'Приложение свёрнуто',
        'app_running_in_tray': 'Приложение продолжает работать в трее',
        'auto_shutdown_on': 'Автовыключение',
        'function_enabled': 'Функция автовыключения включена',
        'shutdown_cancelled': 'Выключение отменено',
        'auto_shutdown_disabled_msg': 'Автовыключение было отключено',
        
        # Ключи содержимого помощи
        'help_purpose_title': 'Назначение программы',
        'help_how_it_works_title': 'Как работает программа',
        'help_settings_title': 'Описание настроек',
        'help_warning_dialog_title': 'Окно предупреждения о выключении',
        'help_tray_title': 'Работа в системном трее',
        'help_current_status_title': 'Текущий статус',
        'help_full_exit_title': 'Полное закрытие программы',
    },
    'uk': {
        # Заголовки вікон
        'main_window_title': 'Автовимикання при роботі від батареї',
        'settings_title': 'Налаштування',
        'help_title': 'Довідка - Автовимикання при роботі від батареї',
        'shutdown_warning_title': 'Попередження про вимикання',
        
        # Головне вікно
        'control_group': 'Керування',
        'enable_auto_shutdown': 'Увімкнути автовимикання',
        'current_status': 'Поточний статус',
        'loading': 'Завантаження...',
        'settings_button': '⚙️ Налаштування',
        'help_button': '📖 Довідка (FAQ)',
        'exit_button': 'Повністю закрити додаток',
        
        # Статусні повідомлення
        'power_connected': 'Підключено до мережі',
        'power_battery': 'Робота від батареї',
        'battery_charge': 'Заряд батареї',
        'auto_shutdown_enabled': '✓ Автовимикання увімкнено',
        'auto_shutdown_disabled': '✗ Автовимикання вимкнено',
        'time_until_shutdown': '⏱ До вимикання',
        'minutes_short': 'хв',
        'seconds_short': 'сек',
        'battery_not_detected': '⚠️ Батарею не виявлено',
        
        # Діалог налаштувань
        'main_settings': 'Основні налаштування',
        'delay_before_shutdown': 'Затримка перед вимиканням:',
        'min_battery_percent': 'Мінімальний заряд батареї:',
        'additional_settings': 'Додаткові налаштування',
        'sound_notifications': 'Звукові сповіщення',
        'autostart_system': 'Автозапуск при старті системи',
        'save_button': 'Зберегти',
        'cancel_button': 'Скасувати',
        
        # Діалог вимикання
        'warning_attention': '⚠️ УВАГА!',
        'computer_shutdown_in': 'Комп\'ютер буде вимкнено через {seconds} секунд',
        'cancel_shutdown_button': 'СКАСУВАТИ ВИМИКАННЯ',
        
        # Сповіщення трею
        'app_minimized': 'Додаток згорнуто',
        'app_running_in_tray': 'Додаток продовжує працювати в треї',
        'auto_shutdown_on': 'Автовимикання',
        'function_enabled': 'Функцію автовимикання увімкнено',
        'shutdown_cancelled': 'Вимикання скасовано',
        'auto_shutdown_disabled_msg': 'Автовимикання було вимкнено',
        
        # Ключі вмісту довідки
        'help_purpose_title': 'Призначення програми',
        'help_how_it_works_title': 'Як працює програма',
        'help_settings_title': 'Опис налаштувань',
        'help_warning_dialog_title': 'Вікно попередження про вимикання',
        'help_tray_title': 'Робота в системному треї',
        'help_current_status_title': 'Поточний статус',
        'help_full_exit_title': 'Повне закриття програми',
    }
}


class Translator:
    """Handles application translations"""
    
    def __init__(self):
        self.current_language = self._detect_system_language()
    
    def _detect_system_language(self):
        """Detect system language and set appropriate translation"""
        try:
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                lang_code = system_locale.split('_')[0].lower()
                if lang_code in TRANSLATIONS:
                    return lang_code
        except:
            pass
        return 'en'  # Default to English
    
    def get(self, key, **kwargs):
        """Get translated string by key with optional formatting"""
        translation = TRANSLATIONS.get(self.current_language, TRANSLATIONS['en']).get(key, key)
        if kwargs:
            return translation.format(**kwargs)
        return translation
    
    def set_language(self, lang_code):
        """Manually set language"""
        if lang_code in TRANSLATIONS:
            self.current_language = lang_code
    
    def get_available_languages(self):
        """Get list of available language codes"""
        return list(TRANSLATIONS.keys())
    
    def get_language_name(self, lang_code):
        """Get human-readable language name"""
        names = {
            'en': 'English',
            'ru': 'Русский',
            'uk': 'Українська'
        }
        return names.get(lang_code, lang_code)


# Global translator instance
translator = Translator()