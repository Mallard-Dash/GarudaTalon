# metric_data.py

import psutil
import os

class Sensors():
    """
    A simple class responsible for fetching system metric data.
    It doesn't store any state (like whether monitoring is active).
    Its only job is to provide current data when asked.
    """

    def cpu_data(self):
        """
        Gets the current CPU usage.
        Returns:
            - float: The raw percentage (e.g., 15.4) for alarm checking.
            - str: A formatted string for display.
        """
        # Using interval=None makes the call non-blocking
        cpu_percent = psutil.cpu_percent(interval=None)
        display_str = f"CPU at {cpu_percent:.1f}% |"
        return cpu_percent, display_str

    def ram_data(self):
        """
        Gets the current RAM usage.
        Returns:
            - float: The raw percentage (e.g., 45.1) for alarm checking.
            - str: A formatted string for display.
        """
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        display_str = f"RAM at {ram_percent:.1f}% ({mem.active / (1024**3):.1f}GB of {mem.total / (1024**3):.1f}GB) |"
        return ram_percent, display_str

    def disk_data(self):
        path = "C:\\" if os.name == 'nt' else "/"
        """
        Gets the current Disk usage for the root directory.
        Returns:
            - float: The raw percentage (e.g., 72.8) for alarm checking.
            - str: A formatted string for display.
        """
        try:
            disk = psutil.disk_usage(path)
        except FileNotFoundError:
            print(f"ERROR! Disk path '{path}' not found!")
            return 0.0, f"DISK ({path}) NOT FOUND |"

        disk = psutil.disk_usage("/")
        disk_percent = disk.percent
        display_str = f"DISK {path} at {disk_percent:.1f}% ({disk.used / (1024**3):.1f}GB of {disk.total / (1024**3):.1f}GB) |"
        return disk_percent, display_str