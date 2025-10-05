import threading
import psutil
import time
import sys
from colorama import Fore, init
init(autoreset=True)

_MONITOR_THREAD = None
_STOP_EVENT = threading.Event()
_LATEST = {}

def _collect_loop(interval=1.0, disk_path="/"):
    psutil.cpu_percent(interval=None)  # warm-up
    while not _STOP_EVENT.is_set():
        cpu = psutil.cpu_percent(interval=interval)
        vm  = psutil.virtual_memory()
        du  = psutil.disk_usage(disk_path)
        _LATEST.update({
            "cpu_percent": cpu,
            "ram_percent": vm.percent,
            "ram_used_gb": (vm.total - vm.available) / (1024**3),
            "ram_total_gb": vm.total / (1024**3),
            "disk_percent": du.percent,
            "disk_used_gb": du.used / (1024**3),
            "disk_total_gb": du.total / (1024**3),
        })

def start_monitoring(interval=1.0, disk_path="/"):
    global _MONITOR_THREAD
    if is_monitoring_active():
        return False
    _STOP_EVENT.clear()
    _MONITOR_THREAD = threading.Thread(
        target=_collect_loop, args=(interval, disk_path), daemon=True
    )
    _MONITOR_THREAD.start()
    return True

def stop_monitoring():
    global _MONITOR_THREAD
    if not is_monitoring_active():
        return False
    _STOP_EVENT.set()
    _MONITOR_THREAD.join(timeout=2)
    _MONITOR_THREAD = None
    return True

def is_monitoring_active():
    return _MONITOR_THREAD is not None and _MONITOR_THREAD.is_alive()

def get_status():
    if not is_monitoring_active():
        return None
    return dict(_LATEST)

def display_usage2(refresh=0.2):
    try:
        while True:
            disk = psutil.disk_usage('/')
            ram  = psutil.virtual_memory()
            cpu  = psutil.cpu_percent(interval=0.4)

            total_disk_gb = disk.total / (1024**3)
            used_disk_gb  = disk.used  / (1024**3)
            total_ram_gb  = ram.total  / (1024**3)
            used_ram_gb   = (ram.total - ram.available) / (1024**3)

            line = (f"CPU: {cpu:5.1f}% | RAM: {ram.percent:5.1f}% "
                    f"({used_ram_gb:.0f}/{total_ram_gb:.0f} GB) | "
                    f"DISK: {disk.percent:5.1f}% "
                    f"({used_disk_gb:.0f}/{total_disk_gb:.0f} GB)")
            sys.stdout.write("\r" + line + " " * 8)
            sys.stdout.flush()
            time.sleep(refresh)
    except KeyboardInterrupt:
        pass

def show_active_monitoring():
    st = get_status()
    if not st:
        print(Fore.YELLOW + "No active monitoring. Start it with option 1 or use Monitoring mode (6).")
        return
    print(Fore.CYAN + "--- ACTIVE MONITORING (snapshot) ---")
    print("CPU usage : {:5.1f}%".format(st["cpu_percent"]))
    print("Memory    : {:5.1f}% ({:.1f}/{:.1f} GB used)".format(
        st["ram_percent"], st["ram_used_gb"], st["ram_total_gb"]))
    print("Disk      : {:5.1f}% ({:.1f}/{:.1f} GB used)".format(
        st["disk_percent"], st["disk_used_gb"], st["disk_total_gb"]))
