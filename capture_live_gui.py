import subprocess
import time
import pyautogui
import os
from hope import diagnostics

def run_gui_and_capture():
    print("[SYSTEM]: Launching HOPE GUI for live capture...")
    
    # Launch gui_main.py as a separate process
    # Note: We use a small delay to let it render
    process = subprocess.Popen(["python", "gui_main.py"])
    
    print("[SYSTEM]: Waiting 8 seconds for GUI to initialize and stabilize...")
    time.sleep(8)
    
    print("[SYSTEM]: Capturing screenshot of the desktop...")
    screenshot = pyautogui.screenshot()
    
    # Save to artifacts directory
    save_path = "live_gui_capture.png"
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
