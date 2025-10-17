#main

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
init(autoreset=True)

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE_PATH = BASE_DIR / "LOG-FILE.json"


class Main():
    def __init__ (self, name = None):
        self.name = name
        self.Sensors = Sensors()
        self.User_alarms = User_alarms(logger_func=self.event_logger)

    def event_logger(self, log):
        LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_log_entry = {
            "timestamp": timestamp,
            "message": log
        }
        try:
            with open(LOG_FILE_PATH, "r") as file:
                logs = json.load(file)
                if not isinstance(logs, list):
                    logs = [logs] 
        except (FileNotFoundError, json.JSONDecodeError):
            logs = []

        logs.append(new_log_entry)
        with open(LOG_FILE_PATH, "w") as file:
            json.dump(logs, file, indent=1)


    def show_main_menu(self):
        menu = True
        self.event_logger(log=("Main-menu opened"))
        while menu:
            print(Fore.LIGHTGREEN_EX + "***Main-menu***\n",
            "1. Start monitoring\n",
            "2. Stop monitoring\n",
            "3. Alarm configuration\n",
            "4. Monitor overview\n",
            "5. Exit")
            try:
                menu_choice = (input( Fore.CYAN + "Please enter a choice from 1-5: "))
            except ValueError:
                        print(Fore.RED + "Only numbers are allowed.")  
                        self.event_logger(log="User entered wrong value in main menu")      
            if menu_choice == "1":
                self.Sensors.ask_start_monitoring()
                self.event_logger(log="User choosed main-menu choice 1")
            elif menu_choice == "2":
                self.Sensors.stop_monitoring()
                self.event_logger(log="User choosed main-menu choice 2")
            elif menu_choice == "3":
                self.User_alarms.show_config_alarm_menu()
                self.event_logger(log="User choosed main-menu choice 3")
            elif menu_choice == "4":
                self.Sensors.start_overview()
                self.event_logger(log="User choosed main-menu choice 4")
            elif menu_choice == "5":
                print ("Shutting down...")
                self.event_logger(log="User choosed main-menu choice EXIT")
                break
            else:
                print (Fore.RED + "Please enter a valid menu choice number from 1-5: ")
                self.event_logger(log="User entered the wrong input on main-menu")


test= Main()


if __name__ == "__main__":
    test.show_main_menu()
