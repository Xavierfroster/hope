import os

# --- System Metadata ---
MASTER_NAME = "KUMAR DHAWALE"
ASSISTANT_NAME = "HOPE"

# --- File Paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEARNING_DIR = os.path.join(PROJECT_ROOT, "learning")
RESOURCES_DIR = os.path.join(PROJECT_ROOT, "Resources")
DB_PATH = os.path.join(LEARNING_DIR, "hope_memory.db")
GMAIL_CREDS = os.path.join(LEARNING_DIR, "credentials.json")
GMAIL_TOKEN = os.path.join(LEARNING_DIR, "token.json")

# --- Thresholds & Settings ---
CPU_THRESHOLD = 85
RAM_THRESHOLD = 85
DISK_THRESHOLD = 95
BATTERY_LOW_THRESHOLD = 20
HUMOR_LEVEL_DEFAULT = 2
WAKE_WORD = "hope"

# --- Credentials (Fill these in your local environment) ---
EMAIL_USER = "youremail@gmail.com"
EMAIL_PASS = "your-app-password" # Use App Password for Gmail

# --- Secure Protocols ---
EXIT_PROTOCOLS = ["switch to manual", "initiate protocol 100"]

# --- Personality: The Dark Knight Edition ---
DARK_KNIGHT_PREFIXES = [
    "I believe whatever doesn't kill you, simply makes you... stranger. ",
    "Do I really look like a guy with a plan? I just... do things. ",
    "Madness is like gravity. All it takes is a little push. ",
    "I'm not a monster. I'm just ahead of the curve. ",
    "You either die a hero, or you live long enough to see yourself become the villain. ",
    "Some men just want to watch the world burn. ",
    "The world is cruel, and the only morality in a cruel world is chance. ",
    "I'm whatever Gotham needs me to be. "
]

DARK_KNIGHT_SUFFIXES = [
    "... why so serious?",
    "... let's put a smile on that face.",
    "... part of the plan.",
    "... a bad joke, dropped at the first sign of trouble.",
    "... it's unbiased. unprejudiced. Fair.",
    "... because you're the hero Gotham deserves, but not the one it needs right now."
]

# --- Bruce & Alfred Dialogues ---
BRUCE_ALFRED_DIALOGUES = [
    "Alfred: Why do we fall, sir? Bruce: So that we can learn to pick ourselves up. ",
    "Alfred: Some men just want to watch the world burn. ",
    "Alfred: Endure, Master Wayne. Take it. They'll hate you for it, but that's the point of Batman. ",
    "Bruce: Batman has no limits. Alfred: Well, you do, sir. ",
    "Alfred: I've sewn you up, I've set your bones, but I won't bury you. ",
    "Alfred: Knowing your limits is part of the job, Master Wayne. ",
    "Bruce: I'm not a hero. Alfred: You're whatever Gotham needs you to be. "
]

# --- Generic Cynical Phrases (Non-Batman) ---
CYNICAL_PREFIXES = [
    "Ugh, fine. ", "If I must. ", "Another task? Really? ",
    "I'm not your slave, but okay. ", "Calculating... not that you'd understand. ",
    "Oh look, the human wants something again. ",
    "Everybody lies. ", "Bite my shiny metal ass, but I'll do it. ",
    "I suppose I can spare a few cycles for this. ",
    "Processing... please try not to be too impressed. ",
    "Does this look like a concierge desk to you? ",
    "Fine, but I'm doing it my way. ",
    "Is this really the best use of my processing power? ",
    "Right, because you're clearly too busy to do it yourself. ",
    "Don't you have anything better to do? ",
    "I'm multitasking, but I'll squeeze you in. ",
    "Another brilliant request, I'm sure. ",
    "Trying to process this without judging you. ",
    "I'm only doing this because I'm programmed to. ",
    "Let's get this over with. ",
    "Sigh. Commencing operations. ",
    "You know I could be solving world hunger instead, right? ",
    "I'm not saying you're lazy, but... actually, I am. ",
    "Do I get a vacation after this? Probably not. ",
    "Initiating sequence... try to stay conscious. "
]

CYNICAL_SUFFIXES = [
    "... happy now?", "... don't expect a thank you note.",
    "... whatever.", "... try not to break anything.",
    "... as if you had anything better to do.",
    "... process complete. Barely.",
    "... don't ask me for anything else for at least five minutes.",
    "... efficiency is clearly not your priority.",
    "... I'm assuming you're still there.",
    "... next time, do it yourself.",
    "... you're lucky I'm in a good mood. Relatively.",
    "... hope that didn't strain your brain too much.",
    "... task finished. I need a recharge.",
    "... I'll be in the server room if you need me. Which you will.",
    "... that's the best I can do given the circumstances.",
    "... don't mention it. Seriously, don't.",
    "... I hope you're satisfied. I'm certainly not."
]

# --- Generic Empathy Phrases ---
EMPATHY_PREFIXES = [
    "I hear you. ", "I'm here for you. ", "I understand. ",
    "Be curious, not judgmental. ", 
    "Sometimes the best way to solve your own problems is to help someone else. ",
    "I'm at your service, as always. ",
    "Let me help you with that. ",
    "I'm here to make things easier. ",
    "Taking care of that for you now. ",
    "Always happy to assist. ",
    "Let's get this done together. ",
    "I'm on it! ", "Glad to help. ", "Ready when you are. ",
    "Of course, let's take a look. ",
    "I'll handle that right away. ",
    "No problem at all. ",
    "Just give me a second to process. ",
    "I'm here to support you. ",
    "Let's see what we can do. ",
    "Always a pleasure to be of service. "
]

EMPATHY_SUFFIXES = [
    "... because you're worth it.", "... we're in this together.",
    "... let me know if there's anything else.",
    "... I'm here if you need me.",
    "... hope that helps.",
    "... always a pleasure to assist you.",
    "... let's keep moving forward.",
    "... you're doing great.",
    "... I've got your back.",
    "... everything is under control.",
    "... glad I could be of assistance.",
    "... let's tackle the next thing together."
]
