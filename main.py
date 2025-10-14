import psutil
from colorama import Fore, init
import sys
import os
import time

class App():
    def __init__ (self, monitoring = False, name = None, current_value = 0, max_value = 0, percent = 0):
        self.name = name
        self.current_value = current_value
        self.max_value = max_value
        self.percent = percent
        self.monitoring = monitoring


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
                    try:
                        bars = 50
                        cpu = self.cpu_data()
                        ram_percent, ram_current, ram_total = self.ram_data()
                        disk_percent, disk_current, disk_total = self.disk_data()
                            #cpu_bar = ' ' * (cpu * bars) + '-' * (bars - cpu * bars)
                            #ram_bar = ' ' * (ram_percent * bars) + '-' * (bars - ram_percent * bars)
                            #disk_bar = ' ' * disk_percent * bars + '-' * (bars - disk_percent * bars)

                        print(f"\rCPU usage: |{cpu_bar}|{cpu:.2f}% ", end= "")
                        print(f"RAM usage: |{ram_bar}|{ram_percent:.2f}% ({ram_current:.2f}GB of {ram_total:.2f}GB)", end= "")
                        print(f"DISK usage: |{disk_bar}|{disk_percent:.2f}% ({disk_current:.2f}GB of {disk_total:.2f}GB)\r")
                        time.sleep(0.5)
                    except KeyboardInterrupt:
                        live_view = False
        elif self.monitoring == False:
            print("Monitoring is not active...")

        

    def cpu_data(self):
        cpu = psutil.cpu_percent(1)
        self.current_value = int(cpu)
        return f"{self.name} currently at {cpu:.1f}%"

    def ram_data(self):
        ram_current = psutil.virtual_memory().active / (1024**3)
        ram_total = psutil.virtual_memory().total / (1024**3)
        ram_percent = psutil.virtual_memory().percent
        self.current_value = int(ram_current)
        self.max_value = int(ram_total)
        self.percent = int(ram_percent)
        return f"{self.name} currently at {self.percent:.1f}% ({self.current_value:.1f}GB of {self.max_value:.1f}GB)", self.percent, self.max_value, self.current_value


    def disk_data(self):
        disk_current = psutil.disk_usage("/").used / (1024**3)
        disk_total = psutil.disk_usage("/").total / (1024**3)
        disk_percent = psutil.disk_usage("/").percent
        self.current_value = int(disk_current)
        self.max_value = int(disk_total)
        self.percent = float(disk_percent)
        return f"{self.name} currently at {self.percent:.1f}% ({self.current_value:.1f}GB of {self.max_value:.1f}GB)", self.percent, self.max_value, self.current_value


    def show_main_menu(self):
        menu = True
        while menu:
            print("***Main-menu***\n",
            "1. Start monitoring\n",
            "2. Stop monitoring\n",
            "3. Show active alarms\n",
            "4. Monitor overview\n",
            "5. Exit")
            try:
                menu_choice = int(input("Please enter a choice from 1-5: "))
                if menu_choice == 1:
                    self.ask_start_monitoring()
                elif menu_choice == 2:
                    self.stop_monitoring()
                elif menu_choice == 3:
                    pass
                elif menu_choice == 4:
                    self.start_overview()
                elif menu_choice == 5:
                    print ("Shutting down...")
                    break
                else:
                    print ("Please enter a valid menu choice number from 1-5: ")
            except ValueError:
                    print("Only numbers are allowed.")        

    def show_alarm_menu():
        while True:
            print("***Alarm-menu***\n",
            "1. CPU-alarm\n",
            "2. RAM-alarm\n",
            "3. DISK-alarm\n",
            "4. Remove-alarm\n"
            "5. Return")
            try:
                menu_choice = input("Please enter a choice from 1-5: ")
            except ValueError:
                print("Only numbers are allowed. ")
                match(menu_choice):
                    case ("1"):
                        pass
                    case ("2"):
                        pass
                    case ("3"):
                        pass
                    case ("4"):
                        pass
                    case ("5"):
                        pass

cpu = App(name="CPU")
ram = App(name="RAM")
disk = App(name="DISK")
test= App()
print(cpu.cpu_data())
print(ram.ram_data())
print(disk.disk_data())
test.show_main_menu()