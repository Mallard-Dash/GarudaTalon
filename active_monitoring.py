#Active monitoring

#Start monitoring
import time
import psutil
import subprocess
import threading

cpu = psutil.cpu_percent(interval=1)


def display_usage(cpu_usage, mem_usage, bars=100):
    cpu_percent = (cpu_usage / 100.0)
    cpu_bar = '#' *int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
    mem_percent = (mem_usage / 100.0)
    mem_bar = '#' *int(mem_percent * bars) + '-' * (bars - int(mem_percent * bars))


    print(f"\rCPU usage: |{cpu_bar}|{cpu_usage:.2f}%   ", end ="")     
    print(f"MEM usage: |{mem_bar}|{mem_percent:.2f}%   ", end ="\r")


def display_usage2():
    disk = psutil.disk_usage('/')
    ram  = psutil.virtual_memory()
    cpu  = psutil.cpu_percent(interval=0.5)

    total_disk_gb = disk.total / (1024**3)
    used_disk_gb  = disk.used / (1024**3)

    total_ram_gb = ram.total / (1024**3)
    used_ram_gb  = (ram.total - ram.available) / (1024**3)

    print(f"Diskanvändning: {disk.percent}%  ({used_disk_gb:.0f}/{total_disk_gb:.0f} GB used)")
    print(f"RAM-användning:  {ram.percent}%  ({used_ram_gb:.0f}/{total_ram_gb:.0f} GB used)")
    print(f"CPU-användning:  {cpu:.0f}%  ")

def display_usage3():
    disk = psutil.disk_usage('/')
    ram  = psutil.virtual_memory()
    cpu  = psutil.cpu_percent(interval=0.5)

    total_disk_gb = disk.total / (1024**3)
    used_disk_gb  = disk.used / (1024**3)

    total_ram_gb = ram.total / (1024**3)
    used_ram_gb  = (ram.total - ram.available) / (1024**3)


def monitor_func():
        # skriv ut 3 tomma rader först
    print("\n\n\n")
try:
    while True:
            # flytta markören upp 3 rader
            print("\033[F\033[F\033[F", end="")
            display_usage2()
            time.sleep(0.2)
except KeyboardInterrupt:
            print("\n--- Avslutar till huvudmeny ---")
            import main