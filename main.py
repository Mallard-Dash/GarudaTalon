# GarudaTalon V1.0 Copyright Mallard-Dash 2025
# Main-file

import os
import json
import datetime
import time
from colorama import Fore, init
init(autoreset=True)

import monitor
import alarms
from stored_alarms import load_alarms, list_alarms_human

# --- App dirs & log ---
APP_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(APP_DIR, exist_ok=True)

def _logfile_path():
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return os.path.join(APP_DIR, f"system-monitor-{ts}.log")

LOG_FILE = _logfile_path()

def _timestamp_swe() -> str:
    now = datetime.datetime.now()
    return f"{now.day}/{now.month}/{now.year}_{now.strftime('%H:%M')}"

def log_event(*parts: str) -> None:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    clean_parts = [str(p).replace(" ", "_") for p in parts]
    line = f"{_timestamp_swe()}_{'_'.join(clean_parts)}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

log_event("Program_started")

loaded = load_alarms()
if loaded:
    print("Loading previously configured alarms...")
    time.sleep(1)
    for line in list_alarms_human(loaded):
        print(" -", line)
    log_event("Previously_configured_alarms_loaded", f"{len(loaded)}_alarms")
else:
    print(Fore.YELLOW + "No previously configured alarms found.")
    log_event("No_previously_configured_alarms")

def logbook(entry: str) -> None:
    path = os.path.join(APP_DIR, "Logbook.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        else:
            data = []
    except Exception:
        data = []
    data.append({"ts": _timestamp_swe(), "entry": entry})
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def mainmenu():
    while True:
        print(Fore.WHITE + "*** Main Menu ***\n",
              Fore.BLUE + "1. START MONITORING\n",
              Fore.BLUE + "2. STOP MONITORING\n",
              Fore.BLUE + "3. LIST ACTIVE MONITORING\n",
              Fore.BLUE + "4. CONFIGURE ALARMS\n",
              Fore.BLUE + "5. SHOW ALARMS\n",
              Fore.BLUE + "6. START MONITORING MODE\n",
              Fore.MAGENTA + "7. EXIT PROGRAM\n")
        choice = input("Enter a number between 1-7: ").strip()

        if choice == "1":
            log_event("Monitoring_started")
            ok = monitor.start_monitoring()
            if ok:
                print(Fore.GREEN + "Monitoring started.")
            else:
                print(Fore.YELLOW + "Monitoring is already running.")
        elif choice == "2":
            log_event("Monitoring_stopped")
            ok = monitor.stop_monitoring()
            if ok:
                print(Fore.CYAN + "Monitoring stopped.")
            else:
                print(Fore.YELLOW + "Monitoring is not active.")
        elif choice == "3":
            log_event("List_active_monitoring")
            monitor.show_active_monitoring()
            input("\nPress Enter to return to the main menu...")
        elif choice == "4":
            log_event("Alarm_menu_opened")
            alarms.alarm_menu()
        elif choice == "5":
            log_event("Show_alarms")
            alarms_loaded = load_alarms()
            if alarms_loaded:
                print("\nConfigured alarms:")
                for line in list_alarms_human(alarms_loaded):
                    print(" -", line)
            else:
                print("No configured alarms.")
            input("\nPress Enter to return to the main menu...")
        elif choice == "6":
            print("Press Ctrl+C to exit")
            log_event("Monitoring_mode_started")
            alarms.start_alarm_watcher(poll_s=0.5)  # alarms only during monitoring mode
            try:
                monitor.display_usage2(refresh=0.2)
            finally:
                alarms.stop_alarm_watcher()
                log_event("Monitoring_mode_stopped")
        elif choice == "7":
            log_event("Program_shutting_down")
            print(Fore.LIGHTMAGENTA_EX + "Shutting down... bye!")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Invalid choice! Enter a number between 1-7.")
            log_event("Invalid_choice", choice)

if __name__ == "__main__":
    mainmenu()
