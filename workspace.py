# GarudaTalon
from colorama import Fore, Style, init
import json
import os
import psutil
from typing import List, Dict, Any
import datetime
init(autoreset=True)

APP_DIR = os.path.join(os.getcwd(), "data")
ALARM_FILE = os.path.join(APP_DIR, "alarms.json")
os.makedirs(APP_DIR, exist_ok=True)

import psutil, sys, time

# --------- Sensor ----------
class Sensor:
    active = False

    @classmethod
    def start(cls):
        cls.active = True

    @classmethod
    def stop(cls):
        cls.active = False

    @classmethod
    def show_status(cls):
        return "Monitor is running" if cls.active else "No active monitoring..."

    @staticmethod
    def snapshot():
        disk = psutil.disk_usage('/')
        ram  = psutil.virtual_memory()
        cpu  = psutil.cpu_percent(interval=None)
        return {
            "cpu":  cpu,                       # %
            "ram":  ram.percent,               # %
            "disk": disk.percent,              # %
            "ram_used_gb":  (ram.total - ram.available) / (1024**3),
            "ram_total_gb":  ram.total / (1024**3),
            "disk_used_gb": disk.used / (1024**3),
            "disk_total_gb": disk.total / (1024**3),
        }

    @classmethod
    def display_loop(cls, alarms, refresh=0.5):
        try:
            while cls.active:
                data = cls.snapshot()

                line = (
                    Fore.LIGHTGREEN_EX + Style.BRIGHT +
                    f"|CPU: {data['cpu']:5.1f}% | "
                    f"RAM: {data['ram']:5.1f}% ({data['ram_used_gb']:.0f}/{data['ram_total_gb']:.0f} GB) | "
                    f"DISK: {data['disk']:5.1f}% ({data['disk_used_gb']:.0f}/{data['disk_total_gb']:.0f} GB)|"
                )
                sys.stdout.write("\r" + line + " " * 6)
                sys.stdout.flush()

                alarms.check_and_print(data)
                time.sleep(refresh)
        except KeyboardInterrupt:
            pass
        finally:
            print()  

