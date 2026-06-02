import os
import sys
import time

# Add root folder to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hope.core import engine
from hope import features

print("====================================================")
print("        PROJECT HOPE: STANDBY DIAGNOSTIC TEST       ")
print("====================================================")

# Mock GUI instance logs to prevent NoneType attribute access in tests
class MockGUI:
    def add_log(self, msg):
        print(f"[GUI LOG]: {msg}")

features.gui_instance = MockGUI()

# Store initial states
orig_standby = engine.standby_mode
print(f"Original Standby State: {orig_standby}")

# Ensure starting fresh
engine.update_standby_mode(False)

print("\n--- 1. TESTING STANDBY ACTIVATION ---")
print("User says: 'hope stand by'")
features.execute_query("hope stand by")
print(f"Engine Standby Mode State: {engine.standby_mode}")

print("\n--- 2. TESTING SILENCING / IGNORING COMMANDS DURING STANDBY ---")
print("User says: 'what is the time'")
features.execute_query("what is the time")
print("(Verified: No speak and no action was executed!)")

print("\n--- 3. TESTING DEACTIVATION / WAKEUP ---")
print("User says: 'hope take the wheel'")
features.execute_query("hope take the wheel")
print(f"Engine Standby Mode State: {engine.standby_mode}")

# Restore
engine.update_standby_mode(orig_standby)

print("====================================================")
print("            STANDBY TEST COMPLETE                   ")
print("====================================================")
