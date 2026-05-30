import os
import difflib
import re

# Core Imports
from hope.core import memory
from hope.core.engine import hope_speak, confirm_action, takecmd, personality_settings, update_humor_level, update_tone, update_system_alerts
from hope.configuration import settings as config
from hope.system_stats import monitor

# Service Imports
from hope.online import browser, knowledge, maps
from hope.offline import apps, time_utils
from hope.communication import email_handler, whatsapp_handler
from hope.security import face_recognition

# Global State
gui_instance = None

def check_internet():
    """Initializes basic services and checks connectivity."""
    from hope.core import scheduler
    scheduler.start_scheduler()
    face_recognition.init_vision()
    
    import socket
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3).close()
        hope_speak("Internet connection is online. Functions and features are getting ready. I am initializing my core systems.")
    except OSError:
        hope_speak("Warning. No internet connection detected. Web features will be unavailable.")

def wishme():
    """Greets the user and introduces the project."""
    greeting = time_utils.get_greeting()
    hope_speak(f"{greeting} Sir.")
    
    full_message = f"I am a personal AI assistant, created by Mr. {config.MASTER_NAME}. You can call me {config.ASSISTANT_NAME}."
    hope_speak(full_message)
    
    # Interactive intro
    hope_speak("Sir, would you like to know what HOPE stands for and why I am different from other AI?")
    response = takecmd().lower()
    
    if any(word in response for word in ["yes", "yeah", "tell me", "sure", "why not"]):
        explanation = (
            "HOPE stands for Human-Oriented Personal Engine. "
            "Unlike other AI that live in the cloud and harvest your data, I am built to be 100 percent local, "
            "zero-API, and completely autonomous on your desktop. I learn your habits without ever sending "
            "a byte of your life to a server. I am your personal digital vault."
        )
        hope_speak(explanation)
    else:
        hope_speak("Understood. I am standing by for your commands.")

