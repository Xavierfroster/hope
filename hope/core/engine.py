import pyttsx3
import speech_recognition as sr
import random
import json
import os
import time
import winsound
from hope.configuration import settings as config
from hope.core import memory
from hope.core.voice_effects import apply_optimus_effect

# Load active voice type
active_voice_type = memory.get_preference("voice_type", "default")
# Load standby mode status
standby_mode = memory.get_preference("standby_mode", "False") == "True"

def update_voice_type(voice_type):
    """Updates the voice type preference (default/optimus_prime) and persists it to the database."""
    global active_voice_type
    if voice_type in ["default", "optimus_prime"]:
        active_voice_type = voice_type
        memory.set_preference("voice_type", voice_type)
        return True
    return False

def update_standby_mode(status):
    """Updates the standby mode status persistently and dynamically."""
    global standby_mode
    standby_mode = status
    memory.set_preference("standby_mode", str(status))
    return True

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

import threading

# Thread-local storage for SAPI5 TTS engines and a global lock to serialize speech
_local_tts = threading.local()
tts_lock = threading.Lock()

def get_tts_engine():
    """Initializes or retrieves a thread-local SAPI5 engine, completely avoiding Windows COM collisions."""
    if not hasattr(_local_tts, "engine"):
        try:
            _local_tts.engine = pyttsx3.init('sapi5')
            voices = _local_tts.engine.getProperty("voices")
            _local_tts.engine.setProperty('voice', voices[0].id)
        except Exception as e:
            print(f"TTS Thread-Local Initialization Error: {e}")
            _local_tts.engine = None
    return _local_tts.engine

def speak(audio):
    if standby_mode:
        print(f"HOPE [Silenced - Standby]: {audio}")
        return
        
    # Add a leading comma and small pause to fix truncation issues on some systems
    processed_audio = f", , {audio}"
    print(f"HOPE: {audio}")
    
    with tts_lock:
        engine_instance = get_tts_engine()
        if engine_instance:
            try:
                if active_voice_type == "optimus_prime":
                    # Optimus Prime Voice Process
                    original_rate = engine_instance.getProperty('rate')
                    # Set synthesized speed to fast (to compensate for resampling slow-down)
                    engine_instance.setProperty('rate', 260)
                    
                    if not os.path.exists(config.RESOURCES_DIR):
                        os.makedirs(config.RESOURCES_DIR)
                        
                    temp_raw = os.path.join(config.RESOURCES_DIR, "temp_raw.wav")
                    temp_proc = os.path.join(config.RESOURCES_DIR, "temp_proc.wav")
                    
                    # Delete existing temp files
                    for f in [temp_raw, temp_proc]:
                        if os.path.exists(f):
                            try:
                                os.remove(f)
                            except Exception:
                                pass
                    
                    # Save TTS raw synthesis to temporary WAV
                    engine_instance.save_to_file(processed_audio, temp_raw)
                    engine_instance.runAndWait()
                    
                    # Restore original rate
                    engine_instance.setProperty('rate', original_rate)
                    
                    # Apply Optimus Prime DSP effect
                    if os.path.exists(temp_raw):
                        apply_optimus_effect(temp_raw, temp_proc)
                        
                        # Play the mechanical voice
                        if os.path.exists(temp_proc):
                            winsound.PlaySound(temp_proc, winsound.SND_FILENAME)
                            time.sleep(1) # Short delay
                else:
                    # Default SAPI5 Voice
                    engine_instance.say(processed_audio)
                    engine_instance.runAndWait()
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
