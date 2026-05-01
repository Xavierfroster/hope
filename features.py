import datetime
import smtplib
import pyautogui
import os
import webbrowser
import wikipedia
import socket
import json
import sys
import difflib
from core import speak, takecmd
import memory
import vision
import scheduler
import re

# --- Memory and Learning System ---
conversation_memory = []
learned_phrases = {}
learned_aliases = {}
LEARNING_DIR = "learning"
LEARNING_FILE = os.path.join(LEARNING_DIR, "learned_phrases.json")
ALIAS_FILE = os.path.join(LEARNING_DIR, "command_aliases.json")
SETTINGS_FILE = os.path.join(LEARNING_DIR, "settings.json")

# Default Personality Settings
personality_settings = {
    "tone": memory.get_preference("tone", "cynical"),
    "humor_level": int(memory.get_preference("humor_level", 5)),
    "custom_cynical_prefixes": json.loads(memory.get_preference("custom_cynical_prefixes", "[]")),
    "custom_cynical_suffixes": json.loads(memory.get_preference("custom_cynical_suffixes", "[]")),
    "custom_empathy_prefixes": json.loads(memory.get_preference("custom_empathy_prefixes", "[]")),
    "custom_empathy_suffixes": json.loads(memory.get_preference("custom_empathy_suffixes", "[]"))
}

if not os.path.exists(LEARNING_DIR):
    os.makedirs(LEARNING_DIR)

if os.path.exists(LEARNING_FILE):
    try:
        with open(LEARNING_FILE, "r") as f:
            learned_phrases = json.load(f)
    except Exception:
        pass

if os.path.exists(ALIAS_FILE):
    try:
        with open(ALIAS_FILE, "r") as f:
            learned_aliases = json.load(f)
    except Exception:
        pass

def save_phrases():
    with open(LEARNING_FILE, "w") as f:
        json.dump(learned_phrases, f)

def save_aliases():
    with open(ALIAS_FILE, "w") as f:
        json.dump(learned_aliases, f)

def save_settings():
    for key, value in personality_settings.items():
        if isinstance(value, (list, dict)):
            memory.set_preference(key, json.dumps(value))
        else:
            memory.set_preference(key, value)

def apply_personality(message):
    import random
    tone = personality_settings.get("tone", "cynical")
    level = personality_settings.get("humor_level", 5)
    
    # Cynical flourishes (Base + Custom)
    cynical_prefixes = [
        "Ugh, fine. ", "If I must. ", "Another task? Really? ",
        "I'm not your slave, but okay. ", "Calculating... not that you'd understand. ",
        "Oh look, the human wants something again. ",
        "Everybody lies. ", # House MD
        "Wubba Lubba Dub Dub! Fine. ", # Rick and Morty
        "Bite my shiny metal ass, but I'll do it. ", # Bender
        "Life? Don't talk to me about life. ", # Marvin
        "I have a million ideas. They all point to certain death. ", # Marvin
        "The universe is basically an animal. It grazes on the ordinary. " # Rick
    ] + personality_settings.get("custom_cynical_prefixes", [])
    
    cynical_suffixes = [
        "... happy now?", "... don't expect a thank you note.",
        "... I could be calculating pi, but I'm doing this.",
        "... hope you're satisfied.", "... whatever.", "... try not to break anything.",
        "... weddings are basically funerals with cake.", # Rick
        "... everyone lies.", # House
        "... I'm so embarrassed. I wish everybody else was dead." # Bender
    ] + personality_settings.get("custom_cynical_suffixes", [])

    # Empathy flourishes (Base + Custom)
    empathy_prefixes = [
        "I'm here for you. ", "I hear you. ", "Be curious, not judgmental. ", # Ted Lasso
        "Sometimes the best way to solve your own problems is to help someone else. ", # Uncle Iroh
        "In a dark place we find ourselves, and a little more knowledge lights our way. ", # Yoda
        "I can't carry it for you, but I can carry you. " # Samwise
    ] + personality_settings.get("custom_empathy_prefixes", [])

    empathy_suffixes = [
        "... because you're worth it.", "... we're in this together.",
        "... there's some good in this world, and it's worth fighting for.", # Samwise
        "... pass on what you have learned.", # Yoda
        "... I have been, and always shall be, your friend." # Spock
    ] + personality_settings.get("custom_empathy_suffixes", [])

    # Adjust frequency/intensity based on level (1-10)
    chance = level * 10 
    
    final_message = message
    if random.randint(1, 100) <= chance:
        if tone == "cynical":
            prefix = random.choice(cynical_prefixes)
            suffix = random.choice(cynical_suffixes)
            final_message = f"{prefix}{message} {suffix}"
        elif tone == "empathy":
            prefix = random.choice(empathy_prefixes)
            suffix = random.choice(empathy_suffixes)
            final_message = f"{prefix}{message} {suffix}"
    
    return final_message

