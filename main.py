#GarudaTalon V1.0 Copyright Mallard-Dash 2025
#Main-file
import time
import psutil
import monitor
import alarms

def mainmenu(): #Main menu function with built in while-loop
    while True:
        print("***Main-Menu***\n",
        "1.---START-MONITORING---\n",
        "2.---STOP-MONITORING---\n",
        "3.---ACTIVE-MONITORING---\n",
        "4.---SET-ALARM---\n",
        "5.---ACTIVE-ALARMS\n",
        "6.---START-SURVEY-MODE---\n",
        "7.---EXIT-PROGRAM---\n")
        mm_choice = (input("Enter a number between 1-6: "))

        if mm_choice == "1":
                monitor.start_monitoring()
        elif mm_choice == "2":
               monitor.stop_monitoring()
        elif mm_choice == "3":
                monitor.show_active_monitoring()
        elif mm_choice == "4":
                alarms.alarm_menu()
        elif mm_choice == "5":
                print("ACTIVE-ALARMS")
        elif mm_choice == "6":
                print("START-SURVEY-MODE")
        elif mm_choice == "7":
                print("Shutting down...bye!")
                break
        else:
            print("Invalid choice! Enter a number between 1-6.")
        
mainmenu()