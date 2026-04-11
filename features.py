import datetime
import smtplib
import pyautogui
import os
import webbrowser
import wikipedia
import socket
import json
import sys
from core import speak, takecmd

# --- Memory and Learning System ---
conversation_memory = []
learned_phrases = {}
learned_aliases = {}
LEARNING_DIR = "learning"
LEARNING_FILE = os.path.join(LEARNING_DIR, "learned_phrases.json")
ALIAS_FILE = os.path.join(LEARNING_DIR, "command_aliases.json")

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

def fake_empathy(query):
    sad_words = ['sad', 'depressed', 'bad day', 'angry', 'upset', 'crying']
    happy_words = ['happy', 'excited', 'great day', 'awesome', 'wonderful']
    
    for word in sad_words:
        if word in query:
            speak("I am sorry you are feeling this way. I am here for you.")
            return True
            
    for word in happy_words:
        if word in query:
            speak("That is wonderful to hear! I am glad you are feeling good.")
            return True
            
    return False

def check_internet():
    try:
        # Check connection to Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3).close()
        speak("Internet connection is online.")
    except OSError:
        speak("Warning. No internet connection detected. Web features will be unavailable.")

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
    speak(full_message)

def execute_query(query):
    # Exit / Shutdown HOPE
    exit_phrases = ['good night', 'switch to manual', 'bye', 'wrap it up']
    if any(phrase in query for phrase in exit_phrases):
        speak("Goodbye Sir. Disconnecting HOPE and switching to manual mode.")
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
            speak(f"Got it. I will treat the command, {alias}, exactly the same as, {base_cmd}")
        except Exception:
            speak("I didn't quite catch the alternate command name.")
        return

    # Phase 2: Learning conversational phrases: "learn that when i say X respond with Y"
    if 'learn that when i say' in query and 'respond with' in query:
        try:
            parts = query.split('learn that when i say')[1].split('respond with')
            phrase = parts[0].strip()
            response = parts[1].strip()
            learned_phrases[phrase] = response
            save_phrases()
            speak(f"I have learned to respond with, {response}, when you say, {phrase}")
        except Exception:
            speak("I didn't quite catch the phrase and response.")
        return

    # Evaluate Command Aliases (Translate query silently behind the scenes)
    for alias, base_cmd in learned_aliases.items():
        if alias and alias in query:
            query = query.replace(alias, base_cmd)

    # Check learned phrases first
    for phrase, response in learned_phrases.items():
        if phrase in query:
            speak(response)
            return

    # Phase 2: Fake empathy check
    if fake_empathy(query):
        return 

    # Phase 1: Memory check
    if 'what was my last command' in query or 'what did i just say' in query:
        if len(conversation_memory) > 1:
            speak(f"Your last command was: {conversation_memory[-2]}")
        else:
            speak("I don't have any previous memory yet.")
        return

    # Phase 3: System Control: Volume
    if 'volume up' in query or 'increase volume' in query:
        speak("Turning volume up")
        for _ in range(5):
            pyautogui.press('volumeup')
        return
    elif 'volume down' in query or 'decrease volume' in query:
        speak("Turning volume down")
        for _ in range(5):
            pyautogui.press('volumedown')
        return
    elif 'mute volume' in query:
        speak("Muting volume")
        pyautogui.press('volumemute')
        return

    # Phase 4: Camera Interface Vision Setup
    if 'open camera' in query or 'enable vision' in query:
        speak("Opening camera. Press Q to exit.")
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
            speak("Open CV is not installed. Please install opencv-python to use camera vision.")
        return

    # Logic for executing tasks based on query
    if 'tell me about' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")
        speak("opening youtube")
        
    elif 'youtube search' in query:
        query = query.replace("hope", "")
        query = query.replace("youtube search", "")
        webbrowser.open('https://www.youtube.com/results?search_query=' + query)

    elif 'close' in query:
        speak("closing application" )
        pyautogui.hotkey("alt", "f4")

    elif 'minimise' in query:
        pyautogui.hotkey('win', 'd')
        speak("minimising")

    elif 'open google' in query:
        speak('opening google...')
        webbrowser.open("google.com")

    elif 'play music' in query:
        music_dir = 'E:\\Songs'
        try:
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))
        except FileNotFoundError:
            speak("Music directory not found.")
            print("Music directory not found.")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'open code' in query:
        codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
        try:
            os.startfile(codePath)
        except Exception:
            speak("Could not open VS Code.")

    elif 'email to XAVIER' in query.upper():
        try:
            speak("What should I say?")
            content = takecmd()
            to = "harryyourEmail@gmail.com"
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
           print(e)
           speak("Sorry SIR. I am not able to send this email")