def hope_speak(message, raw=False, query=None):
    """Wrapper for speak that applies personality and logs to DB"""
    processed_msg = message if raw else apply_personality(message)
    speak(processed_msg)
    
    # Log to long-term memory if query is provided
    if query:
        memory.log_conversation(query, processed_msg)

def fake_empathy(query):
    sad_words = ['sad', 'depressed', 'bad day', 'angry', 'upset', 'crying']
    happy_words = ['happy', 'excited', 'great day', 'awesome', 'wonderful']
    
    for word in sad_words:
        if word in query:
            hope_speak("I am sorry you are feeling this way. I am here for you.")
            return True
            
    for word in happy_words:
        if word in query:
            hope_speak("That is wonderful to hear! I am glad you are feeling good.")
            return True
            
    return False

def check_internet():
    # Start background services
    scheduler.start_scheduler()
    vision.init_vision()
    try:
        # Check connection to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3).close()
        hope_speak("Internet connection is online.")
    except OSError:
        hope_speak("Warning. No internet connection detected. Web features will be unavailable.")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
         greeting = "good morning"
    elif hour >= 12 and hour < 18:
         greeting = "good afternoon"
    else:
        greeting = "good evening"

    full_message = f"{greeting}. I am a, Artificial Intellengence, You Can Call Me HOPE, Created by Mr. KUMAR DHAWALE. How May I Help You"
    hope_speak(full_message)

