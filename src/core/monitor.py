"""
Battery monitoring thread
Monitors battery status and triggers shutdown when conditions are met
"""

import threading
import time
import psutil


class BatteryMonitor(threading.Thread):
    """Background thread that monitors battery status"""
    
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
        """Main monitoring loop"""
        while self.running:
            if self.config['enabled']:
                battery = psutil.sensors_battery()
                
                if battery:
                    on_ac = battery.power_plugged
                    percent = battery.percent
                    
                    # Transition from AC to battery
                    if self.was_on_ac and not on_ac:
                        if not self.timer_started:
                            self.timer_started = True
                            self.shutdown_time = time.time() + (self.config['delay_minutes'] * 60)
                            print(f"Transitioned to battery. Timer started for {self.config['delay_minutes']} minutes.")
                    
                    # Returned to AC - cancel timer
                    if not self.was_on_ac and on_ac:
                        if self.timer_started:
                            self.timer_started = False
                            self.shutdown_time = None
                            print("Connected to AC power. Timer cancelled.")
                    
                    # Check shutdown conditions
                    if self.timer_started and not on_ac:
                        if time.time() >= self.shutdown_time and percent <= self.config['battery_percent']:
                            print(f"Shutdown triggered! Battery: {percent}%")
                            self.signals.shutdown_triggered.emit()
                            self.timer_started = False
                    
                    self.was_on_ac = on_ac
                    
            time.sleep(2)
    
    def stop(self):
        """Stop the monitoring thread"""
        self.running = False