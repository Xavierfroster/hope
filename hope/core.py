import pyttsx3
import speech_recognition as sr

def speak(audio):
    print(f"HOPE: {audio}")
    try:
        # Initializing inline prevents the infamous 'run loop already started' pyttsx3 freeze
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
        return query.lower()  # Convert query to lowercase

    except Exception as e:
        print(e)
        speak("say that again.....")
        print("say that again......")
        return "None"
