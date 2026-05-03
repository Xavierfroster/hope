from hope.gui import HopeGUI
from hope import features
from hope.core import takecmd
import threading

def voice_listener_loop():
    """Background thread to listen for voice commands even while GUI is open"""
    while True:
        query = takecmd().lower()
        if "none" in query:
            continue
            
        if "hey hope" in query or "hope" in query:
            # We don't speak "Yes sir" here to avoid interrupting GUI flow unless needed
            # but we update the log
            if features.gui_instance:
                features.gui_instance.add_log(f"> [Voice] {query}")
                
            clean_query = query.replace("hey hope", "").replace("hope", "").strip()
            if not clean_query:
                clean_query = takecmd().lower()
            
            if "none" not in clean_query:
                features.execute_query(clean_query)

if __name__ == "__main__":
    # 1. Initialize Backend
    features.check_internet()
    
    # 2. Setup GUI
    # We pass execute_query as the callback for text input
    app = HopeGUI(process_query_callback=features.execute_query)
    features.gui_instance = app
    
    # 3. Start Voice Listener in Background
    threading.Thread(target=voice_listener_loop, daemon=True).start()
    
    # 4. Start GUI (Main Thread)
    app.add_log("HOPE Dashboard Online. Awaiting your command.")
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
