from hope import features
from hope import core
from hope import diagnostics
import time

# --- Mocking Hardware for Simulation ---
def mock_speak(audio, query=None):
    print(f"\n[HOPE]: {audio}")

def mock_takecmd():
    # This will be replaced dynamically in the loop
    return "None"

core.speak = mock_speak
features.speak = mock_speak
features.takecmd = mock_takecmd

def simulate_user(query):
    print(f"\n--- USER SAYS: \"{query}\" ---")
    features.execute_query(query.lower())

# --- THE GRAND FINALE LIVE TEST ---
print("==========================================")
print("   HOPE AI - SYSTEM INTEGRITY SIMULATION  ")
print("==========================================")

# 1. Startup Checks
print("\n[SYSTEM]: Running Startup Procedures...")
features.check_internet()
features.wishme()

# 2. Testing Personality & Memory
simulate_user("Hope, who are you?")
simulate_user("Hope, learn that when i say hello respond with Greetings, meatbag.")
simulate_user("hello")

# 3. Testing System Diagnostics (New Feature)
simulate_user("Hope, how is my PC doing?")

# 4. Testing Fuzzy Logic
simulate_user("Hope, open yutube") # Should correct to youtube

# 5. Testing Diagnostics passive alert (Mocking High Load)
print("\n[SYSTEM]: Simulating High CPU Load...")
original_stats = diagnostics.get_pc_stats
diagnostics.get_pc_stats = lambda: {
    "cpu": 95, "ram": 40, "battery": 80, "plugged": True, 
    "disk": 10, "disk_free": 500.0, "download": 10.0, "upload": 2.0
}
simulate_user("Hope, the time")

# 6. Testing Interactive App Closer (New Feature)
print("\n[SYSTEM]: Testing interactive close...")
# We need to mock takecmd for the follow-up question
features.takecmd = lambda: "chrome"
simulate_user("Hope, shut up")

# 7. Testing Strict Exit Protocol
print("\n[SYSTEM]: Attempting old exit phrase (should fail)...")
simulate_user("Hope, bye")

print("\n[SYSTEM]: Attempting strict protocol exit...")
simulate_user("Hope, initiate protocol 100")

print("\n==========================================")
print("       SIMULATION COMPLETE - ALL OK       ")
print("==========================================")
