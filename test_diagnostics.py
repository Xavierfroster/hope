from hope import features
from hope import core
from hope import diagnostics

# Mock TTS
def mock_speak(audio, query=None):
    print(f"HOPE: {audio}")

core.speak = mock_speak
features.speak = mock_speak

def run_test(command):
    print(f"\n[USER]: {command}")
    features.execute_query(command)

print("--- STARTING SYSTEM DIAGNOSTICS TEST ---")

# 1. Test Command
run_test("how is my pc doing")

# 2. Mock a high load situation to test passive alerts
print("\n--- MOCKING HIGH LOAD (>80%) ---")
# Temporarily monkeypatch get_pc_stats
original_stats = diagnostics.get_pc_stats
diagnostics.get_pc_stats = lambda: {
    "cpu": 90, "ram": 40, "battery": 50, "plugged": False, 
    "disk": 10, "disk_free": 500.0, "download": 0.0, "upload": 0.0
}

run_test("open youtube") # Passive check should trigger here

# 3. Mock low battery (<20%)
print("\n--- MOCKING LOW BATTERY (<20%) ---")
diagnostics.get_pc_stats = lambda: {
    "cpu": 10, "ram": 10, "battery": 15, "plugged": False,
    "disk": 10, "disk_free": 500.0, "download": 0.0, "upload": 0.0
}

run_test("the time") # Passive check should trigger here

# 4. Mock low disk (>95%)
print("\n--- MOCKING LOW DISK (>95%) ---")
diagnostics.get_pc_stats = lambda: {
    "cpu": 10, "ram": 10, "battery": 50, "plugged": True,
    "disk": 98, "disk_free": 1.5, "download": 0.0, "upload": 0.0
}

run_test("open google")

# Restore
diagnostics.get_pc_stats = original_stats

print("\n--- TEST COMPLETE ---")
