#configurations

import psutil
import sys
import os
import colorama
import time
import json
from pathlib import Path
from metric_data import Sensors

BASE_DIR = Path(__name__).resolve().parent
FILE_PATH = BASE_DIR /"active_alarms.json"
os.makedirs(FILE_PATH, exist_ok=True)



class User_alarms():
    def __init__ (self, name = None, current_value = 0):
        self.name = name
        self.current_value = current_value
        self.Sensors = Sensors()

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
        while True:
            print("***Alarm-configuration***\n",
            "1. Add new alarm\n",
            "2. CPU\n",
            "3. RAM\n",
            "4. DISK\n",
            "5. Remove alarm\n"
            "6. Return\n")
            try:
                menu_choice = int(input("Please choose an option from 1-6: "))
            except ValueError:
                print("Only numbers are allowed.")
            if menu_choice == 1:
                self.add_new_alarm()
            elif menu_choice == 2:
                self.show_alarms(data=None)
            elif menu_choice == 3:
                self.show_alarms(data=None)
            elif menu_choice == 4:
                self.show_alarms(data=None)
            elif menu_choice == 5:
                self.remove_alarms()
            elif menu_choice == 6:
                print("Going back...")
                time.sleep(2)
                return
            else:
                print("Please enter a valid choice from 1-6: ")

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
            with open(path, "a") as file:
                data = {"Name": name, "Threshold": set_threshold}
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
            return None


    def alarm_triggered(self, cpu, ram, disk):
        data = self.show_alarms()
        if self.current_value <= data["Threshold"]:
            return None
        elif self.current_value >= data["Threshold"]:
            return f"WARNING! {data["Name"]} has triggered the alarm set at {data["Threshold"]}%"

    def remove_alarms(self, data):
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
                delete.data(index)

        self.save_json(data)
        print("Alarm removed...")

    def save_json(self, data, path):
        self.path = FILE_PATH
        self.path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=str(self.path.parent)) as tmp:
            json.dump(self.data, tmp, ensure_ascii=False, indent=2)
            tmp_name = tmp.name
        os.replace(tmp_name, path)

    def load_previous_alarms(self, data):
        self.data = self.show_alarms()



        
        



