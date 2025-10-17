#configurations

import psutil
import sys
import os
from colorama import Fore, init
import time
import json
from pathlib import Path
from metric_data import Sensors
init(autoreset=True)

BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "active_alarms.json"

class User_alarms():
    def __init__ (self, logger_func, name = None, current_value = 0):
        self.name = name
        self.current_value = current_value
        self.Sensors = Sensors()
        self.event_logger = logger_func


    def cpu_value(self):
        cpu = self.Sensors.cpu_data()
        return cpu

    def ram_data(self):
        ram = self.Sensors.ram_percent()
        return ram

    def disk_data(self):
        disk = self.Sensors.disk_percent()
        return disk

    def show_config_alarm_menu(self):
        self.event_logger(log="Alarm-menu opened")
        while True:
            print(Fore.LIGHTGREEN_EX + "\n***Alarm-configuration***\n",
            "1. Add new alarm\n",
            "2. Show active alarms\n", 
            "3. Remove alarm\n",      
            "4. Return\n")           
            try:
                menu_choice = int(input("Please choose an option from 1-4: "))
            except ValueError:
                print(Fore.RED + "Only numbers are allowed.")
                self.event_logger(log="User entered wrong value in alarm-menu")
                continue 

            if menu_choice == 1:
                self.add_new_alarm()
                self.event_logger(log="User choosed alarm-menu choice 1")
            elif menu_choice == 2:
                self.show_alarms()
                self.event_logger(log="User choosed alarm-menu choice 2")
            elif menu_choice == 3:
                self.remove_alarms()
                self.event_logger(log="User choosed alarm-menu choice 3")
            elif menu_choice == 4:
                print("Going back...")
                time.sleep(1)
                self.event_logger(log="User choosed to exit to main menu")
                return
            else:
                print(Fore.RED + "Please enter a valid choice from 1-4: ")
                self.event_logger(log="User entered wrong input choice in alarm-menu")


    def _load_alarms(self):

        try:
            with open(FILE_PATH, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_alarms(self, data):

        FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(FILE_PATH, "w") as file:

            json.dump(data, file, indent=2)


    def add_new_alarm(self):
        name_choice = ""
        while name_choice not in ["cpu", "ram", "disk"]:
            name_choice = input("Choose where to put the new alarm (cpu/ram/disk): ").lower()
            if name_choice not in ["cpu", "ram", "disk"]:
                print("Please enter one of the following: cpu, ram, disk")

        name = name_choice.upper()

        set_threshold = 0
        while set_threshold <= 0 or set_threshold > 100:
            try:
                set_threshold = int(input(f"Set a threshold value for {name} (1-100)%: "))
                if set_threshold <= 0 or set_threshold > 100:
                    print(Fore.RED + "Value must be between 1 and 100.")
            except ValueError:
                print(Fore.RED + "Please enter a number from 1-100.")


        all_alarms = self._load_alarms()


        new_alarm = {"Name": name, "Threshold": set_threshold}
        all_alarms.append(new_alarm)


        self._save_alarms(all_alarms)

        print(Fore.GREEN + f"Alarm for {name} at {set_threshold}% has been activated...")
        self.event_logger(log=f"User activated new alarm for {name} at {set_threshold}%")


    def show_alarms(self):
        print("\n---Activated alarms---")
        alarms = self._load_alarms()
        if not alarms:
            print(Fore.YELLOW + "No active alarms found.")
            return

        for alarm in alarms:
            print(f"- {alarm['Name']} is set to {alarm['Threshold']}%")


    def alarm_triggered(self, cpu, ram, disk):
        active_alarms = self._load_alarms()
        

        for alarm in active_alarms:
            value_to_check = 0
            if alarm["Name"] == "CPU":
                value_to_check = cpu
            elif alarm["Name"] == "RAM":
                value_to_check = ram
            elif alarm["Name"] == "DISK":
                value_to_check = disk

            if value_to_check >= alarm["Threshold"]:
                print(Fore.RED + f"WARNING! {alarm['Name']} ({value_to_check}%) has triggered the alarm set at {alarm['Threshold']}%")
                self.event_logger(log=f"Alarm triggered for {alarm['Name']} at {alarm['Threshold']}%")


    def remove_alarms(self):
        alarms = self._load_alarms()
        if not alarms:
            print(Fore.YELLOW + "No alarms to remove.")
            return

        print("Select an alarm to remove:")
        for i, item in enumerate(alarms, start=1):
            print(f"{i}. {item['Name']} (Threshold: {item['Threshold']}%)")

        try:
            choice = int(input(f"What alarm would you like to remove? (1-{len(alarms)}): "))
            if 1 <= choice <= len(alarms):
                removed_alarm = alarms.pop(choice - 1)
                
                self._save_alarms(alarms)
                print(Fore.GREEN + f"Alarm for {removed_alarm['Name']} has been removed...")
                return self.event_logger(log=f"Alarm triggered for {removed_alarm['Name']} at {removed_alarm['Threshold']}%")
            else:
                print(Fore.RED + "Invalid choice.")
                self.event_logger(log=f"User entered invalid choice in remove-alarms function")
        except ValueError:
            print(Fore.RED + "Only numbers please.")
            self.event_logger(log=f"User entered invalid value in remove-alarms function")
        
        



