# GarudaTalon is a program for monitoring CPU, RAM and DISK parameters
from colorama import Fore, init
init(autoreset=True)
import time
import psutil
import sys


class Sensor:
    count = 0
    active_monitoring = False

    def __init__(self, type, level=0, active_monitoring=False):
        self.type = type
        self.level = level
        Sensor.count += 1
        self.active_monitoring = active_monitoring  # lämnas kvar för minimal diff, används ej nedan

    @classmethod
    def display_usage(cls, refresh=0.2):
        try:
            while cls.active_monitoring:
                disk = psutil.disk_usage('/')
                ram  = psutil.virtual_memory()
                cpu  = psutil.cpu_percent(interval=None)  # undvik blockering

                total_disk_gb = disk.total / (1024**3)
                used_disk_gb  = disk.used  / (1024**3)
                total_ram_gb  = ram.total  / (1024**3)
                used_ram_gb   = (ram.total - ram.available) / (1024**3)

                line = (f"CPU: {cpu:5.1f}% | RAM: {ram.percent:5.1f}% "
                        f"({used_ram_gb:.0f}/{total_ram_gb:.0f} GB) | "
                        f"DISK: {disk.percent:5.1f}% "
                        f"({used_disk_gb:.0f}/{total_disk_gb:.0f} GB)")
                sys.stdout.write("\r" + line + " " * 8)
                sys.stdout.flush()
                time.sleep(refresh)
        except KeyboardInterrupt:
            pass

    def __str__(self):
        return f"Sensor: {self.type} at level {self.level}%, number of sensors # {Sensor.count}"

    @classmethod
    def start_monitoring(cls):
        cls.active_monitoring = True

    @classmethod
    def stop_monitoring(cls):
        cls.active_monitoring = False

    def is_alarm_triggered(self, threshold):
        if self.level < threshold:
            return False
        elif self.level >= threshold:
            return True

    @classmethod
    def show_status(cls):
        return "Monitor is running" if cls.active_monitoring else "No active monitoring..."


class Garudamenus:
    def __init__(self):
        pass

    @staticmethod
    def main_menu():
        while True:
            print(
                Fore.WHITE + "*** Main Menu ***\n",
                Fore.BLUE + "1. START MONITORING\n",
                Fore.BLUE + "2. STOP MONITORING\n",
                Fore.BLUE + "3. LIST ACTIVE MONITORING\n",
                Fore.BLUE + "4. CONFIGURE ALARMS\n",
                Fore.BLUE + "5. SHOW ALARMS\n",
                Fore.BLUE + "6. START MONITORING MODE\n",
                Fore.MAGENTA + "7. EXIT PROGRAM\n"
            )

            choice = int(input("Enter a number between 1-7: "))

            if choice == 1:
                print("Monitoring started...")
                Sensor.start_monitoring()
            elif choice == 2:
                Sensor.stop_monitoring()
                print("Monitoring stopped...")
            elif choice == 3:
                print(Sensor.show_status())
            elif choice == 4:
                pass
            elif choice == 5:
                pass
            elif choice == 6:
                # kör visningen så länge flaggan är True
                Sensor.display_usage()
            elif choice == 7:
                print("Logging off...")
                time.sleep(1.5)
                break
            else:
                return ("Please enter a valid menu choice: ")


Garudamenus.main_menu()
