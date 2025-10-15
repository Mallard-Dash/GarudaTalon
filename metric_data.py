#metric_data

import psutil

class Sensors():
    def __init__(self, monitoring = False, name = None, current_value = 0, max_value = 0, percent = 0):
        self.name = name
        self.current_value = current_value
        self.max_value = max_value
        self.percent = percent
        self.monitoring = monitoring

    def cpu_data(self):
        cpu = psutil.cpu_percent(1)
        self.current_value = int(cpu)
        return f"{self.name} currently at {cpu:.1f}% |"

    def ram_data(self):
        ram_current = psutil.virtual_memory().active / (1024**3)
        ram_total = psutil.virtual_memory().total / (1024**3)
        ram_percent = psutil.virtual_memory().percent
        self.current_value = int(ram_current)
        self.max_value = int(ram_total)
        self.percent = int(ram_percent)
        return f"{self.name} currently at {self.percent:.1f}% ({self.current_value:.1f}GB of {self.max_value:.1f}GB) |"


    def disk_data(self):
        disk_current = psutil.disk_usage("/").used / (1024**3)
        disk_total = psutil.disk_usage("/").total / (1024**3)
        disk_percent = psutil.disk_usage("/").percent
        self.current_value = int(disk_current)
        self.max_value = int(disk_total)
        self.percent = float(disk_percent)
        return f"{self.name} currently at {self.percent:.1f}% ({self.current_value:.1f}GB of {self.max_value:.1f}GB) |"

    def ask_start_monitoring(self):
        if self.monitoring == False:
            print ("Monitoring started...")
            self.monitoring = True
        elif self.monitoring == True:
            print (f"Monitoring already running...")
            self.monitoring = True

    def stop_monitoring(self):
        if self.monitoring == True:
            print("Monitoring stopped...")
            self.monitoring = False
        elif self.monitoring == False:
            print (f"Monitoring not running...")
            self.monitoring = False

    def start_overview(self):
        if self.monitoring == True:
            live_view = True
            while live_view:
                    cpu = Sensors(name="CPU")
                    ram = Sensors(name="RAM")
                    disk = Sensors(name="DISK")
                    try:
                        print(f"\r {cpu.cpu_data()}", end=""
                        f"{ram.ram_data()}"
                        f"{disk.disk_data()}"
                        f" Press ctrl + C to return...\r", flush= True)
                        time.sleep(0.5)
                    except KeyboardInterrupt:
                        live_view = False
        elif self.monitoring == False:
            print("Monitoring is not active...")

