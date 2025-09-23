#Alarms
import monitor
import psutil
ALARM_THRESHOLDS = {"cpu": None, "ram": None, "disk": None}


def alarm_menu():
    while True:
        print("---ALARM-CONFIGURATION---\n",
              "1.---CPU-USAGE---\n",
              "2.---RAM-USAGE---\n",
              "3.---DISK-USAGE---\n",
              "4.---EXIT-TO-MAIN-MENU---")
        alarm_menu_choice = int(input("Enter a value between 1-4: \n"))

        if alarm_menu_choice == 1:
            cpu_config()
        elif alarm_menu_choice == 2:
            ram_config()
        elif alarm_menu_choice == 3:
            disk_config()
        elif alarm_menu_choice == 4:
            print("Exiting to main menu...")
            return
        else:
            print("ERROR! Enter a valid number between 1-4: ")

def ask_threshold(label, current_percent):
    while True:
        s = input(f"Enter {label}-threshold (1–100). Current {label}: {current_percent:.0f}%: ").strip()
        try:
            choice = int(s)
            if 1 <= choice <= 100:
                return choice
        except ValueError:
            pass
        print("ERROR! Enter a value between 1-100.")

def cpu_config():
    current = psutil.cpu_percent(interval=0.5)
    choice = ask_threshold("CPU", current)
    ALARM_THRESHOLDS["cpu"] = choice
    print(f"CPU-alarm set to {choice}%")

def ram_config():
    vm  = psutil.virtual_memory()
    choice = ask_threshold("RAM", vm.percent)
    ALARM_THRESHOLDS["ram"] = choice
    print(f"RAM-alarm set to {choice}%")


def disk_config():
    disk = psutil.disk_usage('/')
    choice = ask_threshold("DISK", disk.percent)
    ALARM_THRESHOLDS["disk"] = choice
    print(f"DISK-alarm set to {choice}%")