# --------- Alarms ----------
class Alarms:
    def __init__(self):
        self.cfg = {
            "cpu":  {"enabled": False, "threshold": 0, "triggered": False},
            "ram":  {"enabled": False, "threshold": 0, "triggered": False},
            "disk": {"enabled": False, "threshold": 0, "triggered": False},
        }

    def show_active_alarms(self):
        print(Fore.CYAN + f"CPU alarm set at {self.cfg['cpu']['threshold']}%.")
        print(Fore.CYAN + f"RAM alarm set at {self.cfg['ram']['threshold']}%.")
        print(Fore.CYAN + f"DISK alarm set at {self.cfg['disk']['threshold']}%.")

    def _timestamp_swe(self) -> str:
        now = datetime.datetime.now()
        return f"{now.day}/{now.month}/{now.year}_{now.strftime('%H:%M')}"

    def _logfile_path(self):
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        return os.path.join(APP_DIR, f"system-monitor-{ts}.log")

    LOG_FILE = _logfile_path(True)

    def log_event(*parts: str) -> None:
        os.makedirs(os.path.dirname(Alarms.LOG_FILE), exist_ok=True)
        clean_parts = [str(p).replace(" ", "_") for p in parts]
        line = f"{Alarms._timestamp_swe()}_{'_'.join(clean_parts)}"
        with open(Alarms.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def _load_json(self) -> List[Dict[str, Any]]:
        if not os.path.exists(ALARM_FILE):
            return []
        try:
            with open(ALARM_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    cleaned = []
                    for item in data:
                        if not isinstance(item, dict):
                            continue
                        kind = item.get("kind")
                        thr  = item.get("threshold")
                        en   = item.get("enabled", True)
                        if kind in {"cpu", "ram", "disk"} and isinstance(thr, (int, float)):
                            cleaned.append({"kind": kind, "threshold": float(thr), "enabled": bool(en)})
                        return cleaned
                return []
        except Exception:
                    return []

    def _ask_threshold(self, name):
        while True:
            raw = input(f"Set {name.upper()} threshold (1–100): ").strip()
            if raw.isdigit():
                value = int(raw)
                if 1 <= value <= 100:
                    return value
            print(Fore.RED + "Enter a valid integer 1–100.")

    # --- config ---
    def cpu_config(self, value):
        self.cfg["cpu"]["threshold"] = self._ask_threshold("cpu")
        self.cfg["cpu"]["enabled"] = True
        self.cfg["cpu"]["triggered"] = False
        thr = value
        en = self.cfg[True]
        print(Fore.CYAN + f"CPU alarm set at {self.cfg['cpu']['threshold']}%.")
        cpu_data = {"kind": "cpu", "threshold": thr, "enabled": en}
        json_str = json.dumps(cpu_data, indent=4)
        with open("sample.json", "w") as f:
            f.write(ALARM_FILE)




    def ram_config(self):
        self.cfg["ram"]["threshold"] = self._ask_threshold("ram")
        self.cfg["ram"]["enabled"] = True
        self.cfg["ram"]["triggered"] = False
        print(Fore.CYAN + f"RAM alarm set at {self.cfg['ram']['threshold']}%.")

    def disk_config(self):
        self.cfg["disk"]["threshold"] = self._ask_threshold("disk")
        self.cfg["disk"]["enabled"] = True
        self.cfg["disk"]["triggered"] = False
        print(Fore.CYAN + f"DISK alarm set at {self.cfg['disk']['threshold']}%.")

    def remove_alarm(self):
        print("Remove which alarm? [cpu/ram/disk/all]")
        target = input("> ").strip().lower()
        if target in self.cfg:
            self.cfg[target].update({"enabled": False, "triggered": False})
            print(Fore.YELLOW + f"{target.upper()} alarm removed.")
        elif target == "all":
            for k in self.cfg:
                self.cfg[k].update({"enabled": False, "triggered": False})
            print(Fore.YELLOW + "All alarms removed.")
        else:
            print(Fore.RED + "Unknown option.")

    # --- runtime check ---
    def check_and_print(self, data):
        # data: {"cpu": %, "ram": %, "disk": %}
        for key in ("cpu", "ram", "disk"):
            cfg = self.cfg[key]
            if not cfg["enabled"]:
                continue
            val = data[key]
            th  = cfg["threshold"]

            if val >= th and not cfg["triggered"]:
                cfg["triggered"] = True
                print("\n" + Fore.RED + Style.BRIGHT +
                      f"WARNING! {key.upper()} alarm triggered at {val:.1f}% (threshold {th}%).")
            elif val < th and cfg["triggered"]:
                cfg["triggered"] = False
                print("\n" + Fore.GREEN +
                      f"{key.upper()} back to normal ({val:.1f}% < {th}%).")

    # --- simple menu ---
    def menu(self):
        while True:
            print(
                Fore.WHITE + "--- ALARM CONFIGURATION ---\n" +
                Fore.BLUE  + "1. CPU\n" +
                Fore.BLUE  + "2. RAM\n" +
                Fore.BLUE  + "3. DISK\n" +
                Fore.BLUE  + "4. REMOVE\n" +
                Fore.MAGENTA + "5. BACK"
            )
            choice = input("Enter 1–5: ").strip()
            if   choice == "1":
                self.cpu_config()
            elif choice == "2":
                self.ram_config()
            elif choice == "3":
                self.disk_config()
            elif choice == "4":
                self.remove_alarm()
            elif choice == "5":
                 return
            else:
                print(Fore.RED + "Invalid choice.")

# --------- Simple Main Menu ----------
def mainmenu():
    alarms = Alarms()
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
            if Sensor.active:
                print(Fore.YELLOW + "Already running.")
            else:
                print(Fore.GREEN + "Monitoring started...")
                Sensor.start()
                Sensor.display_loop(alarms, refresh=0.5)

        elif choice == "2":
            Sensor.stop()
            print(Fore.RED + "Monitoring stopped...")

        elif choice == "3":
            print(Sensor.show_status())

        elif choice == "4":
            alarms.menu()

        elif choice == "5":
            alarms._load_json()

        elif choice == "6":
            Sensor.display_loop()

        elif choice == "7":
            Sensor.stop()
            print(Fore.BLUE + "Bye!")
            break

        else:
            print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    mainmenu()
