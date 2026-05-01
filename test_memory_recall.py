import features
import core
import memory
import os

# Mock TTS
def mock_speak(audio):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak

def run_test(command):
    print(f"\n[USER]: {command}")
    features.execute_query(command)

print("--- STARTING LONG-TERM MEMORY TEST ---")

# 1. Generate some history
run_test("open youtube")
run_test("tell me about black holes")
run_test("the time")

# 2. Test Recall Commands
run_test("how many times have i open youtube")
run_test("remember when we talked about black holes")

print("\n--- TEST COMPLETE ---")
