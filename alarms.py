# Alarms
import os
import time
import pygame
import psutil
from colorama import Fore, init
init(autoreset=True)

from stored_alarms import load_alarms, add_alarm, remove_alarm_by_index, list_alarms_human

soundfile = "Alarm_sound.mp3"

# Arm state per kind
ON   = {"cpu": False, "ram": False, "disk": False}
OVER = {"cpu": False, "ram": False, "disk": False}

def alarm_menu():
    while True:
        print(Fore.WHITE + "--- ALARM CONFIGURATION ---\n",
              Fore.BLUE + "1. CPU USAGE\n",
              Fore.BLUE + "2. RAM USAGE\n",
              Fore.BLUE + "3. DISK USAGE\n",
              Fore.BLUE + "4. REMOVE ALARM\n",
              Fore.MAGENTA + "5. EXIT TO MAIN MENU")
        choice = input("Enter a value between 1-5: ").strip()
        if choice == "1":
            cpu_config()
        elif choice == "2":
            ram_config()
        elif choice == "3":
            disk_config()
        elif choice == "4":
            remove_alarm()
        elif choice == "5":
            print(Fore.CYAN + "Exiting to main menu...")
            psutil.cpu_percent(interval=None)
            return
        else:
            print(Fore.RED + "ERROR! Enter a valid number between 1-5.")

def init_sound():
    try:
        pygame.mixer.init()
    except Exception as e:
        print(Fore.RED + f"[WARN] pygame init fail: {e}")

def play_sound():
    try:
        if os.path.isfile(soundfile):
            pygame.mixer.music.load(soundfile)
            pygame.mixer.music.play()
        else:
            print(Fore.RED + f"[WARN] sound not found: {soundfile}")
    except Exception as e:
        print(Fore.RED + f"[WARN] sound play fail: {e}")

def ask_pct(label):
    while True:
        try:
            x = int(input(f"Set {label} threshold (1-100): "))
            if 1 <= x <= 100:
                return x
        except ValueError:
            pass
        print("Enter 1-100.")

def cpu_config():
    pct = ask_pct("CPU")
    add_alarm(load_alarms(), kind="cpu", threshold=pct, enabled=True)
    ON["cpu"] = True
    print(f"CPU threshold saved at {pct}%")

def ram_config():
    pct = ask_pct("RAM")
    add_alarm(load_alarms(), kind="ram", threshold=pct, enabled=True)
    ON["ram"] = True
    print(f"RAM threshold saved at {pct}%")

def disk_config():
    pct = ask_pct("DISK")
    add_alarm(load_alarms(), kind="disk", threshold=pct, enabled=True)
    ON["disk"] = True
    print(f"DISK threshold saved at {pct}%")

def list_active_alarms():
    alarms = load_alarms()
    lines  = list_alarms_human(alarms)
    if not lines:
        print("No configured alarms.")
    else:
        print("\nConfigured alarms:")
        for i, line in enumerate(lines, 1):
            print(f" {i}. {line}")
    return alarms, lines

def remove_alarm():
    alarms, lines = list_active_alarms()
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

# --- Monitoring helpers ---

def _value(kind: str) -> float:
    if kind == "cpu":  return psutil.cpu_percent(interval=None)
    if kind == "ram":  return psutil.virtual_memory().percent
    if kind == "disk": return psutil.disk_usage('/').percent
    return 0.0

def _best_threshold(kind: str, value: float) -> float | None:
    """Pick the highest threshold <= current value (avoids spamming lower alarms)."""
    cand = [a["threshold"] for a in load_alarms() if a["kind"] == kind]
    elig = [t for t in cand if value >= t]
    return max(elig) if elig else None

def check(kind: str):
    if not ON.get(kind, False):
        OVER[kind] = False
        return
    v = _value(kind)
    best = _best_threshold(kind, v)
    if best is None:
        OVER[kind] = False
        return
    if not OVER[kind]:
        OVER[kind] = True
        init_sound()
        play_sound()
        print(Fore.RED + f"*** WARNING, {kind.upper()} USAGE EXCEEDED {best:.0f}% ***  (now {v:.0f}%) \a")
    elif v < best:
        OVER[kind] = False

# --- Alarm watcher (used ONLY in menu option 6) ---
import threading
_ALARM_THREAD = None
_STOP_EVENT = threading.Event()

def _alarm_loop(poll_s=0.5):
    while not _STOP_EVENT.is_set():
        for k in ("cpu", "ram", "disk"):
            check(k)
        time.sleep(poll_s)

def start_alarm_watcher(poll_s=0.5):
    global _ALARM_THREAD
    if _ALARM_THREAD and _ALARM_THREAD.is_alive():
        return False
    _STOP_EVENT.clear()
    _ALARM_THREAD = threading.Thread(target=_alarm_loop, args=(poll_s,), daemon=True)
    _ALARM_THREAD.start()
    return True

def stop_alarm_watcher():
    global _ALARM_THREAD
    if not _ALARM_THREAD:
        return False
    _STOP_EVENT.set()
    _ALARM_THREAD.join(timeout=2)
    _ALARM_THREAD = None
    return True
