# main.py

import psutil
from colorama import Fore, init
import sys
import os
import time
from configurations import User_alarms
from metric_data import Sensors
from pathlib import Path
import json
from datetime import datetime
init(autoreset=True) #Colorama resets everytime so not every code gets one color
BASE_DIR = Path(__file__).resolve().parent
session_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

log_filename = f"log_{session_timestamp}.jsonl" #Timestamp for the log-files

LOG_FILE_PATH = BASE_DIR / log_filename
class Main(): 
    def __init__(self, name=None):
        self.name = name
        self.sensors = Sensors()
        self.user_alarms = User_alarms(logger_func=self.event_logger)
        # This flag represents if the system is "armed" or not.
        self.monitoring_active = False

    def event_logger(self, log):
        LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_log_entry = {"timestamp": timestamp, "message": log}

        with open(LOG_FILE_PATH, "a") as file:
            json_log_line = json.dumps(new_log_entry)
            file.write(json_log_line + "\n")


    def start_monitoring(self):
        """This function only 'arms' the system in the background."""
        if self.monitoring_active:
            print(Fore.YELLOW + "Monitoring is already active.")
            return
        self.monitoring_active = True
        print(Fore.GREEN + "Monitoring has been started (System is ARMED).")
        self.event_logger("Monitoring armed")

    def stop_monitoring(self):
        """This function 'disarms' the system."""
        if not self.monitoring_active:
            print(Fore.YELLOW + "Monitoring is not active.")
            return
        self.monitoring_active = False
        self.user_alarms.triggered_alarms.clear()
        print(Fore.RED + "Monitoring stopped (System is DISARMED).")
        self.event_logger("Monitoring disarmed")

    def show_live_overview(self):
        """
        This is the dedicated view for live data.
        Alarms are ONLY checked and shown here.
        """
        if not self.monitoring_active:
            print(Fore.YELLOW + "Monitoring is not active. Please start monitoring first (Option 1).")
            time.sleep(2)
            return

        print(Fore.CYAN + "Showing live overview... Press Ctrl+C to return to the menu.")
        self.event_logger("User opened live monitoring view")
        try:
            while True:
                
                # 1. Get current data
                cpu_percent, cpu_display = self.sensors.cpu_data()
                ram_percent, ram_display = self.sensors.ram_data()
                disk_percent, disk_display = self.sensors.disk_data()

                # 2. Display the live data
                display_string = f"\r {cpu_display} {ram_display} {disk_display} \r"
                print(display_string, end="", flush=True)
                time.sleep(1.5)

                self.user_alarms.check_alarms(cpu_percent, ram_percent, disk_percent)

        except KeyboardInterrupt:
            print("\nReturning to main menu.")
            self.event_logger("User closed live monitoring view")

    def show_main_menu(self):
        menu = True
        self.event_logger(log=("Main-menu opened"))
        while menu:
            self.user_alarms.show_alarms()
            print(Fore.LIGHTGREEN_EX + "\n***Main-menu***\n",
                  "1. Start Monitoring (Arm System)\n",
                  "2. Stop Monitoring (Disarm System)\n",
                  "3. Show Live Monitoring & Alarms\n", 
                  "4. Alarm Configuration\n",
                  "5. Exit")
            try:
                menu_choice = input(Fore.CYAN + "Please enter a choice from 1-5: ")

                if menu_choice == "1":
                    self.start_monitoring()
                elif menu_choice == "2":
                    self.stop_monitoring()
                elif menu_choice == "3":
                    self.show_live_overview() 
                elif menu_choice == "4":
                    self.user_alarms.show_config_alarm_menu()
                elif menu_choice == "5":
                    print("Shutting down...")
                    self.event_logger(log="User chose main-menu choice EXIT")
                    break
                else:
                    print(Fore.RED + "Please enter a valid menu choice number from 1-5.")
                    self.event_logger(log="User entered the wrong input on main-menu")
            except KeyboardInterrupt:
                    print("To exit press 5")
            
if __name__ == "__main__":
    run = Main()
    run.show_main_menu() #Startcommand, call for the menu method in the Main-class