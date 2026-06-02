import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import threading
from hope.system_stats import monitor as diagnostics
import queue
import os

class HopeGUI(ctk.CTk):
    def __init__(self, process_query_callback):
        super().__init__()

        self.process_query_callback = process_query_callback
        self.title("PROJECT HOPE - System Dashboard")
        self.geometry("1000x600")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Layout Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar (Diagnostics) ---
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="HOPE v2.5", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(pady=20)

        # CPU
        self.cpu_label = ctk.CTkLabel(self.sidebar, text="CPU: 0%")
        self.cpu_label.pack(pady=(10, 0))
        self.cpu_bar = ctk.CTkProgressBar(self.sidebar)
        self.cpu_bar.pack(pady=5, padx=10)
        
        # RAM
        self.ram_label = ctk.CTkLabel(self.sidebar, text="RAM: 0%")
        self.ram_label.pack(pady=(10, 0))
        self.ram_bar = ctk.CTkProgressBar(self.sidebar)
        self.ram_bar.pack(pady=5, padx=10)

        # Disk
        self.disk_label = ctk.CTkLabel(self.sidebar, text="Disk: 0%")
        self.disk_label.pack(pady=(10, 0))
        self.disk_bar = ctk.CTkProgressBar(self.sidebar)
        self.disk_bar.pack(pady=5, padx=10)

        # Battery
        self.battery_label = ctk.CTkLabel(self.sidebar, text="Battery: 0%")
        self.battery_label.pack(pady=(20, 0))

        # --- Voice Settings ---
        self.voice_label = ctk.CTkLabel(self.sidebar, text="Voice Settings", font=ctk.CTkFont(size=13, weight="bold"))
        self.voice_label.pack(pady=(30, 5))
        
        # Dynamically import engine to retrieve baseline active voice
        import hope.core.engine as engine
        initial_val = "Optimus Prime" if engine.active_voice_type == "optimus_prime" else "Default Voice"
        
        self.voice_menu = ctk.CTkOptionMenu(
            self.sidebar, 
            values=["Default Voice", "Optimus Prime"],
            command=self.change_voice_mode
        )
        self.voice_menu.set(initial_val)
        self.voice_menu.pack(pady=5, padx=15)

        # --- Main View (Vision) ---
        self.vision_frame = ctk.CTkFrame(self, corner_radius=10)
        self.vision_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.vision_label = ctk.CTkLabel(self.vision_frame, text="") # Video feed goes here
        self.vision_label.pack(expand=True, fill="both")

        # --- Bottom Area (Chat Log & Input) ---
        self.log_frame = ctk.CTkFrame(self, height=150)
        self.log_frame.grid(row=1, column=1, padx=20, pady=(0, 20), sticky="nsew")
        
        self.log_text = ctk.CTkTextbox(self.log_frame, state="disabled", font=("Consolas", 12))
        self.log_text.pack(expand=True, fill="both", padx=10, pady=10)
        
        self.input_frame = ctk.CTkFrame(self.log_frame, height=40, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.query_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type command here...")
        self.query_entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
        self.query_entry.bind("<Return>", lambda e: self.send_query())
        
        self.send_btn = ctk.CTkButton(self.input_frame, text="Execute", width=80, command=self.send_query)
        self.send_btn.pack(side="right")

        # State
        self.cap = None
        self.running = True
        self.log_queue = queue.Queue()

        # Start Update Loops
        self.start_vision_loop()
        self.start_diagnostics_loop()
        self.check_log_queue()

    def add_log(self, message):
        self.log_queue.put(message)

    def check_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"{msg}\n")
            self.log_text.see("end")
            self.log_text.configure(state="disabled")
        self.after(100, self.check_log_queue)

    def show_architecture_graph(self):
        """Displays the neural architecture network graph pop-up window."""
        try:
            from hope.gui.graph_visualization import ProjectGraphWindow
            graph_win = ProjectGraphWindow(self)
            self.add_log("System: Visualizing Neural Architecture Graph.")
        except Exception as e:
            print(f"Error opening architecture graph window: {e}")

    def send_query(self):
        query = self.query_entry.get()
        if query:
            self.query_entry.delete(0, "end")
            self.add_log(f"> {query}")
            threading.Thread(target=self.process_query_callback, args=(query,), daemon=True).start()

    def change_voice_mode(self, val):
        import hope.core.engine as engine
        voice_type = "optimus_prime" if val == "Optimus Prime" else "default"
        if engine.update_voice_type(voice_type):
            self.add_log(f"System: Voice Mode changed to {val}")

    def start_diagnostics_loop(self):
        def update():
            while self.running:
                stats = diagnostics.get_pc_stats()
                # Update UI elements in main thread
                self.after(0, self.update_stats_ui, stats)
                threading.Event().wait(2)
        
        threading.Thread(target=update, daemon=True).start()

    def update_stats_ui(self, stats):
        self.cpu_label.configure(text=f"CPU: {stats['cpu']}%")
        self.cpu_bar.set(stats['cpu'] / 100)
        
        self.ram_label.configure(text=f"RAM: {stats['ram']}%")
        self.ram_bar.set(stats['ram'] / 100)
        
        self.disk_label.configure(text=f"Disk: {stats['disk']}%")
        self.disk_bar.set(stats['disk'] / 100)
        
        self.battery_label.configure(text=f"Battery: {stats['battery']}% {'(Plugged)' if stats['plugged'] else ''}")

    def start_vision_loop(self):
        self.cap = cv2.VideoCapture(0)
        self.running_live_feed = True
        def update():
            while self.running:
                if self.running_live_feed:
                    ret, frame = self.cap.read()
                    if ret:
                        # Convert to RGB for PIL
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        # Resize to fit frame
                        img = Image.fromarray(frame)
                        img = img.resize((600, 400))
                        ctk_img = ctk.CTkImage(img, size=(600, 400))
                        self.after(0, lambda: self.vision_label.configure(image=ctk_img))
                threading.Event().wait(0.03) # ~30 FPS
        
        threading.Thread(target=update, daemon=True).start()

    def display_captured_image(self, image_path, problems):
        """Pauses live camera feed, draws solved mathematical equations on the image, and displays it in the GUI."""
        try:
            img = Image.open(image_path)
            # Resize image to match vision label dimensions for crisp drawing
            img = img.resize((600, 400))
            
            from PIL import ImageDraw
            draw = ImageDraw.Draw(img)
            y_offset = 20
            
            for p in problems:
                text = f"SOLVED: {p['problem']} -> {p['solution']}"
                # Render a semi-transparent black background strip for absolute text readability
                draw.rectangle([10, y_offset - 2, 590, y_offset + 25], fill="black")
                draw.text((18, y_offset + 3), text, fill="green")
                y_offset += 38
            
            ctk_img = ctk.CTkImage(img, size=(600, 400))
            self.running_live_feed = False
            self.after(0, lambda: self.vision_label.configure(image=ctk_img))
            
            # Resume live camera feed automatically after 8 seconds
            self.after(8000, self.resume_live_feed)
        except Exception as e:
            print(f"Error displaying captured image in GUI: {e}")
            self.running_live_feed = True

    def resume_live_feed(self):
        """Resumes live webcam feed updating."""
        self.running_live_feed = True

    def on_closing(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.after(0, self.destroy)
        os._exit(0)

if __name__ == "__main__":
    app = HopeGUI(print) # Test with print
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
