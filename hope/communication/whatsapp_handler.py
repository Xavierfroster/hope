import pywhatkit
from hope.core import memory
from hope.core.engine import speak, takecmd

def send_whatsapp_message(recipient_name=None):
    """Handles the WhatsApp messaging flow."""
    if not recipient_name:
        speak("Who is the unfortunate recipient of this message?")
        recipient_name = takecmd().lower()
    
    if recipient_name == "none":
        return

    phone = memory.get_phone(recipient_name)
    if not phone:
        speak(f"I don't have a contact for {recipient_name}. What is the phone number? Include the country code.")
        phone = takecmd().replace(" ", "").strip()
        if "none" not in phone:
            memory.save_phone(recipient_name, phone)
        else:
            return
    
    speak(f"What should I say to {recipient_name}?")
    message = takecmd()
    
    if message != "none":
        try:
            speak(f"Sending message to {recipient_name}. This will take about 15 seconds. Don't touch anything.")
            pywhatkit.sendwhatmsg_instantly(phone, message, 15, True, 4)
            speak("WhatsApp message sent. Hopefully they don't block you.")
        except Exception as e:
            print(f"WhatsApp Error: {e}")
            speak("Failed to transmit the message. Maybe the internet finally gave up.")
