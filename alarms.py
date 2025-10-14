def show_config_alarm_menu():
    pass

def add_new_alarm():
    pass

def show_alarms():
    pass

def is_alarm_triggered():
    pass

def active_alarms():
    pass

def remove_alarms():
    pass

def load_previously_alarms():
    pass

def store_alarms():
    pass

import psutil
for part in psutil.disk_partitions():
    print(part.device, part.mountpoint, part.fstype)