# GarudaTalon is a program for monitoring CPU, RAM and DISK parameters
from colorama import Fore, init
init(autoreset=True)
import time
import pygame
import psutil
import sys
import os
soundfile = "Alarm_sound.mp3"


class Sensor:
    count = 0
    active_monitoring = False

    def __init__(self, type, level=0, active_monitoring=False):
        self.type = type
        self.level = level
        Sensor.count += 1
        self.active_monitoring = active_monitoring 

    @classmethod
    def display_usage(cls, refresh=0.2):
        try:
            while cls.active_monitoring:
                disk = psutil.disk_usage('/')
                ram  = psutil.virtual_memory()
                cpu  = psutil.cpu_percent(interval=None)  

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
    
class Alarms:
    def __init__(self):
        pass

    # Arm state per kind
    ON   = {"cpu": False, "ram": False, "disk": False}
    OVER = {"cpu": False, "ram": False, "disk": False}

    def alarm_menu(self):
        while True:
            print(Fore.WHITE + "--- ALARM CONFIGURATION ---\n",
                Fore.BLUE + "1. CPU USAGE\n",
                Fore.BLUE + "2. RAM USAGE\n",
                Fore.BLUE + "3. DISK USAGE\n",
                Fore.BLUE + "4. REMOVE ALARM\n",
                Fore.MAGENTA + "5. EXIT TO MAIN MENU")
            choice = input("Enter a value between 1-5: ").strip()
            if choice == "1":
                self.cpu_config()
            elif choice == "2":
                self.ram_config()
            elif choice == "3":
                self.disk_config()
            elif choice == "4":
                self.remove_alarm()
            elif choice == "5":
                print(Fore.CYAN + "Exiting to main menu...")
                psutil.cpu_percent(interval=None)
                return
            else:
                print(Fore.RED + "ERROR! Enter a valid number between 1-5.")

    def init_sound():
        try:
            pygame.mixer.init()
        except Exception as e:
            print(Fore.RED + f"[WARN] pygame init fail: {e}")

    def play_sound():
        try:
            if os.path.isfile(soundfile):
                pygame.mixer.music.load(soundfile)
                pygame.mixer.music.play()
            else:
                print(Fore.RED + f"[WARN] sound not found: {soundfile}")
        except Exception as e:
            print(Fore.RED + f"[WARN] sound play fail: {e}")

    
    def cpu_config(self):
        pct = ask_pct("CPU")
        add_alarm(load_alarms(), kind="cpu", threshold=pct, enabled=True)
        ON["cpu"] = True
        print(f"CPU threshold saved at {pct}%")

    def ram_config(self):
        pct = ask_pct("RAM")
        add_alarm(load_alarms(), kind="ram", threshold=pct, enabled=True)
        ON["ram"] = True
        print(f"RAM threshold saved at {pct}%")

    def disk_config(self):
        pct = ask_pct("DISK")
        add_alarm(load_alarms(), kind="disk", threshold=pct, enabled=True)
        ON["disk"] = True
        print(f"DISK threshold saved at {pct}%")

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
                Alarms.alarm_menu()
            elif choice == 5:
                pass
            elif choice == 6:
                Sensor.display_usage()
            elif choice == 7:
                print("Logging off...")
                time.sleep(1.5)
                break
            else:
                return ("Please enter a valid menu choice: ")


Garudamenus.main_menu()
