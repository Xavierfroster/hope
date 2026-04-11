<div align="center">
  <h1>✨ Project HOPE ✨</h1>
  <p><b>Human-Oriented Personal Engine</b></p>
  <p><i>Your fully local, zero-API desktop bestie. No LLMs, no subscriptions, just immaculate pure Python vibes. 🐍💅</i></p>
</div>

---

## 🚀 What is HOPE? 
Sick of paying for API keys? Tired of big tech AI models harvesting your data? **HOPE** (Human-Oriented Personal Engine) is living rent-free in your terminal entirely offline. She’s a heavily customizable desktop voice assistant completely written in pure Python. No cloud, no lag, no cap. 🧢

Instead of relying on ChatGPT or expensive backend LLMs, HOPE actually *learns* from you locally. You can personally teach her your slang, assign command aliases on the fly, and automate your workflow with zero internet dependence. 

## 🌶️ Features That Slap
* **🧠 Real-Time Memory & Learning:** You can natively teach HOPE new conversational responses and command aliases directly through your voice. (Try saying: *"Hope, learn that 'who is' means 'tell me about'"*)
* **💬 Empathy Engine:** Bad day? HOPE catches sad or hyped keywords and matches your energy. 
* **🎛️ PC Automation Level 9000:** Full system control. Mute/unmute, crank the volume, open Google, close apps, or blast your local mp3 playlists without touching the keyboard.
* **🕵️‍♀️ Zero Cloud/API Keys:** Your data stays exactly where it belongs—on your hard drive.
* **📸 Offline Computer Vision Base:** Primed and prepped for facial/object recognition utilizing OpenCV (Camera feed opens instantly on command).
* **🌐 Web Surfing:** She searches YouTube and scrapes Wikipedia summaries naturally.

## 🔥 How To Get Her Running
You're gonna need a couple of libraries because HOPE hooks into the entire OS. 

1. **Clone the repo** and step into the directory:
   ```bash
   git clone https://github.com/YourUsername/Project-HOPE.git
   cd Project-HOPE
   ```
2. **Install the drip (dependencies):**
   ```bash
   pip install pyttsx3 SpeechRecognition pyautogui wikipedia opencv-python pyaudio
   ```
   *(Note: If you run into issues with `pyaudio` on Windows, you might need to install the wheel directly).*

3. **Wake Her Up:**
   ```bash
   python main.py
   ```
   *She'll boot up, verify your internet connection, introduce herself, and start listening!*

## 🗣️ How to talk to HOPE
She uses a **strict Wake Word**, so you gotta address her properly. Always start your sentence with `"Hope"` or `"Hey Hope"`.

**Try these out:**
* *"Hey Hope, volume up"* 🔊
* *"Hope, open Youtube"* 🎥
* *"Hope, tell me about Black Holes"* 🌌
* *"Hope, enable vision"* 👁️
* *"Hope, what was my last command?"* 🔁 (Tests her running memory list)
* *"Hey Hope, wrap it up"* ✌️ (Graceful shutdown)

---
<div align="center">
  <sub>Built with ❤️ and purely unhinged Python architecture.</sub>
</div>
