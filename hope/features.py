import os
import difflib
import re

# Core Imports
from hope.core import memory
from hope.core.engine import hope_speak, confirm_action, takecmd, personality_settings
from hope.configuration import settings as config
from hope.system_stats import monitor

# Service Imports
from hope.online import browser, knowledge
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
        hope_speak("Internet connection is online.")
    except OSError:
        hope_speak("Warning. No internet connection detected. Web features will be unavailable.")

def wishme():
    """Greets the user based on the time of day."""
    greeting = time_utils.get_greeting()
    full_message = f"{greeting}. I am a, Artificial Intellengence, You Can Call Me {config.ASSISTANT_NAME}, Created by Mr. {config.MASTER_NAME}. How May I Help You"
    hope_speak(full_message)

def execute_query(query):
    """Main orchestrator for processing user commands."""
    
    # 1. System Health Check
    stats = monitor.get_pc_stats()
    if stats["cpu"] > config.CPU_THRESHOLD or stats["ram"] > config.RAM_THRESHOLD:
        hope_speak(f"Sir, the core is at its limit. CPU is {stats['cpu']}% and RAM is {stats['ram']}%", query=query)
    if stats["disk"] > config.DISK_THRESHOLD:
        hope_speak(f"Sir, your disk is almost full. Only {stats['disk_free']} GB left.", query=query)

    # 2. Fuzzy Command Normalization
    core_commands = [
        "tell me about", "open youtube", "youtube search", "close", "minimise", 
        "open google", "play music", "the time", "open code", "volume up", 
        "volume down", "mute volume", "open camera", "enable vision",
        "switch to empathy mode", "switch to cynical mode", "humor level",
        "what was my last command", "wrap it up", "read my emails", "whatsapp message",
        "directions to", "where is"
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
        dest = query.replace("directions to", "").strip()
        browser.get_directions(dest)
        return

    # --- OFFLINE / SYSTEM ---
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

    # Fallback
    hope_speak("I don't know how to do that yet. Maybe you should teach me.", query=query)
