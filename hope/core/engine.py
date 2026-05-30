import pyttsx3
import speech_recognition as sr
import random
import json
import os
import time
from hope.configuration import settings as config
from hope.core import memory

# --- Global State for Engine ---
gui_instance = None
last_phrases = [] 
personality_settings = {
    "tone": memory.get_preference("tone", "cynical"),
    "humor_level": int(memory.get_preference("humor_level", config.HUMOR_LEVEL_DEFAULT)),
    "system_alerts": memory.get_preference("system_alerts", "True") == "True"
}

def update_humor_level(level):
    """Updates the humor level and persists it to the database."""
    try:
        level = int(level)
        if 0 <= level <= 10:
            personality_settings["humor_level"] = level
            memory.set_preference("humor_level", str(level))
            return True
    except (ValueError, TypeError):
        pass
    return False

def update_tone(tone):
    """Updates the tone (cynical/empathy) and persists it to the database."""
    if tone in ["cynical", "empathy"]:
        personality_settings["tone"] = tone
        memory.set_preference("tone", tone)
        return True
    return False

def update_system_alerts(status):
    """Toggles system health alerts."""
    personality_settings["system_alerts"] = status
    memory.set_preference("system_alerts", str(status))
    return True

# Global TTS Engine Initialization
try:
    tts_engine = pyttsx3.init('sapi5')
    voices = tts_engine.getProperty("voices")
    tts_engine.setProperty('voice', voices[0].id)
except Exception as e:
    print(f"TTS Initialization Error: {e}")
    tts_engine = None

def speak(audio):
    # Add a leading comma and small pause to fix truncation issues on some systems
    processed_audio = f", , {audio}"
    print(f"HOPE: {audio}")
    
    if tts_engine:
        try:
            # Sync personality settings for speed if needed
            # (Note: we use the rate set by the user or default)
            # rate = tts_engine.getProperty('rate')
            # tts_engine.setProperty('rate', int(rate * 1)) 
            
            tts_engine.say(processed_audio)
            tts_engine.runAndWait()
            time.sleep(2) # Delay after speaking
        except Exception as e:
            print(f"TTS Error: {e}")
    else:
        print("TTS Engine not available.")

def takecmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("WORKING ON IT")
        query = r.recognize_google(audio, language='en-in')
        print("user said:", query)
        time.sleep(2) # Delay after receiving command before returning
        return query.lower()
    except Exception:
        speak("say that again.....")
        return "None"

def apply_personality(message, query=""):
    global last_phrases
    tone = personality_settings.get("tone", "cynical")
    level = personality_settings.get("humor_level", config.HUMOR_LEVEL_DEFAULT)
    
    # Base Pools
    p_pool = config.CYNICAL_PREFIXES[:] if tone == "cynical" else config.EMPATHY_PREFIXES[:]
    s_pool = config.CYNICAL_SUFFIXES[:] if tone == "cynical" else config.EMPATHY_SUFFIXES[:]

    # Batman Logic: Only mix in cinematic phrases based on humor level and randomness
    batman_chance = level / 10.0 # 0.0 to 1.0
    
    if random.random() < batman_chance:
        # Add a slice of Batman phrases instead of the whole thing
        if tone == "cynical":
            # Cynical Batman (Joker/Bane/Dark Knight)
            p_pool += random.sample(config.DARK_KNIGHT_PREFIXES, min(len(config.DARK_KNIGHT_PREFIXES), 3))
            s_pool += random.sample(config.DARK_KNIGHT_SUFFIXES, min(len(config.DARK_KNIGHT_SUFFIXES), 2))
        else:
            # Empathy Batman (Alfred/Bruce)
            p_pool += random.sample(config.BRUCE_ALFRED_DIALOGUES, min(len(config.BRUCE_ALFRED_DIALOGUES), 3))
            # Suffixes are mostly cinematic cynicism, so we skip for empathy unless mixed
            
    # Final chance to apply ANY personality
    trigger_chance = level * 10 # e.g., 20% for level 2
    final_message = message
    
    if random.randint(1, 100) <= trigger_chance:
        prefix = random.choice(p_pool)
        suffix = random.choice(s_pool)
        
        # Avoid repeating the exact same cinematic phrase twice in a row if possible
        if prefix in last_phrases:
            prefix = random.choice(p_pool)
            
        final_message = f"{prefix}{message}{suffix}"
        last_phrases = [prefix, suffix] # Simple tracking
    
    return final_message

def hope_speak(message, raw=False, query=None):
    """Unified speak function with personality and logging."""
    processed_msg = message if raw else apply_personality(message, query=query)
    
    if gui_instance:
        gui_instance.add_log(f"HOPE: {processed_msg}")
        
    speak(processed_msg)
    if query:
        memory.log_conversation(query, processed_msg)

def confirm_action(prompt, query=None):
    """Asks for confirmation before proceeding with an automation task."""
    hope_speak(prompt, query=query)
    response = takecmd().lower()
    
    if any(word in response for word in ['yes', 'go ahead', 'proceed', 'do it', 'yeah', 'sure']):
        return True
    
    if any(word in response for word in ['stop', 'no', 'abort', 'cancel', 'don\'t']):
        hope_speak("Task aborted. I'll just sit here and wait for you to change your mind.")
        return False
        
    hope_speak("I didn't catch a clear confirmation. Aborting the task for safety.")
    return False
