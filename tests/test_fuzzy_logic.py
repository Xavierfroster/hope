from hope import features, core

# Mock TTS
def mock_speak(audio):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak

def run_test(command):
    print(f"\n[USER]: {command}")
    features.execute_query(command)

print("--- STARTING FUZZY LOGIC TEST ---")

# Ensure Cynical mode for that extra bite
features.personality_settings["tone"] = "cynical"
features.personality_settings["humor_level"] = 10

# Test misspelled commands
run_test("open yutube")        # Should match 'open youtube'
run_test("search wikpedia")    # Should match 'tell me about' or similar if keywords were updated
run_test("the thyme")          # Should match 'the time'
run_test("volum up")           # Should match 'volume up'
run_test("enable vizion")      # Should match 'enable vision'

print("\n--- TEST COMPLETE ---")
