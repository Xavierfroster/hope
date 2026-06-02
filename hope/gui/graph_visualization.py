import customtkinter as ctk
import tkinter as tk
import math
import random
import threading
import time

class ProjectGraphWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("PROJECT HOPE - Neural Architecture Network")
        self.geometry("800x550")
        self.configure(fg_color="#0A0E17") # Deep cybernetic blue/black
        self.resizable(False, False)

        # Force window on top and grab focus
        self.attributes("-topmost", True)
        self.focus_force()

        # Title Label
        self.title_label = ctk.CTkLabel(
            self, 
            text="PROJECT HOPE: NEURAL ARCHITECTURE NETWORK", 
            font=ctk.CTkFont(family="Consolas", size=18, weight="bold"),
            text_color="#00F6FF" # Cyber Cyan
        )
        self.title_label.pack(pady=(15, 5))

        self.subtitle = ctk.CTkLabel(
            self,
            text="Hover over nodes to inspect modular systems in real-time.",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#8F96A3"
        )
        self.subtitle.pack(pady=(0, 10))

        # Canvas Frame
        self.canvas_frame = ctk.CTkFrame(self, fg_color="#070A0F", border_width=2, border_color="#1F2A3D")
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_frame, 
            bg="#070A0F", 
            highlightthickness=0, 
            width=760, 
            height=430
        )
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

        # Define Nodes in Neural Network
        self.nodes = {
            "core": {"x": 380, "y": 215, "label": "HOPE Core", "color": "#00F6FF", "radius": 24, "desc": "Central orchestrator & fuzzy intent-router. Dispatches user queries to offline modules.", "sector": "Hub"},
            
            # Inputs (Neon Pink)
            "speech": {"x": 140, "y": 70, "label": "Speech Recognition", "color": "#FF007F", "radius": 16, "desc": "Offline speech-to-text transcriber using speech_recognition audio capture.", "sector": "Input"},
            "gui_in": {"x": 140, "y": 160, "label": "GUI Dashboard", "color": "#FF007F", "radius": 16, "desc": "CustomTkinter dashboard visual log console and text execution pane.", "sector": "Input"},
            "camera": {"x": 140, "y": 260, "label": "Camera Vision", "color": "#FF007F", "radius": 16, "desc": "Captures live webcam OpenCV streams for face recognition & vision queries.", "sector": "Input"},
            "screen": {"x": 140, "y": 350, "label": "Screen Capture", "color": "#FF007F", "radius": 16, "desc": "Takes desktop screenshots using PIL to extract math problem details.", "sector": "Input"},
            
            # Core Utilities (Neon Purple)
            "db": {"x": 380, "y": 65, "label": "SQLite Memory DB", "color": "#9D4EDD", "radius": 16, "desc": "Local persistent database storing settings, preferences, and chat logs.", "sector": "Utility"},
            "scheduler": {"x": 380, "y": 365, "label": "System Scheduler", "color": "#9D4EDD", "radius": 16, "desc": "Orchestrates background cron tasks and active pc health monitoring.", "sector": "Utility"},
            
            # Outputs / Features (Neon Green)
            "tts": {"x": 620, "y": 70, "label": "Optimus Prime TTS", "color": "#39FF14", "radius": 16, "desc": "Offline speech synthesizer, utilizing custom DSP, pitch down, & LFO ring modulation.", "sector": "Output"},
            "math": {"x": 620, "y": 160, "label": "Math Solver", "color": "#39FF14", "radius": 16, "desc": "Zero-dependency algebraic/arithmetic solver utilizing the Secant root-finding method.", "sector": "Output"},
            "diagnostics": {"x": 620, "y": 260, "label": "PC Diagnostics", "color": "#39FF14", "radius": 16, "desc": "Checks local hardware status including CPU load, RAM thresholds, and low battery.", "sector": "Output"},
            "security": {"x": 620, "y": 350, "label": "Face Recognition", "color": "#39FF14", "radius": 16, "desc": "Haar-cascade visual recognizer verifying user face identities.", "sector": "Output"}
        }

        # Define Edges (Signal Flow Paths)
        self.edges = [
            ("speech", "core"), ("gui_in", "core"), ("camera", "core"), ("screen", "core"),
            ("core", "db"), ("core", "scheduler"),
            ("core", "tts"), ("core", "math"), ("core", "diagnostics"), ("core", "security")
        ]

        # Real-time Stats State
        self.realtime_data = {
            "cpu": 0, "ram": 0, "logs": 0, "contacts": 0, "voice": "Default SAPI5", "standby": False
        }
        self.particles = []
        self.hovered_node = None
        self.running = True

        # Bind Mouse Interactions
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Draw Base Static Graph Elements
        self.draw_graph()

        # Start Particle Animation, Spawn Loops, and Real-time Stats Thread
        self.animate_loop()
        self.spawn_loop()
        self.start_stats_thread()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_stats_thread(self):
        """Launches a background daemon thread to monitor CPU, RAM, SQLite logs, and speech states dynamically."""
        def run_stats():
            from hope.system_stats import monitor
            import sqlite3
            from hope.configuration import settings as config
            
            while self.running:
                # 1. Read hardware diagnostics
                stats = {"cpu": 0, "ram": 0}
                try:
                    stats = monitor.get_pc_stats()
                except Exception:
                    pass
                
                # 2. Count persistent sqlite logs
                logs_count = 0
                contacts_count = 0
                try:
                    conn = sqlite3.connect(config.DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM history")
                    logs_count = cursor.fetchone()[0]
                    cursor.execute("SELECT COUNT(*) FROM contacts")
                    contacts_count = cursor.fetchone()[0]
                    conn.close()
                except Exception:
                    pass
                
                # 3. Retrieve engine settings
                voice_label = "Default"
                standby = False
                try:
                    from hope.core import engine
                    voice_label = "Optimus Prime" if engine.active_voice_type == "optimus_prime" else "Default"
                    standby = engine.standby_mode
                except Exception:
                    pass
                
                # Update visual state thread-safely
                self.realtime_data = {
                    "cpu": stats.get("cpu", 0),
                    "ram": stats.get("ram", 0),
                    "logs": logs_count,
                    "contacts": contacts_count,
                    "voice": voice_label,
                    "standby": standby
                }
                
                # Triggers label updates on main Tkinter thread
                self.after(0, self.update_canvas_text)
                time.sleep(2.5) # Poll every 2.5 seconds
                
        threading.Thread(target=run_stats, daemon=True).start()

    def update_canvas_text(self):
        """Updates neon dynamic status labels and node glows in real-time."""
        if not self.running or not hasattr(self, "realtime_data"):
            return
            
        data = self.realtime_data
        
        # Core Orchestration
        core_status = "[STANDBY]" if data["standby"] else "[ACTIVE]"
        core_color = "#FF9F1C" if data["standby"] else "#00F6FF" # Amber if Standby, Cyan if Active
        self.canvas.itemconfig("stats_core", text=core_status, fill=core_color)
        self.canvas.itemconfig("core_core", fill=core_color)
        self.canvas.itemconfig("shell_core", outline=core_color)
        self.canvas.itemconfig("node_core", outline=core_color)
        
        # Hardware Diagnostics
        diag_status = f"C:{int(data['cpu'])}% | R:{int(data['ram'])}%"
        diag_color = "#FF0055" if (data['cpu'] > 80 or data['ram'] > 80) else "#39FF14" # Red warning if high load
        self.canvas.itemconfig("stats_diagnostics", text=diag_status, fill=diag_color)
        
        # SQLite database memory
        db_status = f"{data['logs']} logs | {data['contacts']} contacts"
        self.canvas.itemconfig("stats_db", text=db_status, fill="#9D4EDD")
        
        # Optimus Prime Speech Engine
        self.canvas.itemconfig("stats_tts", text=f"({data['voice']})", fill="#39FF14")
        
        # Scheduler
        self.canvas.itemconfig("stats_scheduler", text="[ONLINE]", fill="#9D4EDD")
        
        # Other default ready states
        for nid in ["speech", "gui_in", "camera", "screen", "math", "security"]:
            self.canvas.itemconfig(f"stats_{nid}", text="[READY]", fill="#8F96A3")

    def draw_graph(self):
        """Draws static edges, node layers, and creates tags for real-time text updates."""
        self.canvas.delete("all")

        # 1. Draw connecting lines (edges)
        for start_id, end_id in self.edges:
            n1 = self.nodes[start_id]
            n2 = self.nodes[end_id]
            self.canvas.create_line(
                n1["x"], n1["y"], n2["x"], n2["y"],
                fill="#151E2B", width=2, tags="edge"
            )

        # 2. Draw nodes and label shells
        for node_id, n in self.nodes.items():
            x, y, r, color = n["x"], n["y"], n["radius"], n["color"]
            
            # Glowing shell
            self.canvas.create_oval(
                x - r - 4, y - r - 4, x + r + 4, y + r + 4,
                outline=color, width=1, tags=f"shell_{node_id}"
            )
            
            # Node body
            self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill="#0A0E17", outline=color, width=2, tags=f"node_{node_id}"
            )

            # Center core dot
            self.canvas.create_oval(
                x - 3, y - 3, x + 3, y + 3,
                fill=color, outline="", tags=f"core_{node_id}"
            )

            # Symmetrical text placement
            y_text = y + r + 15 if node_id != "db" else y - r - 15
            y_stats = y_text + 14 if node_id != "db" else y_text - 14
            
            # Main label name
            self.canvas.create_text(
                x, y_text,
                text=n["label"],
                fill="#8F96A3",
                font=("Consolas", 10, "bold"),
                tags=f"label_{node_id}"
            )

            # Real-time secondary status label
            self.canvas.create_text(
                x, y_stats,
                text="[SYNCING]",
                fill="#00F6FF",
                font=("Consolas", 8),
                tags=f"stats_{node_id}"
            )

    def spawn_loop(self):
        """Periodically spawns animated data particles flowing along the edges."""
        if not self.running:
            return

        # Choose a random edge
        start_id, end_id = random.choice(self.edges)
        
        # Determine flow direction based on logic (Inputs -> Hub -> Outputs)
        n_start = self.nodes[start_id]
        n_end = self.nodes[end_id]
        
        self.particles.append({
            "start_x": n_start["x"],
            "start_y": n_start["y"],
            "end_x": n_end["x"],
            "end_y": n_end["y"],
            "progress": 0.0,
            "speed": random.uniform(0.015, 0.03),
            "color": n_start["color"]
        })

        # Schedule next particle spawn in 250 - 500 ms
        self.after(random.randint(250, 500), self.spawn_loop)

    def animate_loop(self):
        """Standard canvas redraw animation loop (renders flowing particles)."""
        if not self.running:
            return

        # Delete old particle drawings
        self.canvas.delete("particle")

        # Update and draw particles
        active_particles = []
        for p in self.particles:
            p["progress"] += p["speed"]
            if p["progress"] < 1.0:
                # Calculate current position coordinates
                x = p["start_x"] + (p["end_x"] - p["start_x"]) * p["progress"]
                y = p["start_y"] + (p["end_y"] - p["start_y"]) * p["progress"]
                
                # Draw neon glowing particle
                self.canvas.create_oval(
                    x - 4, y - 4, x + 4, y + 4,
                    fill=p["color"], outline="", tags="particle"
                )
                active_particles.append(p)
                
        self.particles = active_particles

        # Schedule redraw at ~30 FPS
        self.after(30, self.animate_loop)

    def on_mouse_move(self, event):
        """Listens to mouse coordinates to highlight hovered nodes and display cards."""
        mx, my = event.x, event.y
        new_hover = None

        # Check if cursor is over any node
        for node_id, n in self.nodes.items():
            dist = math.sqrt((n["x"] - mx) ** 2 + (n["y"] - my) ** 2)
            if dist <= n["radius"] + 8:
                new_hover = node_id
                break

        # Redraw tooltips if hovered node changes
        if new_hover != self.hovered_node:
            self.hovered_node = new_hover
            self.canvas.delete("tooltip")
            
            # Restore all node text colors
            for nid in self.nodes:
                self.canvas.itemconfig(f"label_{nid}", fill="#8F96A3")
                self.canvas.itemconfig(f"node_{nid}", width=2)
            
            if self.hovered_node:
                # Highlight active node
                n = self.nodes[self.hovered_node]
                self.canvas.itemconfig(f"label_{self.hovered_node}", fill="#FFFFFF")
                self.canvas.itemconfig(f"node_{self.hovered_node}", width=4)
                
                # Draw glowing info tooltip card
                self.draw_tooltip(n)

    def draw_tooltip(self, n):
        """Draws a beautiful neon futuristic dashboard card explaining the hovered node."""
        # Top level coordinates
        cx, cy = 380, 215 # Middle
        
        # Position card on the opposite side of the hovered node
        card_w, card_h = 290, 120
        card_x = 380 - (card_w // 2)
        card_y = 215 - (card_h // 2)
        
        # Shift card based on hover positions to ensure we don't overlap the hovered node
        if n["x"] < 300:
            card_x = 420
        elif n["x"] > 500:
            card_x = 100
        else:
            # Over db or scheduler
            if n["y"] < 150:
                card_y = 250
            else:
                card_y = 60

        # Draw card body (neon glowing boarder)
        self.canvas.create_rectangle(
            card_x, card_y, card_x + card_w, card_y + card_h,
            fill="#0F1626", outline=n["color"], width=2, tags="tooltip"
        )

        # Header Title (Node Name)
        self.canvas.create_text(
            card_x + 15, card_y + 20,
            anchor="w",
            text=n["label"].upper(),
            fill="#FFFFFF",
            font=("Consolas", 11, "bold"),
            tags="tooltip"
        )

        # Subtitle (System Sector)
        self.canvas.create_text(
            card_x + 15, card_y + 36,
            anchor="w",
            text=f"SYSTEM SECTOR: {n['sector']}",
            fill=n["color"],
            font=("Consolas", 8, "bold"),
            tags="tooltip"
        )

        # Horizontal Divider Line
        self.canvas.create_line(
            card_x + 15, card_y + 48, card_x + card_w - 15, card_y + 48,
            fill="#1E293B", tags="tooltip"
        )

        # Body Description text wrapping
        desc = n["desc"]
        words = desc.split(' ')
        lines = []
        curr_line = ""
        for w in words:
            if len(curr_line + " " + w) < 42:
                curr_line += " " + w
            else:
                lines.append(curr_line.strip())
                curr_line = w
        if curr_line:
            lines.append(curr_line.strip())

        # Render description lines
        y_text = card_y + 64
        for line in lines[:3]: # Cap at 3 lines
            self.canvas.create_text(
                card_x + 15, y_text,
                anchor="w",
                text=line,
                fill="#8F96A3",
                font=("Consolas", 9),
                tags="tooltip"
            )
            y_text += 16

    def on_closing(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    # Test standalone window
    root = ctk.CTk()
    root.geometry("200x200")
    btn = ctk.CTkButton(root, text="Open Graph", command=lambda: ProjectGraphWindow(root))
    btn.pack(pady=50)
    root.mainloop()
