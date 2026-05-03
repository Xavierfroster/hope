import psutil
import time
from hope import config

def get_pc_stats():
    # CPU and RAM
    cpu_usage = psutil.cpu_percent(interval=None)
    ram_stats = psutil.virtual_memory()
    ram_usage = ram_stats.percent
    
    # Battery
    battery = psutil.sensors_battery()
    battery_percent = battery.percent if battery else "Unknown"
    is_plugged = battery.power_plugged if battery else False
    
    # Disk Usage (Main Drive)
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    disk_free = disk.free / (1024**3) # Convert to GB
    
    # Network Speed (Sample over 0.5s)
    net_1 = psutil.net_io_counters()
    time.sleep(0.5)
    net_2 = psutil.net_io_counters()
    
    download_speed = (net_2.bytes_recv - net_1.bytes_recv) * 2 / 1024 # KB/s
    upload_speed = (net_2.bytes_sent - net_1.bytes_sent) * 2 / 1024 # KB/s
    
    return {
        "cpu": cpu_usage,
        "ram": ram_usage,
        "battery": battery_percent,
        "plugged": is_plugged,
        "disk": disk_usage,
        "disk_free": round(disk_free, 2),
        "download": round(download_speed, 2),
        "upload": round(upload_speed, 2)
    }

def get_diagnostics_report():
    stats = get_pc_stats()
    
    # Critical threshold checks using central config
    if stats["cpu"] > config.CPU_THRESHOLD or stats["ram"] > config.RAM_THRESHOLD:
        return f"Sir, the core is at its limit. CPU is at {stats['cpu']}% and RAM is at {stats['ram']}%."
    
    if stats["disk"] > config.DISK_THRESHOLD:
        return f"Sir, your disk is almost full ({stats['disk']}%). I can't breathe in here."

    if isinstance(stats["battery"], int) and stats["battery"] < config.BATTERY_LOW_THRESHOLD and not stats["plugged"]:
        return "Sir, I think I need some rest. I am going to sleep. Battery is below 20%."
        
    report = (f"CPU: {stats['cpu']}% | RAM: {stats['ram']}% | Disk: {stats['disk']}% ({stats['disk_free']} GB free). "
              f"Network: DL {stats['download']} KB/s, UL {stats['upload']} KB/s. ")
    
    if stats["battery"] != "Unknown":
        report += f"Battery: {stats['battery']}%."
        
    return report
