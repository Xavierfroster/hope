import threading
import time
import datetime
from .core import speak

# Store tasks as (time, message, type)
scheduled_tasks = []

def add_task(delay_seconds, message):
    target_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
    scheduled_tasks.append({
        "time": target_time,
        "message": message,
        "type": "reminder"
    })
    return target_time

def add_alarm(hour, minute):
    now = datetime.datetime.now()
    target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target_time < now:
        target_time += datetime.timedelta(days=1)
    
    scheduled_tasks.append({
        "time": target_time,
        "message": "ALARM! Time's up!",
        "type": "alarm"
    })
    return target_time

def scheduler_loop():
    while True:
        now = datetime.datetime.now()
        for task in scheduled_tasks[:]:
            if now >= task["time"]:
                print(f"\n[SCHEDULER]: {task['message']}")
                speak(f"Excuse me, I have a {task['type']} for you: {task['message']}")
                scheduled_tasks.remove(task)
        time.sleep(10) # Check every 10 seconds

def start_scheduler():
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