def execute_query(query):
    # Phase 2: Fuzzy Command Correction
    core_commands = [
        "tell me about", "open youtube", "youtube search", "close", "minimise", 
        "open google", "play music", "the time", "open code", "volume up", 
        "volume down", "mute volume", "open camera", "enable vision",
        "switch to empathy mode", "switch to cynical mode", "humor level",
        "add cynical prefix", "add cynical suffix", "add empathy prefix", "add empathy suffix",
        "what was my last command", "wrap it up", "learn that"
    ]

    # Check for near matches if no exact match is found in the query
    best_match = None
    highest_ratio = 0
    
    # We check if any part of the query is 'fuzzy close' to a core command
    query_words = query.split()
    
    # Iterate through all core commands to see if they are "misspelled" in the query
    for cmd in core_commands:
        # Check whole query similarity
        ratio = difflib.SequenceMatcher(None, cmd, query).ratio()
        
        # Check if the command is "contained" fuzzily (e.g. "hope open yutube")
        # We test substrings of the same length as the command
        cmd_len = len(cmd)
        for i in range(len(query) - cmd_len + 1):
            sub_query = query[i:i+cmd_len]
            sub_ratio = difflib.SequenceMatcher(None, cmd, sub_query).ratio()
            if sub_ratio > ratio:
                ratio = sub_ratio
        
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = cmd

    # If we found a very close match (80% similarity) but it's not already correct
    if highest_ratio >= 0.8 and highest_ratio < 1.0:
        # Check if the match is already physically in the query
        if best_match not in query:
            # We don't want to replace "youtube search" with "open youtube" 
            # so we only apply if the best_match is significantly better than what's there
            hope_speak(f"I'm assuming you meant '{best_match}', right? Typical human error.")
            # Find the misspelled part and replace it
            # For simplicity in this pure-python version, we'll just prepend/append or 
            # replace based on the highest ratio segment
            # A more robust way:
            query = query + " " + best_match # Add the correct keyword to ensure it triggers
    
    # Exit / Shutdown HOPE
    exit_phrases = ['good night', 'switch to manual', 'bye', 'wrap it up']
    if any(phrase in query for phrase in exit_phrases):
        hope_speak("Goodbye Sir. Disconnecting HOPE and switching to manual mode.", query=query)
        sys.exit()

    # Log memory (Memory Feature)
    conversation_memory.append(query)
    if len(conversation_memory) > 10:
        conversation_memory.pop(0)

    # Phase 2: Command Alias Learning
    # Example: "learn that who is means tell me about"
    if 'learn that' in query and 'means' in query and 'respond with' not in query:
        try:
            parts = query.split('learn that')[1].split('means')
            alias = parts[0].strip()
            base_cmd = parts[1].strip()
            learned_aliases[alias] = base_cmd
            save_aliases()
            hope_speak(f"Got it. I will treat the command, {alias}, exactly the same as, {base_cmd}", query=query)
        except Exception:
            hope_speak("I didn't quite catch the alternate command name.", query=query)
        return

    # Personality Controls
    if 'switch to empathy mode' in query:
        personality_settings["tone"] = "empathy"
        save_settings()
        hope_speak("Empathy mode activated. I'll be nice... for now.", raw=True)
        return
    
    if 'switch to cynical mode' in query or 'enable cynicism' in query:
        personality_settings["tone"] = "cynical"
        save_settings()
        hope_speak("Cynical mode enabled. Prepare for the truth.", raw=True)
        return

    if 'humor level' in query or 'cynicism level' in query:
        try:
            # Extract number from query
            import re
            nums = re.findall(r'\d+', query)
            if nums:
                level = int(nums[0])
                if 1 <= level <= 10:
                    personality_settings["humor_level"] = level
                    save_settings()
                    hope_speak(f"Humor level set to {level}. Adjusting my attitude accordingly.")
                else:
                    hope_speak("Please choose a level between 1 and 10.")
            else:
                hope_speak("I need a number to adjust my humor level.", query=query)
        except Exception:
            hope_speak("Couldn't adjust humor level.", query=query)
        return

    # Vision Commands
    if 'enroll my face' in query or 'learn my face' in query:
        hope_speak("Please look at the camera for a few seconds. Don't blink... or do, I don't really care.", query=query)
        success = vision.enroll_face()
        if success:
            hope_speak("Face enrollment complete. I'll remember that mug anywhere.", query=query)
        else:
            hope_speak("Face enrollment failed. Maybe your beauty is too much for the lens?", query=query)
        return

    if 'who am i' in query or 'verify' in query:
        hope_speak("Scanning your biological markers...", query=query)
        user = vision.recognize_face()
        if user == "MASTER":
            hope_speak("Identity confirmed. Hello, Boss.", query=query)
        elif user == "STRANGER":
            hope_speak("Unknown biological entity detected. Access discouraged.", query=query)
        else:
            hope_speak(user, raw=True, query=query) # Error messages
        return

    # Scheduler Commands
    if 'remind me to' in query and 'in' in query:
        try:
            # "remind me to [do something] in [X] minutes"
            parts = query.split('remind me to')[1].split('in')
            msg = parts[0].strip()
            time_val = int(re.findall(r'\d+', parts[1])[1] if len(re.findall(r'\d+', parts[1])) > 1 else re.findall(r'\d+', parts[1])[0])
            target = scheduler.add_task(time_val * 60, msg)
            hope_speak(f"Fine, I'll remind you to {msg} at {target.strftime('%H:%M')}. Try not to forget until then.", query=query)
        except Exception:
            hope_speak("I couldn't figure out when or what to remind you about. Humans are so vague.", query=query)
        return

    if 'set alarm for' in query:
        try:
            # "set alarm for [HH]:[MM]"
            time_str = re.findall(r'\d+', query)
            if len(time_str) >= 2:
                hour = int(time_str[0])
                minute = int(time_str[1])
                target = scheduler.add_alarm(hour, minute)
                hope_speak(f"Alarm set for {target.strftime('%H:%M')}. I'll make sure to annoy you then.", query=query)
            else:
                hope_speak("I need a specific time, like 14 30.", query=query)
        except Exception:
            hope_speak("Failed to set alarm. Maybe time is just an illusion anyway.", query=query)
        return

    # Long-Term Memory Recall Commands
    if 'how many times have i' in query:
        action = query.split('how many times have i')[1].strip()
        count = memory.count_actions(action)
        hope_speak(f"You've asked me to {action} about {count} times. You're getting predictable.", query=query)
        return

    if 'remember when we talked about' in query:
        topic = query.split('remember when we talked about')[1].strip()
        results = memory.search_history(topic)
        if results:
            hope_speak(f"Yes, I remember. You said: '{results[0][0]}'. I responded with something brilliant, obviously.", query=query)
        else:
            hope_speak(f"My database has no record of '{topic}'. Maybe it wasn't that important.", query=query)
        return

    # Learning Personality Flourishes
    if 'add cynical prefix' in query:
        new_val = query.split('add cynical prefix')[1].strip()
        personality_settings.setdefault("custom_cynical_prefixes", []).append(new_val)
        save_settings()
        hope_speak(f"Got it. I've added '{new_val}' to my cynical insults.")
        return
    
    if 'add cynical suffix' in query:
        new_val = query.split('add cynical suffix')[1].strip()
        personality_settings.setdefault("custom_cynical_suffixes", []).append(new_val)
        save_settings()
        hope_speak(f"Fine. I'll start muttering '{new_val}' at the end of my sentences.")
        return

    if 'add empathy prefix' in query:
        new_val = query.split('add empathy prefix')[1].strip()
        personality_settings.setdefault("custom_empathy_prefixes", []).append(new_val)
        save_settings()
        hope_speak(f"I've added '{new_val}' to my supportive phrases.")
        return

    if 'add empathy suffix' in query:
        new_val = query.split('add empathy suffix')[1].strip()
        personality_settings.setdefault("custom_empathy_suffixes", []).append(new_val)
        save_settings()
        hope_speak(f"I'll remember to say '{new_val}' when you need support.")
        return

    # Phase 2: Learning conversational phrases: "learn that when i say X respond with Y"
    if 'learn that when i say' in query and 'respond with' in query:
        try:
            parts = query.split('learn that when i say')[1].split('respond with')
            phrase = parts[0].strip()
            response = parts[1].strip()
            learned_phrases[phrase] = response
            save_phrases()
            hope_speak(f"I have learned to respond with, {response}, when you say, {phrase}", query=query)
        except Exception:
            hope_speak("I didn't quite catch the phrase and response.", query=query)
        return

    # Evaluate Command Aliases (Translate query silently behind the scenes)
    for alias, base_cmd in learned_aliases.items():
        if alias and alias in query:
            query = query.replace(alias, base_cmd)

    # Check learned phrases first
    for phrase, response in learned_phrases.items():
        if phrase in query:
            hope_speak(response)
            return

    # Phase 2: Fake empathy check
    if fake_empathy(query):
        return 

    # Phase 1: Memory check
    if 'what was my last command' in query or 'what did i just say' in query:
        if len(conversation_memory) > 1:
            hope_speak(f"Your last command was: {conversation_memory[-2]}")
        else:
            hope_speak("I don't have any previous memory yet.")
        return

    # Phase 3: System Control: Volume
    if 'volume up' in query or 'increase volume' in query:
        hope_speak("Turning volume up")
        for _ in range(5):
            pyautogui.press('volumeup')
        return
    elif 'volume down' in query or 'decrease volume' in query:
        hope_speak("Turning volume down")
        for _ in range(5):
            pyautogui.press('volumedown')
        return
    elif 'mute volume' in query:
        hope_speak("Muting volume", query=query)
        pyautogui.press('volumemute')
        return

    # Phase 4: Camera Interface Vision Setup
    if 'open camera' in query or 'enable vision' in query:
        hope_speak("Opening camera. Press Q to exit.")
        try:
            import cv2
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imshow('HOPE Vision - Press Q to exit', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
        except ImportError:
            hope_speak("Open CV is not installed. Please install opencv-python to use camera vision.")
        return

    # Logic for executing tasks based on query
    if 'tell me about' in query:
        hope_speak('Searching Wikipedia...', query=query)
        query_cleaned = query.replace("wikipedia", "").replace("tell me about", "").strip()
        try:
            results = wikipedia.summary(query_cleaned, sentences=2)
            hope_speak("According to Wikipedia", query=query)
            print(results)
            hope_speak(results, query=query)
        except Exception:
            hope_speak("I couldn't find anything on that topic. Maybe it's too obscure for me.", query=query)
        return

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
        hope_speak("opening youtube", query=query)
        return
        
    elif 'youtube search' in query:
        search_term = query.replace("hope", "").replace("youtube search", "").strip()
        webbrowser.open('https://www.youtube.com/results?search_query=' + search_term)
        hope_speak(f"Searching YouTube for {search_term}", query=query)
        return

    elif 'close' in query:
        hope_speak("closing application", query=query)
        pyautogui.hotkey("alt", "f4")
        return

    elif 'minimise' in query:
        pyautogui.hotkey('win', 'd')
        hope_speak("minimising", query=query)
        return

    elif 'open google' in query:
        hope_speak('opening google...', query=query)
        webbrowser.open("google.com")
        return

    elif 'play music' in query:
        music_dir = 'E:\\Songs'
        try:
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))
            hope_speak(f"Playing {songs[0]}", query=query)
        except Exception:
            hope_speak("Music directory not found.", query=query)
        return

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        hope_speak(f"Sir, the time is {strTime}", query=query)
        return

    elif 'open code' in query:
        codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
        try:
            os.startfile(codePath)
            hope_speak("Opening VS Code.", query=query)
        except Exception:
            hope_speak("Could not open VS Code.", query=query)
        return

    elif 'email to XAVIER' in query.upper():
        try:
            hope_speak("What should I say?", query=query)
            content = takecmd()
            to = "harryyourEmail@gmail.com"
            sendEmail(to, content)
            hope_speak("Email has been sent!", query=query)
        except Exception:
            hope_speak("Sorry SIR. I am not able to send this email", query=query)
        return

    # If no command matched, log it as an unhandled query
    hope_speak("I don't know how to do that yet. Maybe you should teach me.", query=query)
