import os
import sys
import time

# Add root folder to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hope.core import engine
from hope.core.voice_effects import apply_optimus_effect

print("====================================================")
print("     PROJECT HOPE: OPTIMUS PRIME VOICE DIAGNOSTIC   ")
print("====================================================")

# 1. Store original voice setting
original_voice = engine.active_voice_type
print(f"Original Voice Type: {original_voice}")

# 2. Switch to Optimus Prime
print("Switching voice mode to: optimus_prime...")
engine.update_voice_type("optimus_prime")

# 3. Speak iconic quote
quote = "I am Optimus Prime. We are here, and we are waiting."
print(f"Synthesising and processing: '{quote}'")
engine.speak(quote)

# 4. Restore original voice
print(f"Restoring voice mode to: {original_voice}...")
engine.update_voice_type(original_voice)

print("====================================================")
print("              DIAGNOSTIC TEST COMPLETE              ")
print("====================================================")
