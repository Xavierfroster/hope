from hope import features, core
import os

# Mock the speak function to prevent pyttsx3 hang
def mock_speak(audio):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak 

def run_test(command):
    print(f"\n[USER]: {command}")
    features.execute_query(command)

print("--- STARTING EXTENDED CYNICISM TEST (HUMOR LEVEL 10) ---")

# Ensure Max Cynicism
features.personality_settings["tone"] = "cynical"
features.personality_settings["humor_level"] = 10
features.save_settings()

# 1. System Controls
run_test("volume up")
run_test("minimise")

# 2. Web & Knowledge (These will mock the actions but show the text)
run_test("tell me about Python programming")
run_test("youtube search how to tolerate humans")

# 3. File/App interaction
run_test("open code")
run_test("play music")

# 4. Personality checks
run_test("learn that when i say you are mean respond with truth hurts")
run_test("you are mean")

# 5. Exit
run_test("wrap it up")

print("\n--- TEST COMPLETE ---")
