#main

import psutil
from colorama import Fore, init
import sys
import os
import time
from configurations import User_alarms
from metric_data import Sensors


class Main():
    def __init__ (self, name = None):
        self.name = name
        self.User_alarms = User_alarms()
        self.Sensors = Sensors()

    def event_logger():
    #Kalla på en ny json-fil som loggar alla kommandon i programmet och lagrar detta som en logg här
        pass

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
                self.Sensors.ask_start_monitoring()
            elif menu_choice == "2":
                self.Sensors.stop_monitoring()
            elif menu_choice == "3":
                self.User_alarms.show_config_alarm_menu()
            elif menu_choice == "4":
                self.Sensors.start_overview()
            elif menu_choice == "5":
                print ("Shutting down...")
                break
            else:
                print ("Please enter a valid menu choice number from 1-5: ")


test= Main()


if __name__ == "__main__":
    test.show_main_menu()