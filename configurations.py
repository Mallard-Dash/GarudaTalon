#configurations

import psutil
import sys
import os
import colorama
import time
import json
from pathlib import Path
import main

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "DATA"
os.makedirs(BASE_DIR, exist_ok=True)
FILE_PATH = BASE_DIR /"active_alarms.json"



class User_alarms():
    def __init__ (self, name = None, current_value = 0):
        self.name = name
        self.current_value = current_value

    cpu_value = App.self.cpu_data()
    ram_value = App.self.ram_percent()
    disk_value = App.self.disk_percent()

    def show_config_alarm_menu(self):
        while True:
            print("***Alarm-configuration***\n",
            "1. Add new alarm\n",
            "2. CPU\n",
            "3. RAM\n",
            "4. DISK\n",
            "5. Remove alarm\n"
            "6. Return\n")
            try:
                menu_choice = input("Please choose an option from 1-4: ")
            except ValueError:
                print("Only numbers are allowed.")
            if menu_choice == "1":
                self.add_new_alarm()
            elif menu_choice == "2":
                self.show_alarms(data=None)
            elif menu_choice == "3":
                self.show_alarms(data=None)
            elif menu_choice == "4":
                self.show_alarms(data=None)
            elif menu_choice == "5":
                self.remove_alarms()
            elif menu_choice == "6":
                print("Going back...")
                time.sleep(2)
                return
            else:
                print("Please enter a valid choice from 1-4: ")

    def add_new_alarm(self):
        name = self.name
        path = FILE_PATH
        try:
            name = input("Choose where to put the new alarm (cpu/ram/disk): ")
        except ValueError:
            print("Please enter one of the following: cpu, disk, ram")
            if name == "cpu":
                name = "CPU"
            elif name == "ram":
                name = "RAM"
            elif name == "disk":
                name = "DISK"
            else:
                print("Please enter one of the following: cpu, disk, ram: ")
        try:
            set_threshold = int(input("Set a threshold value (1-100)%: "))
        except ValueError:
            print("Please enter a number from 1-100: ")

        try:
            with open(path, "w") as file:
                data = {"Name": name, "Threshold": set_threshold+"%"}
                json.dump(data, file, indent=2)
                print("Alarm activated...")
                return set_threshold
        except FileNotFoundError:
            print("Error! File not found!")

    def show_alarms(self, data):
        path = FILE_PATH
        try:
            with open(path, "r") as file:
                data = json.load(file)
                print("---Activated alarms---\n")
                print(data)
                return data
        except FileNotFoundError:
            print("Error! File not found!")


    def is_alarm_triggered(self):
        self.show_alarms()
        if self.current_value <= data["Threshold"]:
            return None
        elif self.current_value >= data["Threshold"]:
            return f"WARNING! {data["Name"]} has triggered the alarm set at {data["Threshold"]}%"

    def remove_alarms(self):
        data = self.show_alarms()
        if not data:
            print("No alarms to remove")
            return
        for i, item in enumerate(data, start=1):
            print(i, item["Name"], item["Threshold"]+ "%")

        try:
            choice = int(input("What alarm would you like to remove?"))
        except ValueError:
                print("Only numbers please.")
        for index in enumerate(data, start=1):
                pop.data(index)

        self.save_json(data)
        print("Alarm removed...")

    def save_json(self, data, path):
        path = FILE_PATH
        path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=str(path.parent)) as tmp:
            json.dump(data, tmp, ensure_ascii=False, indent=2)
            tmp_name = tmp.name
        os.replace(tmp_name, path)

    def load_previous_alarms():
        data = self.show_alarms()



        
        



