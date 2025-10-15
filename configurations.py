#configurations

import psutil
import sys
import os
import colorama
import time


class User_alarms():
    def __init__ (self, name = None, treshold = 0, alarm_triggered = False):
        self.name = name
        self.treshold = treshold
        alarm_triggered = alarm_triggered

    def show_config_alarm_menu(self):
        while True:
            print("***Alarm-configuration***\n",
            "1. Add new alarm\n",
            "2. CPU\n",
            "3. DISK\n",
            "4. Return\n")
            try:
                menu_choice = input("Please choose an option from 1-4: ")
            except ValueError:
                print("Only numbers are allowed.")
            if menu_choice == "1":
                self.show_alarms()
            elif menu_choice == "2":
                self.show_alarms()
            elif menu_choice == "3":
                self.show_alarms()
            elif menu_choice == "4":
                print("Going back...")
                time.sleep(2)
                return
            else:
                print("Please enter a valid choice from 1-4: ")

    def add_new_alarm(self):
        treshold = self.treshold
        set_treshold = input("Set a treshold value (1-100)%: ")
        self.treshold = set_treshold
        #kalla på json och lagra larmet där.

    def show_alarms(self):
        #Kalla på json-filen med sparade larm och visa alla sparade larm
        pass

    def is_alarm_triggered(self):
        #Ett boolean som returnerar True om ett alarm triggas, False om det är vilande eller inaktiverat
        pass

    def remove_alarms(self):
        #Kalla på show_alarms och visa vilka som är satta
        #Fråga användaren vilket alarm i listan man vill ta bort
        #Bygg en meny med siffror och en range-sats
        #Kalla på json-filen och ta bort det larmet användaren anger
        pass



