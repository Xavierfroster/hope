<div align="center">
  <h1>✨ Project HOPE ✨</h1>
  <p><b>Human-Oriented Personal Engine</b></p>
  <p><i>Your fully local, zero-API desktop bestie. No LLMs, no subscriptions, just pure Python logic. 🐍💅</i></p>

  <img src="https://img.shields.io/badge/Phase-2.5%20%2F%205-blueviolet?style=for-the-badge" alt="Phase 2.5/5">
  <img src="https://img.shields.io/badge/Completion-~55%25-green?style=for-the-badge" alt="Completion 55%">
</div>

---

## 🚀 What is HOPE? 
**HOPE** (Human-Oriented Personal Engine) is a heavily customizable desktop voice assistant written entirely in pure Python. No cloud, no lag, no data harvesting. 🧢

Instead of relying on expensive backend LLMs, HOPE *learns* from you locally. You can teach her your slang, assign command aliases on the fly, and automate your workflow with zero internet dependence. She features a unique **Cynical Personality Engine**, making her interactions more human (and slightly judgmental).

## 🧠 Current Progress: Phase 2.5
We have successfully established the core engine and the personality layer. Phase 3 (System Control) is partially integrated, while Phase 4 (Vision) and Phase 5 (Advanced Intelligence) are under active development.

### ✅ Completed Features
*   **🎙️ Core Interaction (Phase 1)**
    *   **Strict Wake Word**: Responds to "Hope" or "Hey Hope".
    *   **Speech-to-Text**: High-accuracy transcription via Google Recognition API.
    *   **Natural Response**: Time-aware greetings and text-to-speech output.
    *   **Short-Term Memory**: Tracks the last 10 commands natively.
*   **🎭 Personality & Learning (Phase 2)**
    *   **Cynical Engine**: A sassy, judging tone with adjustable humor levels (1-10).
    *   **Empathy Toggle**: Switch between "Cynical" and "Nice" modes on command.
    *   **Phrase Learning**: Teach specific responses (e.g., *"learn that when I say hello respond with hi there"*).
    *   **Command Aliasing**: Map complex phrases to simple ones.
    *   **SQLite Integration**: Long-term memory storage for user preferences and learned data.
*   **🌐 Automation & Web (Phase 3)**
    *   **System Control**: Volume management, window minimization, and app closing.
    *   **Web Tools**: Instant access to Google, YouTube, and Wikipedia summaries.
    *   **Tool Launching**: Quick-launch apps like VS Code.

## 🛠️ In-Process & Upcoming
*   **📸 Vision System (Phase 4)**: Basic camera integration is live. Advanced face recognition and object detection are in progress.
*   **📅 Task Scheduling**: Implementing a custom `cron`-like system for reminders and automation.
*   **📚 Knowledge Base**: Integrating local PDF extraction into the real-time query engine.

## 🔥 How To Get Her Running
HOPE hooks directly into your OS, so you'll need a few dependencies.

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/Xavierfroster/hope.git
    cd hope
    ```
2.  **Install the dependencies**:
    ```bash
    pip install pyttsx3 SpeechRecognition pyautogui wikipedia opencv-python pyaudio
    ```
    *(Note: If you encounter issues with `pyaudio` on Windows, consider installing the appropriate wheel file).*

3.  **Wake Her Up**:
    ```bash
    python main.py
    ```

## 🗣️ Talking to HOPE
Always address her by name. Try these commands:
*   *"Hope, set humor level to 10"* (Crank up the sass) 🌶️
*   *"Hope, switch to empathy mode"* (Make her nice again) ✨
*   *"Hope, learn that [phrase] means [action]"* 🧠
*   *"Hey Hope, volume up"* 🔊
*   *"Hope, open vision"* 👁️

---

## 🚀 Future Roadmap
1.  **Advanced Pattern Matching**: Fuzzy string matching for more resilient command recognition.
2.  **Dynamic GUI**: A minimalist dashboard for status visualization and vision feeds.
3.  **Smart Home Integration**: Plugins for IoT device control.
4.  **Active Learning**: Automatic refinement of command understanding through user feedback.

<div align="center">
  <sub>Built with ❤️ and purely unhinged Python architecture.</sub>
</div>

