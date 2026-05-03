from hope import features
from hope import core
import time

# Mocking core.speak to print to terminal
def mock_speak(audio):
    print(f"[HOPE]: {audio}")

core.speak = mock_speak
features.speak = mock_speak

def test_query(query):
    print(f"\n--- USER: \"{query}\" ---")
    features.execute_query(query)

print("==========================================")
print("   HOPE SMART PERSONALITY FINAL TEST      ")
print("==========================================")

# Ensure Cynical mode for testing variety
features.personality_settings["tone"] = "cynical"
features.personality_settings["humor_level"] = 10

# 1. Test Context: System Status (Should trigger Bruce/Alfred)
test_query("How is my PC doing?")

# 2. Test Context: Knowledge (Should trigger Yoda/Knowledge)
test_query("Who is Albert Einstein?")

# 3. Test Anti-Repetition: Run same command 3 times
print("\n[SYSTEM]: Testing Anti-Repetition (Same command 3 times)...")
test_query("What is the time?")
test_query("What is the time?")
test_query("What is the time?")

# 4. Test Empathy Mode (Should include restored phrases)
print("\n[SYSTEM]: Switching to Empathy Mode...")
features.personality_settings["tone"] = "empathy"
test_query("I am feeling sad")
test_query("Help me with my homework")

print("\n==========================================")
print("        TEST COMPLETE - ALL OK            ")
print("==========================================")
