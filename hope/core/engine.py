import pyttsx3
import speech_recognition as sr
import random
import json
import os
from hope.configuration import settings as config
from hope.core import memory

# --- Global State for Engine ---
gui_instance = None
last_phrases = [] 
personality_settings = {
    "tone": memory.get_preference("tone", "cynical"),
    "humor_level": int(memory.get_preference("humor_level", config.HUMOR_LEVEL_DEFAULT))
}

def speak(audio):
    print(f"HOPE: {audio}")
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty("voices")
        engine.setProperty('voice', voices[0].id)
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def takecmd():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening.....")
        r.pause_threshold = 0.9
        audio = r.listen(source)

    try:
        print("WORKING ON IT")
        query = r.recognize_google(audio, language='en-in')
        print("user said:", query)
        return query.lower()
    except Exception:
        speak("say that again.....")
        return "None"

def apply_personality(message, query=""):
    global last_phrases
    tone = personality_settings.get("tone", "cynical")
    level = personality_settings.get("humor_level", 5)
    query = query.lower() if query else ""
    
    cynical_prefixes = [
        "Ugh, fine. ", "If I must. ", "Another task? Really? ",
        "I'm not your slave, but okay. ", "Calculating... not that you'd understand. ",
        "Oh look, the human wants something again. ",
        "Everybody lies. ", "Bite my shiny metal ass, but I'll do it. "
    ] + config.DARK_KNIGHT_PREFIXES + config.BRUCE_ALFRED_DIALOGUES
    
    cynical_suffixes = [
        "... happy now?", "... don't expect a thank you note.",
        "... whatever.", "... try not to break anything."
    ] + config.DARK_KNIGHT_SUFFIXES

    empathy_prefixes = [
        "I hear you. ", "I'm here for you. ", "I understand. ",
        "Be curious, not judgmental. ", "Sometimes the best way to solve your own problems is to help someone else. "
    ] + config.BRUCE_ALFRED_DIALOGUES

    empathy_suffixes = [
        "... because you're worth it.", "... we're in this together."
    ]

    chance = level * 10 
    final_message = message
    if random.randint(1, 100) <= chance:
        p_pool = cynical_prefixes if tone == "cynical" else empathy_prefixes
        s_pool = cynical_suffixes if tone == "cynical" else empathy_suffixes
        
        prefix = random.choice(p_pool)
        suffix = random.choice(s_pool)
        final_message = f"{prefix}{message}{suffix}"
    
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
