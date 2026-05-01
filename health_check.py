import importlib
import sys
import os

def check_module(module_name, pip_name=None):
    try:
        importlib.import_module(module_name)
        print(f"[OK] {module_name} is installed.")
        return True
    except ImportError:
        install_cmd = pip_name if pip_name else module_name
        print(f"[MISSING] {module_name} is MISSING. (Fix: pip install {install_cmd})")
        return False

def check_face_recognition():
    try:
        import cv2
        if hasattr(cv2, 'face'):
            print("[OK] OpenCV Face Recognition (contrib) is installed.")
            return True
        else:
            print("[MISSING] OpenCV Face Recognition is MISSING. (Fix: pip install opencv-contrib-python)")
            return False
    except ImportError:
        return False

print("--- HOPE SYSTEM HEALTH CHECK ---")
print(f"Python Version: {sys.version}\n")

# List of required modules
modules = [
    ("pyttsx3", "pyttsx3"),
    ("speech_recognition", "SpeechRecognition"),
    ("pyautogui", "pyautogui"),
    ("wikipedia", "wikipedia"),
    ("cv2", "opencv-python"),
    ("numpy", "numpy"),
    ("pyaudio", "pyaudio")
]

results = []
for mod, pip in modules:
    results.append(check_module(mod, pip))

# Special check for Face ID
results.append(check_face_recognition())

# Check Database
if os.path.exists("learning/hope_memory.db"):
    print("[OK] Long-term memory database found.")
else:
    print("[WARNING] Database not found. (It will be created on first run)")

# Final Verdict
print("\n--- VERDICT ---")
if all(results):
    print("ALL SYSTEMS GO. HOPE is ready to be cynical.")
else:
    print("SOME COMPONENTS ARE MISSING. Please run the fix commands listed above.")
