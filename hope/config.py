import os

# --- System Metadata ---
MASTER_NAME = "KUMAR DHAWALE"
ASSISTANT_NAME = "HOPE"

# --- File Paths ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEARNING_DIR = os.path.join(PROJECT_ROOT, "learning")
RESOURCES_DIR = os.path.join(PROJECT_ROOT, "Resources")
DB_PATH = os.path.join(LEARNING_DIR, "hope_memory.db")

# --- Thresholds & Settings ---
CPU_THRESHOLD = 80
RAM_THRESHOLD = 80
DISK_THRESHOLD = 95
BATTERY_LOW_THRESHOLD = 20
HUMOR_LEVEL_DEFAULT = 5
WAKE_WORD = "hope"

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
