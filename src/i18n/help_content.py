"""
Help content for different languages
Contains detailed user documentation
"""

HELP_CONTENT = {
    'en': """
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
            <h2>Purpose of the Program</h2>
            <p>This program is designed to automatically shut down the computer when it transitions 
            to battery power. This is useful in situations where you want to prevent complete 
            battery discharge if the charger is accidentally disconnected.</p>
            
            <h2>How the Program Works</h2>
            <p>The program constantly monitors your computer's power status. When disconnection from 
            AC power occurs and the computer starts running on battery, a special countdown timer is started.</p>
            
            <p>If after the set time the computer is still running on battery and the battery charge 
            drops to the value you specified, the program initiates the computer shutdown procedure.</p>
            
            <h2>Settings Description</h2>
            
            <h3>Enable Auto-Shutdown</h3>
            <p>Main program switch. When enabled, the program actively monitors power status. 
            When disabled, the program runs in the background but performs no actions.</p>
            
            <h3>Delay Before Shutdown</h3>
            <p>Time in minutes that must pass after disconnecting from AC power before 
            the shutdown procedure is initiated. Minimum value: 1 minute. Maximum value: 60 minutes.</p>
            
            <div class="important">
                <strong>Important:</strong> The timer starts only when transitioning to battery. 
                If you reconnect the charger, the timer is automatically cancelled.
            </div>
            
            <h3>Minimum Battery Charge</h3>
            <p>Battery charge percentage at which (or below) the computer will be shut down. 
            For example, if set to 50%, shutdown will occur only if the battery charge is 50% or less.</p>
            
            <p>This is an additional protection condition. Even if the set delay time has elapsed, 
            the computer will not shut down until the battery charge drops to the specified level.</p>
            
            <h3>Sound Notifications</h3>
            <p>When this setting is enabled, a sound signal will play when the shutdown warning 
            window appears. This helps draw your attention if you're not directly in front of the screen.</p>
            
            <h3>Run at Windows Startup</h3>
            <p>When this setting is enabled, the program will automatically start when Windows boots. 
            This is convenient if you want battery discharge protection to work constantly, without 
            manually starting the program each time.</p>
            
            <h2>Shutdown Warning Dialog</h2>
            <p>30 seconds before computer shutdown, a special warning window appears. This window shows:</p>
            <ul>
                <li>Countdown to shutdown</li>
                <li>"CANCEL SHUTDOWN" button</li>
            </ul>
            
            <p><strong>If you press the cancel button:</strong></p>
            <ul>
                <li>Computer shutdown will be cancelled</li>
                <li>Auto-shutdown function will be automatically disabled</li>
                <li>You'll need to manually enable it again if needed</li>
            </ul>
            
            <p><strong>If you ignore the window:</strong></p>
            <ul>
                <li>After 30 seconds the computer will shut down</li>
            </ul>
            
            <h2>System Tray Operation</h2>
            <p>When you close the main program window, it doesn't terminate but minimizes to the 
            notification area (system tray) near the clock.</p>
            
            <p><strong>Double-click left mouse button</strong> on the program icon in the tray 
            opens the main program window.</p>
            
            <p><strong>Right-click</strong> on the program icon opens a menu with 
            "Show" (open window) and "Exit" (completely close program) options.</p>
            
            <h2>Current Status</h2>
            <p>The main program window displays the following information:</p>
            <ul>
                <li><strong>Power:</strong> shows whether the computer is connected to AC power 
                or running on battery</li>
                <li><strong>Battery Charge:</strong> current charge level in percentage</li>
                <li><strong>Auto-Shutdown Status:</strong> whether the function is enabled</li>
                <li><strong>Countdown Timer:</strong> if the computer is running on battery 
                and the timer is active, shows remaining time until shutdown</li>
            </ul>
            
            <div class="important">
                <strong>Note:</strong> The program saves all settings automatically. 
                On next program start, your settings will be restored.
            </div>
            
            <h2>Complete Program Shutdown</h2>
            <p>To completely terminate the program, use the "Completely close application" button 
            at the bottom of the main window. This will completely stop the program and remove it 
            from the system tray.</p>
        </body>
        </html>
    """,
    'ru': """
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
    """,
    'uk': """
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
            <h2>Призначення програми</h2>
            <p>Ця програма призначена для автоматичного вимикання комп'ютера при переході 
            на живлення від акумуляторної батареї. Це корисно в ситуаціях, коли ви хочете запобігти 
            повному розрядженню батареї ноутбука при випадковому відключенні зарядного пристрою.</p>
            
            <h2>Як працює програма</h2>
            <p>Програма постійно відстежує стан живлення вашого комп'ютера. Коли відбувається 
            відключення від електричної мережі і комп'ютер починає працювати від батареї, запускається 
            спеціальний таймер зворотного відліку.</p>
            
            <p>Якщо після встановленого часу комп'ютер все ще працює від батареї і рівень 
            її заряду знижується до вказаного вами значення, програма ініціює процедуру вимикання 
            комп'ютера.</p>
            
            <h2>Опис налаштувань</h2>
            
            <h3>Увімкнути автовимикання</h3>
            <p>Основний перемикач програми. Коли він увімкнений, програма активно відстежує 
            стан живлення. Коли вимкнений — програма працює у фоновому режимі, але не виконує 
            жодних дій.</p>
            
            <h3>Затримка перед вимиканням</h3>
            <p>Час у хвилинах, який має минути після відключення комп'ютера від електричної мережі, 
            перш ніж буде запущено процедуру вимикання. Мінімальне значення: 1 хвилина. 
            Максимальне значення: 60 хвилин.</p>
            
            <div class="important">
                <strong>Важливо:</strong> Таймер запускається тільки при переході на батарею. Якщо ви знову 
                підключите зарядний пристрій, таймер автоматично скасовується.
            </div>
            
            <h3>Мінімальний заряд батареї</h3>
            <p>Відсоток заряду акумуляторної батареї, при досягненні якого (або нижче) комп'ютер 
            буде вимкнено. Наприклад, якщо встановлено значення 50%, то вимикання відбудеться тільки 
            в тому випадку, якщо заряд батареї становить 50% або менше.</p>
            
            <p>Це додаткова умова захисту. Навіть якщо минув встановлений час затримки, 
            комп'ютер не буде вимкнено, поки заряд батареї не опуститься до вказаного рівня.</p>
            
            <h3>Звукові сповіщення</h3>
            <p>Коли це налаштування увімкнено, при появі вікна попередження про вимикання 
            буде відтворюватися звуковий сигнал. Це допомагає привернути вашу увагу, якщо ви 
            не перебуваєте безпосередньо перед екраном комп'ютера.</p>
            
            <h3>Автозапуск при старті Windows</h3>
            <p>Коли це налаштування увімкнено, програма буде автоматично запускатися при завантаженні 
            операційної системи Windows. Це зручно, якщо ви хочете, щоб захист від розрядження батареї 
            працював постійно, без необхідності вручну запускати програму щоразу.</p>
            
            <h2>Вікно попередження про вимикання</h2>
            <p>За 30 секунд до вимикання комп'ютера з'являється спеціальне вікно попередження. 
            У цьому вікні:</p>
            <ul>
                <li>Відображається зворотний відлік часу до вимикання</li>
                <li>Присутня кнопка "СКАСУВАТИ ВИМИКАННЯ"</li>
            </ul>
            
            <p><strong>Якщо ви натиснете кнопку скасування:</strong></p>
            <ul>
                <li>Вимикання комп'ютера буде скасовано</li>
                <li>Функція автовимикання автоматично вимкнеться</li>
                <li>Вам потрібно буде вручну увімкнути її знову, якщо вона знадобиться</li>
            </ul>
            
            <p><strong>Якщо ви проігноруєте вікно:</strong></p>
            <ul>
                <li>Після 30 секунд комп'ютер буде вимкнено</li>
            </ul>
            
            <h2>Робота в системному треї</h2>
            <p>Коли ви закриваєте головне вікно програми, вона не завершує свою роботу, а згортається 
            в область сповіщень (системний трей) біля годинника.</p>
            
            <p><strong>Подвійний клік лівою кнопкою миші</strong> по значку програми в треї — 
            відкриває головне вікно програми.</p>
            
            <p><strong>Клік правою кнопкою миші</strong> по значку програми — відкриває меню 
            з пунктами "Показати" (відкрити вікно) та "Вихід" (повністю закрити програму).</p>
            
            <h2>Поточний статус</h2>
            <p>У головному вікні програми відображається наступна інформація:</p>
            <ul>
                <li><strong>Живлення:</strong> показує, чи підключений комп'ютер до електричної мережі 
                або працює від батареї</li>
                <li><strong>Заряд батареї:</strong> поточний рівень заряду у відсотках</li>
                <li><strong>Стан автовимикання:</strong> чи увімкнена функція</li>
                <li><strong>Таймер зворотного відліку:</strong> якщо комп'ютер працює від батареї 
                та таймер активний, відображається час, що залишився до вимикання</li>
            </ul>
            
            <div class="important">
                <strong>Примітка:</strong> Програма зберігає всі налаштування автоматично. 
                При наступному запуску програми ваші налаштування будуть відновлені.
            </div>
            
            <h2>Повне закриття програми</h2>
            <p>Для повного завершення роботи програми використовуйте кнопку "Повністю закрити додаток" 
            у нижній частині головного вікна. Це повністю зупинить роботу програми та видалить її з 
            системного трею.</p>
        </body>
        </html>
    """
}