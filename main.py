# GarudaTalon V1.0 Copyright Mallard-Dash 2025
# main.py

import os
import json
import datetime
import time
from colorama import Fore, init
init(autoreset=True)

import monitor
from alarms import Alarms
from stored_alarms import load_alarms, list_alarms_human


class GarudaTalonApp:
    def __init__(self):
        self.APP_DIR = os.path.join(os.getcwd(), "data")
        os.makedirs(self.APP_DIR, exist_ok=True)
        self.LOG_FILE = self._new_logfile_path()


        self.alarms = Alarms(soundfile="alert.wav", poll_s=0.5)
        self.alarms.sync_enabled_flags_from_storage()

        self.log_event("Program_started")

        loaded = load_alarms()
        if loaded:
            print("Loading previously configured alarms...")
            time.sleep(1)
            for line in list_alarms_human(loaded):
                print(" -", line)
            self.log_event("Previously_configured_alarms_loaded", f"{len(loaded)}_alarms")
        else:
            print(Fore.YELLOW + "No previously configured alarms found.")
            self.log_event("No_previously_configured_alarms")

    # ---------- Logging ----------
    def _new_logfile_path(self) -> str:
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return os.path.join(self.APP_DIR, f"system-monitor-{ts}.log")

    @staticmethod
    def _timestamp_swe() -> str:
        now = datetime.datetime.now()
        return f"{now.day}/{now.month}/{now.year}_{now.strftime('%H:%M')}"

    def log_event(self, *parts: str) -> None:
        os.makedirs(os.path.dirname(self.LOG_FILE), exist_ok=True)
        clean_parts = [str(p).replace(" ", "_") for p in parts]
        line = f"{self._timestamp_swe()}_{'_'.join(clean_parts)}"
        with open(self.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def logbook(self, entry: str) -> None:
        path = os.path.join(self.APP_DIR, "Logbook.json")
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
        data.append({"ts": self._timestamp_swe(), "entry": entry})
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # ---------- Meny ----------
    def mainmenu(self):
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
                self.log_event("Monitoring_started")
                ok = monitor.start_monitoring()
                if ok:
                    print(Fore.GREEN + "Monitoring started.")
                else:
                    print(Fore.YELLOW + "Monitoring is already running.")

            elif choice == "2":
                self.log_event("Monitoring_stopped")
                ok = monitor.stop_monitoring()
                if ok:
                    print(Fore.CYAN + "Monitoring stopped.")
                else:
                    print(Fore.YELLOW + "Monitoring is not active.")

            elif choice == "3":
                self.log_event("List_active_monitoring")
                monitor.show_active_monitoring()
                input("\nPress Enter to return to the main menu...")

            elif choice == "4":
                self.log_event("Alarm_menu_opened")
                self.alarms.alarm_menu()  

            elif choice == "5":
                self.log_event("Show_alarms")
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
                self.log_event("Monitoring_mode_started")
                self.alarms.start_alarm_watcher()  # alarms under “monitoring mode”
                try:
                    monitor.display_usage2(refresh=0.2)
                finally:
                    self.alarms.stop_alarm_watcher()
                    self.log_event("Monitoring_mode_stopped")

            elif choice == "7":
                self.log_event("Program_shutting_down")
                print(Fore.LIGHTMAGENTA_EX + "Shutting down... bye!")
                time.sleep(1)
                break

            else:
                print(Fore.RED + "Invalid choice! Enter a number between 1-7.")
                self.log_event("Invalid_choice", choice)

    def run(self):
        try:
            self.mainmenu()
        finally:
            self.alarms.stop_alarm_watcher()


if __name__ == "__main__":
    GarudaTalonApp().run()
