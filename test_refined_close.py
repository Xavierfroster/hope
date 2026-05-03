from hope import features
from hope import core
import sys

# Mock TTS
def mock_speak(audio, query=None):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak

# Mock taking command
command_queue = []
def mock_takecmd():
    if command_queue:
        cmd = command_queue.pop(0)
        print(f"[MOCK INPUT]: {cmd}")
        return cmd
    return "none"

features.takecmd = mock_takecmd

def run_test(query, follow_up=None):
    print(f"\n[USER]: {query}")
    if follow_up:
        command_queue.append(follow_up)
    try:
        features.execute_query(query)
    except SystemExit:
        print("HOPE has exited (SystemExit).")

print("--- STARTING REFINED CLOSE TEST ---")

# 1. Test standard 'close' command
run_test("close", follow_up="chrome")

# 2. Test 'shut up' trigger
run_test("shut up", follow_up="notepad")

# 3. Test strict exit protocol (Fail case: old phrases)
print("\n--- TESTING OLD EXIT PHRASES (Should NOT exit) ---")
run_test("bye") # Should trigger 'I don't know how to do that yet' or similar if not in exit_phrases

# 4. Test strict exit protocol (Success case)
print("\n--- TESTING PROTOCOL 100 ---")
run_test("initiate protocol 100")

print("\n--- TEST COMPLETE ---")
