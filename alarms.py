#Alarms
import psutil
import os
import pygame
import time
soundfile = "aughhhh-tiktok.mp3"
THR = {"cpu": None, "ram": None, "disk": None}  
ON  = {"cpu": False, "ram": False, "disk": False} 
OVER= {"cpu": False, "ram": False, "disk": False} 


def alarm_menu():
    while True:
        print("---ALARM-CONFIGURATION---\n",
              "1.---CPU-USAGE---\n",
              "2.---RAM-USAGE---\n",
              "3.---DISK-USAGE---\n",
              "4.---EXIT-TO-MAIN-MENU---")
        alarm_menu_choice = (input("Enter a value between 1-4: \n"))

        if alarm_menu_choice == "1":
            cpu_config()
        elif alarm_menu_choice == "2":
            ram_config()
        elif alarm_menu_choice == "3":
            disk_config()
        elif alarm_menu_choice == "4":
            print("Exiting to main menu...")
            psutil.cpu_percent(interval=None)
            monitor_loop()
            return
        else:
            print("ERROR! Enter a valid number between 1-4: ")


def init_sound():
    try:
        pygame.mixer.init()
    except Exception as e:
        print(f"[WARN] pygame init fail: {e}")

def play_sound():
    try:
        if os.path.isfile(soundfile):
            pygame.mixer.music.load(soundfile)
            pygame.mixer.music.play()
        else:
            print(f"[WARN] sound not found: {soundfile}")
    except Exception as e:
        print(f"[WARN] sound play fail: {e}")


def ask_pct(label):
    while True:
        try:
            x = int(input(f"Set {label} threshold (1–100): "))
            if 1 <= x <= 100: return x
        except ValueError:
            pass
        print("Enter 1–100.")

def cpu_config():
    pct = ask_pct("CPU") #pct is %
    set_threshold("cpu", pct)
    enable("cpu", True)

def ram_config():
    pct = ask_pct("RAM")
    set_threshold("ram", pct)
    enable("ram", True)

def disk_config():
    pct = ask_pct("DISK")
    set_threshold("disk", pct)
    enable("disk", True)

    
def set_threshold(type, pct):
    THR[type] = pct
    print(f"{type.upper()}-threshold = {pct}%")

def enable(type, state=True): #Arm the alarm
    ON[type] = state
    if not state: OVER[type] = False
    print(f"{type.upper()} {'ON' if state else 'OFF'}")
    monitor_loop()

def reset_alarm(type):
    OVER[type] = False
    print(f"{type.upper()} reset")

def choice(type):
    if type == "cpu":  return psutil.cpu_percent(interval=None)
    if type == "ram":  return psutil.virtual_memory().percent
    if type == "disk": return psutil.disk_usage('/').percent

def check(type):
    if not ON[type] or THR[type] is None: return
    v = choice(type)
    if not OVER[type] and v >= THR[type]:       
        OVER[type] = True
        init_sound()
        play_sound()
        print(f"WARNING! ALARM TRIGGERED! {type.upper()}: {v:.0f}%.  Threshold: {THR[type]}% \a")
    elif OVER[type] and v < THR[type]:          
        OVER[type] = False

def monitor_loop(poll_s=0.5):
    print("Monitoring... Press ctrl+C to abort.")
    try:
        while True:
            for k in ("cpu","ram","disk"):
                check(k)
            time.sleep(poll_s)
    except KeyboardInterrupt:
        print("\nStop monitoring.")