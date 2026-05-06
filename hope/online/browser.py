import webbrowser

def open_youtube():
    webbrowser.open("youtube.com")

def search_youtube(term):
    webbrowser.open(f'https://www.youtube.com/results?search_query={term}')

def open_google():
    webbrowser.open("google.com")

def get_directions(destination):
    url = f"https://www.google.com/maps/dir/?api=1&destination={destination.replace(' ', '+')}"
    webbrowser.open(url)

def search_map(location):
    url = f"https://www.google.com/maps/search/?api=1&query={location.replace(' ', '+')}"
    webbrowser.open(url)

def open_whatsapp_web():
    webbrowser.open("https://web.whatsapp.com")
