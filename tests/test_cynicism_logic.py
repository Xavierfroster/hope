from hope import features, core
import os

# Mock the speak function to prevent pyttsx3 hang
def mock_speak(audio):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak # Just in case

def run_test(command):
    print(f"\n[USER]: {command}")
    features.execute_query(command)

print("--- STARTING CYNICISM TEST (TTS MOCKED) ---")

# Ensure we are in Cynical Mode at Max Humor (10)
features.personality_settings["tone"] = "cynical"
features.personality_settings["humor_level"] = 10
features.save_settings()

print(f"Current Settings: {features.personality_settings}")

# Test normal commands with high cynicism (100% chance of sarcasm)
run_test("the time")
run_test("open google")
run_test("what was my last command")

# Test switching to Empathy mode
run_test("switch to empathy mode")
run_test("the time")

# Test humor level adjustment
run_test("switch to cynical mode")
run_test("set humor level to 1") 
# At level 1, there's only a 10% chance of sarcasm
print("\n[NOTE] Humor level is now 1. Sarcasm is rare (10% chance).")
for _ in range(5):
    run_test("the time")

print("\n--- TEST COMPLETE ---")
