#main

import psutil
from colorama import Fore, init
import sys
import os
import time
from configurations import User_alarms


class App():
    def __init__ (self, monitoring = False, name = None, current_value = 0, max_value = 0, percent = 0):
        self.name = name
        self.current_value = current_value
        self.max_value = max_value
        self.percent = percent
        self.monitoring = monitoring
        self.User_alarms = User_alarms()


    def ask_start_monitoring(self):
        if self.monitoring == False:
            print ("Monitoring started...")
            self.monitoring = True
        elif self.monitoring == True:
            print (f"Monitoring already running...")
            self.monitoring = True

    def stop_monitoring(self):
        if self.monitoring == True:
            print("Monitoring stopped...")
            self.monitoring = False
        elif self.monitoring == False:
            print (f"Monitoring not running...")
            self.monitoring = False

    def start_overview(self):
        if self.monitoring == True:
            live_view = True
            while live_view:
                    cpu = App(name="CPU")
                    ram = App(name="RAM")
                    disk = App(name="DISK")
                    try:
                        print(f"\r {cpu.cpu_data()}", end=""
                        f"{ram.ram_data()}"
                        f"{disk.disk_data()}"
                        f" Press ctrl + C to return...\r", flush= True)
                        time.sleep(0.5)
                    except KeyboardInterrupt:
                        live_view = False
        elif self.monitoring == False:
            print("Monitoring is not active...")

        

    def cpu_data(self):
        cpu = psutil.cpu_percent(1)
        self.current_value = int(cpu)
        return f"{self.name} currently at {cpu:.1f}% |"

    def ram_data(self):
        ram_current = psutil.virtual_memory().active / (1024**3)
        ram_total = psutil.virtual_memory().total / (1024**3)
        ram_percent = psutil.virtual_memory().percent
        self.current_value = int(ram_current)
        self.max_value = int(ram_total)
        self.percent = int(ram_percent)
        return f"{self.name} currently at {self.percent:.1f}% ({self.current_value:.1f}GB of {self.max_value:.1f}GB) |"


    def disk_data(self):
        disk_current = psutil.disk_usage("/").used / (1024**3)
        disk_total = psutil.disk_usage("/").total / (1024**3)
        disk_percent = psutil.disk_usage("/").percent
        self.current_value = int(disk_current)
        self.max_value = int(disk_total)
        self.percent = float(disk_percent)
        return f"{self.name} currently at {self.percent:.1f}% ({self.current_value:.1f}GB of {self.max_value:.1f}GB) |"


    def show_main_menu(self):
        menu = True
        while menu:
            print("***Main-menu***\n",
            "1. Start monitoring\n",
            "2. Stop monitoring\n",
            "3. Alarm configuration\n",
            "4. Monitor overview\n",
            "5. Exit")
            try:
                menu_choice = (input("Please enter a choice from 1-5: "))
            except ValueError:
                        print("Only numbers are allowed.")        
            if menu_choice == "1":
                self.ask_start_monitoring()
            elif menu_choice == "2":
                self.stop_monitoring()
            elif menu_choice == "3":
                self.User_alarms.show_config_alarm_menu()
            elif menu_choice == "4":
                self.start_overview()
            elif menu_choice == "5":
                print ("Shutting down...")
                break
            else:
                print ("Please enter a valid menu choice number from 1-5: ")

def main():
    test= App()

if __name__ == "__main__":
    test.show_main_menu()