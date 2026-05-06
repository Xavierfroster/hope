import datetime

def get_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_greeting():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
         return "good morning"
    elif hour >= 12 and hour < 18:
         return "good afternoon"
    else:
        return "good evening"
