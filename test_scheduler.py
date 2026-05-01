import features
import core
import scheduler
import time

# Mock TTS
def mock_speak(audio):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak

def run_test(command):
    print(f"\n[USER]: {command}")
    features.execute_query(command)

print("--- STARTING SCHEDULER TEST ---")

# 1. Start Services
scheduler.start_scheduler()

# 2. Set a 5-second reminder
run_test("remind me to check the oven in 0 minutes") # Using 0 for instant test
# (Wait, my logic uses time_val * 60, so 0 might be immediate)

# Actually, let's use a real wait
run_test("remind me to take a break in 1 minutes")

print("\nWaiting for scheduler to trigger (this should take ~10-20 seconds due to sleep)...")
# Note: I won't wait the full minute here, I'll just check if the task was added
print(f"Active tasks: {scheduler.scheduled_tasks}")

# Test alarm setting
run_test("set alarm for 12 30")

print("\n--- TEST COMPLETE ---")
