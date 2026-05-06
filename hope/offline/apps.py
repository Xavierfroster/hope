import os
import pyautogui

def minimise_windows():
    pyautogui.hotkey('win', 'd')

def open_code():
    codePath = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
    if os.path.exists(codePath):
        os.startfile(codePath)
        return True
    return False

def play_music():
    music_dir = 'E:\\Songs'
    if os.path.exists(music_dir):
        songs = os.listdir(music_dir)
        if songs:
            os.startfile(os.path.join(music_dir, songs[0]))
            return songs[0]
    return None

def change_volume(direction):
    key = 'volumeup' if direction == "up" else 'volumedown'
    for _ in range(5):
        pyautogui.press(key)

def mute_volume():
    pyautogui.press('volumemute')
