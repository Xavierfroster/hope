import webbrowser
import urllib.parse

def open_youtube():
    webbrowser.open("https://www.youtube.com")

def search_youtube(term):
    query = urllib.parse.quote_plus(term)
    webbrowser.open(f'https://www.youtube.com/results?search_query={query}')

def open_google():
    webbrowser.open("https://www.google.com")

def get_directions(destination, origin=None):
    dest_encoded = urllib.parse.quote_plus(destination)
    if origin:
        orig_encoded = urllib.parse.quote_plus(origin)
        url = f"https://www.google.com/maps/dir/?api=1&origin={orig_encoded}&destination={dest_encoded}"
    else:
        url = f"https://www.google.com/maps/dir/?api=1&destination={dest_encoded}"
    print(f"[MAPS LAUNCH]: Opening {url}")
    webbrowser.open(url, new=2)

def search_map(location):
    loc_encoded = urllib.parse.quote_plus(location)
    url = f"https://www.google.com/maps/search/?api=1&query={loc_encoded}"
    webbrowser.open(url, new=2)

def open_whatsapp_web():
    webbrowser.open("https://web.whatsapp.com")
