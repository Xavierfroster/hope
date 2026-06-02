import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import subprocess
import time
import pyautogui
from hope import diagnostics

def run_gui_and_capture():
    print("[SYSTEM]: Launching HOPE GUI for live capture...")
    
    # Resolve the project root folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Launch gui_main.py as a separate process in the project root directory
    process = subprocess.Popen(["python", "gui_main.py"], cwd=base_dir)
    
    print("[SYSTEM]: Waiting 8 seconds for GUI to initialize and stabilize...")
    time.sleep(8)
    
    print("[SYSTEM]: Capturing screenshot of the desktop...")
    screenshot = pyautogui.screenshot()
    
    # Save to docs folder
    save_path = os.path.join(base_dir, "docs", "live_gui_capture.png")
    screenshot.save(save_path)
    
    print(f"[SYSTEM]: Screenshot saved to {save_path}")
    
    # Terminate the GUI process
    process.terminate()
    print("[SYSTEM]: GUI test complete.")

if __name__ == "__main__":
    try:
        run_gui_and_capture()
    except Exception as e:
        print(f"Error during capture: {e}")
