# alarms.py
import os
import time
import threading
import pygame
import psutil
from colorama import Fore, init
init(autoreset=True)

from stored_alarms import load_alarms, add_alarm, remove_alarm_by_index, list_alarms_human


class Alarms:
    def __init__(self, soundfile: str = "alert.wav", poll_s: float = 0.5):
        self.soundfile = soundfile
        self.poll_s = poll_s
        self.on   = {"cpu": False, "ram": False, "disk": False}
        self.over = {"cpu": False, "ram": False, "disk": False}

        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

        self._mixer_ready = False

        psutil.cpu_percent(interval=None)

    # ----------------- Meny -----------------
    def alarm_menu(self):
        while True:
            print(
                Fore.WHITE + "--- ALARM CONFIGURATION ---\n",
                Fore.BLUE + "1. CPU USAGE\n",
                Fore.BLUE + "2. RAM USAGE\n",
                Fore.BLUE + "3. DISK USAGE\n",
                Fore.BLUE + "4. REMOVE ALARM\n",
                Fore.MAGENTA + "5. EXIT TO MAIN MENU"
            )
            choice = input("Enter a value between 1-5: ").strip()
            if choice == "1":
                self.cpu_config()
            elif choice == "2":
                self.ram_config()
            elif choice == "3":
                self.disk_config()
            elif choice == "4":
                self.remove_alarm()
            elif choice == "5":
                print(Fore.CYAN + "Exiting to main menu...")
                psutil.cpu_percent(interval=None)
                return
            else:
                print(Fore.RED + "ERROR! Enter a valid number between 1-5.")

    def _ensure_mixer(self):
        if self._mixer_ready:
            return
        try:
            pygame.mixer.init()
            self._mixer_ready = True
        except Exception as e:
            print(Fore.RED + f"[WARN] pygame init fail: {e}")

    def _play_sound(self):
        try:
            if not os.path.isfile(self.soundfile):
                print(Fore.RED + f"[WARN] sound not found: {self.soundfile}")
                return
            self._ensure_mixer()
            if not self._mixer_ready:
                return
            pygame.mixer.music.load(self.soundfile)
            pygame.mixer.music.play()
        except Exception as e:
            print(Fore.RED + f"[WARN] sound play fail: {e}")

    def _ask_pct(self, label: str) -> int:
        while True:
            try:
                x = int(input(f"Set {label} threshold (1-100): "))
                if 1 <= x <= 100:
                    return x
            except ValueError:
                pass
            print("Enter 1-100.")

    def cpu_config(self):
        pct = self._ask_pct("CPU")
        add_alarm(load_alarms(), kind="cpu", threshold=pct, enabled=True)
        self.on["cpu"] = True
        print(f"CPU threshold saved at {pct}%")

    def ram_config(self):
        pct = self._ask_pct("RAM")
        add_alarm(load_alarms(), kind="ram", threshold=pct, enabled=True)
        self.on["ram"] = True
        print(f"RAM threshold saved at {pct}%")

    def disk_config(self):
        pct = self._ask_pct("DISK")
        add_alarm(load_alarms(), kind="disk", threshold=pct, enabled=True)
        self.on["disk"] = True
        print(f"DISK threshold saved at {pct}%")

    def list_active_alarms(self):
        alarms = load_alarms()
        lines  = list_alarms_human(alarms)
        if not lines:
            print("No configured alarms.")
        else:
            print("\nConfigured alarms:")
            for i, line in enumerate(lines, 1):
                print(f" {i}. {line}")
        return alarms, lines

    def remove_alarm(self):
        alarms, lines = self.list_active_alarms()
        if not lines:
            return
        print(f"{len(lines)+1}. EXIT")
        while True:
            try:
                choice = int(input("Choose an alarm to remove: "))
                if 1 <= choice <= len(lines):
                    ok = remove_alarm_by_index(alarms, choice-1)
                    print("Alarm removed." if ok else "Failed to remove alarm.")
                    break
                elif choice == len(lines)+1:
                    print("Exit...")
                    break
            except ValueError:
                pass
            print(Fore.RED + "Invalid choice.")

    # ----------------- Monitoring -----------------
    def _value(self, kind: str) -> float:
        if kind == "cpu":
            return psutil.cpu_percent(interval=None)
        if kind == "ram":
            return psutil.virtual_memory().percent
        if kind == "disk":
            return psutil.disk_usage('/').percent
        return 0.0

    def _best_threshold(self, kind: str, value: float) -> float | None:
        """Välj högsta tröskeln ≤ aktuellt värde (hindrar spam från lägre nivåer)."""
        cand = [a["threshold"] for a in load_alarms() if a["kind"] == kind and a.get("enabled", True)]
        elig = [t for t in cand if value >= t]
        return max(elig) if elig else None

    def check(self, kind: str):
        if not self.on.get(kind, False):
            self.over[kind] = False
            return
        v = self._value(kind)
        best = self._best_threshold(kind, v)
        if best is None:
            self.over[kind] = False
            return
        if not self.over[kind] and v >= best:
            self.over[kind] = True
            self._play_sound()
            print(Fore.RED + f"*** WARNING, {kind.upper()} USAGE EXCEEDED {best:.0f}% ***  (now {v:.0f}%) \a")
        elif v < best:
            self.over[kind] = False

    # ----------------- Watcher-thread -----------------
    def _alarm_loop(self):
        while not self._stop_event.is_set():
            for k in ("cpu", "ram", "disk"):
                self.check(k)
            time.sleep(self.poll_s)

    def start_alarm_watcher(self) -> bool:
        if self._thread and self._thread.is_alive():
            return False
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._alarm_loop, daemon=True)
        self._thread.start()
        return True

    def stop_alarm_watcher(self) -> bool:
        if not self._thread:
            return False
        self._stop_event.set()
        self._thread.join(timeout=2)
        self._thread = None
        return True

    def sync_enabled_flags_from_storage(self):
        try:
            data = load_alarms()
            kinds_enabled = {a["kind"] for a in data if a.get("enabled", True)}
            for k in ("cpu", "ram", "disk"):
                self.on[k] = (k in kinds_enabled)
        except Exception:
            for k in ("cpu", "ram", "disk"):
                self.on[k] = False
