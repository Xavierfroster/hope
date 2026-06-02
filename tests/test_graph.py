import customtkinter as ctk
import os
import sys

# Add root folder to python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hope.gui.graph_visualization import ProjectGraphWindow

print("====================================================")
print("     PROJECT HOPE: NEURAL ARCHITECTURE DIAGNOSTIC    ")
print("====================================================")

# Initialize CustomTkinter window context
root = ctk.CTk()
root.geometry("100x100")
root.withdraw() # Keep parent hidden during test

print("Instantiating neural network visualization graph...")
try:
    graph_win = ProjectGraphWindow(root)
    print("Graph window created successfully!")
    
    # Configure the window to terminate the script only when the user manually closes it
    graph_win.protocol("WM_DELETE_WINDOW", lambda: [
        print("User closed the graph window. Completing diagnostics..."),
        graph_win.on_closing(),
        root.destroy()
    ])
    
    print("Graph running. Close the window manually to finish the test.")
    root.mainloop()
    print("====================================================")
    print("              DIAGNOSTIC TEST SUCCESS               ")
    print("====================================================")
except Exception as e:
    print(f"DIAGNOSTIC TEST FAILED: {e}")
    sys.exit(1)