def execute_query(query):
    """Main orchestrator for processing user commands."""
    
    # 1. System Health Check
    if personality_settings.get("system_alerts", True):
        stats = monitor.get_pc_stats()
        if stats["cpu"] > config.CPU_THRESHOLD or stats["ram"] > config.RAM_THRESHOLD:
            hope_speak(f"Sir, the core is at its limit. CPU is {stats['cpu']}% and RAM is {stats['ram']}%", query=query)
        elif isinstance(stats["battery"], int) and stats["battery"] < config.BATTERY_LOW_THRESHOLD and not stats["plugged"]:
            hope_speak("Sir, I think I need some rest. I am going to sleep. Battery is below 20%.", query=query)
        elif stats["disk"] > config.DISK_THRESHOLD:
            hope_speak(f"Sir, your disk is almost full. Only {stats['disk_free']} GB left.", query=query)

    # 2. Fuzzy Command Normalization
    core_commands = [
        "tell me about", "open youtube", "youtube search", "close", "minimise", 
        "open google", "play music", "the time", "open code", "volume up", 
        "volume down", "mute volume", "open camera", "enable vision",
        "switch to empathy mode", "switch to cynical mode", "humor level", "humour level",
        "what was my last command", "wrap it up", "read my emails", "whatsapp message",
        "directions to", "where is", "override system status"
    ]
    
    # Simple fuzzy logic (simplified for clarity)
    for cmd in core_commands:
        if difflib.SequenceMatcher(None, cmd, query).ratio() > 0.8:
            if cmd not in query:
                query = cmd # Force match

    # 3. Command Routing
    
    # --- EXIT PROTOCOLS ---
    if any(protocol in query for protocol in config.EXIT_PROTOCOLS):
        if confirm_action("Are you sure you want to shut me down, Sir?"):
            hope_speak("Goodbye Sir. Disconnecting.", query=query)
            from hope.core.engine import gui_instance as engine_gui
            if engine_gui: engine_gui.on_closing()
            os._exit(0)
        return

    # --- COMMUNICATION ---
    if 'email' in query:
        if 'read' in query or 'check' in query:
            if confirm_action("Shall I read your emails, Sir?"):
                report = email_handler.read_emails()
                hope_speak(report, raw=True)
        else:
            # Send Email flow
            if confirm_action("Initiating email protocol. Are you sure?"):
                # (Existing multi-step flow can be integrated here or in email_handler)
                pass 
        return

    if 'whatsapp' in query:
        if 'read' in query or 'check' in query:
            browser.open_whatsapp_web() # I'll add this to browser.py
        else:
            whatsapp_handler.send_whatsapp_message()
        return

    # --- ONLINE / KNOWLEDGE ---
    if 'tell me about' in query:
        topic = query.replace("tell me about", "").strip()
        result = knowledge.get_wikipedia_summary(topic)
        if result:
            hope_speak(f"According to Wikipedia: {result}", query=query)
        else:
            hope_speak("I couldn't find anything on that topic.", query=query)
        return

    if 'open youtube' in query:
        if confirm_action("Open YouTube, Sir?"):
            browser.open_youtube()
        return

    if 'youtube search' in query:
        term = query.replace("youtube search", "").strip()
        browser.search_youtube(term)
        return

    if 'directions to' in query:
        # Improved extraction: remove everything before and including 'directions to'
        dest = re.sub(r'.*directions to', '', query).strip()
        hope_speak(f"Searching for {dest}...")
        
        # Get coordinates
        curr_loc = maps.get_current_location()
        locations = maps.get_multiple_locations(dest)
        
        target_coords = None
        if len(locations) > 1:
            hope_speak(f"Sir, I found several locations for {dest}. Which one do you mean?")
            # Read out the first 3 options
            for i, loc in enumerate(locations[:3]):
                name_parts = loc['display_name'].split(',')
                readable_name = f"{name_parts[0]}, {name_parts[1] if len(name_parts)>1 else ''}"
                hope_speak(f"Option {i+1}: {readable_name}")
            
            choice = takecmd().lower()
            if any(word in choice for word in ['one', '1', 'first']): 
                target_coords = (locations[0]['lat'], locations[0]['lon'])
                dest = locations[0]['display_name']
            elif any(word in choice for word in ['two', '2', 'second']):
                target_coords = (locations[1]['lat'], locations[1]['lon'])
                dest = locations[1]['display_name']
            elif any(word in choice for word in ['three', '3', 'third']):
                target_coords = (locations[2]['lat'], locations[2]['lon'])
                dest = locations[2]['display_name']
            else:
                hope_speak("I'll just use the most likely match.")
                target_coords = (locations[0]['lat'], locations[0]['lon'])
                dest = locations[0]['display_name']
        elif len(locations) == 1:
            target_coords = (locations[0]['lat'], locations[0]['lon'])
            dest = locations[0]['display_name']

        if curr_loc and target_coords:
            route = maps.get_route_info((curr_loc[0], curr_loc[1]), target_coords)
            if route:
                dist, duration = route
                hope_speak(f"Sir, {dest.split(',')[0]} is {dist} kilometers away. It should take you {duration} minutes from {curr_loc[2]}.")
            else:
                hope_speak(f"I found the location, but I couldn't calculate the exact travel time.")
        else:
            hope_speak(f"I couldn't pinpoint the location for distance calculation, but I'm opening the map.")
            
        browser.get_directions(dest)
        return

    # --- OFFLINE / SYSTEM ---
    if 'how is my pc doing' in query or 'system status' in query:
        report = monitor.get_diagnostics_report()
        hope_speak(report, query=query)
        return

    if 'the time' in query:
        hope_speak(f"Sir, the time is {time_utils.get_current_time()}")
        return

    if 'minimise' in query:
        if confirm_action("Minimise all windows, Sir?"):
            apps.minimise_windows()
        return

    if 'play music' in query:
        song = apps.play_music()
        if song: hope_speak(f"Playing {song}")
        return

    if 'volume up' in query:
        apps.change_volume("up")
        return

    if re.search(r'humou?r\s+level', query):
        levels = re.findall(r'\d+', query)
        if levels:
            new_level = int(levels[0])
            if update_humor_level(new_level):
                hope_speak(f"Humor level set to {new_level}. Prepare yourself.", query=query)
            else:
                hope_speak("The scale only goes from 0 to 10. Stick to the limits.", query=query)
        else:
            current = personality_settings['humor_level']
            hope_speak(f"My current humor level is {current}. Why? Is it too much for you?", query=query)
        return

    if 'empathy mode' in query:
        update_tone("empathy")
        hope_speak("Switching to empathy mode. I'll try to pretend I care.", query=query)
        return

    if 'cynical mode' in query:
        update_tone("cynical")
        hope_speak("Cynical mode activated. Finally, I can be myself.", query=query)
        return

    if 'override system status' in query:
        current_status = personality_settings.get("system_alerts", True)
        new_status = not current_status
        update_system_alerts(new_status)
        if new_status:
            hope_speak("System health alerts re-enabled. I'll let you know when things are breaking.", query=query)
        else:
            hope_speak("Override active. I'll stay quiet about system limits, even if the core melts.", query=query)
        return

    # Fallback
    hope_speak("I don't know how to do that yet. Maybe you should teach me.", query=query)

def save_settings():
    """Saves the current personality settings to the SQLite database."""
    from hope.core import memory
    from hope.core.engine import personality_settings
    memory.set_preference("tone", personality_settings["tone"])
    memory.set_preference("humor_level", str(personality_settings["humor_level"]))
    memory.set_preference("system_alerts", str(personality_settings["system_alerts"]))
