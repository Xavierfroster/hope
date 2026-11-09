import requests
from hope.core import memory

def get_multiple_locations(address):
    """Geocodes an address and returns up to 5 possible locations."""
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={address.replace(' ', '+')}&format=json&limit=5"
        headers = {'User-Agent': 'HOPE-Assistant/1.0'}
        response = requests.get(url, headers=headers, timeout=5)
        data = response.json()
        results = []
        for item in data:
            results.append({
                'display_name': item['display_name'],
                'lat': float(item['lat']),
                'lon': float(item['lon'])
            })
        return results
    except Exception as e:
        print(f"Geocoding error: {e}")
    return []

def set_user_location(location_str):
    """Saves preferred user starting location to database memory."""
    locs = get_multiple_locations(location_str)
    if locs:
        memory.set_preference("user_location", location_str)
        readable = locs[0]['display_name'].split(',')[0]
        return locs[0]['lat'], locs[0]['lon'], readable
    return None

import subprocess

def show_location_notification(title="Project HOPE - Location Service", message="Location Services Active: Accessing device location to pinpoint coordinates."):
    """Displays a native Windows System Tray / Toast Notification when location access is active."""
    ps_cmd = f"""
    [void] [System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms')
    $notify = New-Object System.Windows.Forms.NotifyIcon
    $notify.Icon = [System.Drawing.SystemIcons]::Information
    $notify.BalloonTipTitle = '{title}'
    $notify.BalloonTipText = '{message}'
    $notify.Visible = $true
    $notify.ShowBalloonTip(4000)
    Start-Sleep -Seconds 1
    """
    try:
        subprocess.Popen(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        print(f"Notification error: {e}")

def get_current_location():
    """Gets current location (lat, lon, name). Triggers Windows System Notification, checks saved preference first, falls back to IP geolocation."""
    # Trigger native Windows System notification
    show_location_notification()

    # 1. Check saved custom location in database
    custom_loc = memory.get_preference("user_location")
    if custom_loc:
        locs = get_multiple_locations(custom_loc)
        if locs:
            name_parts = locs[0]['display_name'].split(',')
            readable_name = f"{name_parts[0]}, {name_parts[1] if len(name_parts) > 1 else ''}".strip()
            return locs[0]['lat'], locs[0]['lon'], readable_name

    # 2. Fallback to IP Geolocation
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['city']
    except Exception as e:
        print(f"IP Location error: {e}")
    return None

def get_route_info(start_coords, end_coords, mode="driving"):
    """Gets distance and duration for the fastest route between two points using OSRM with alternatives."""
    try:
        # OSRM format is lon,lat;lon,lat
        # Request alternatives=true to get candidate routes and select the fastest by minimum duration
        url = f"http://router.project-osrm.org/route/v1/{mode}/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=false&alternatives=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data.get('code') == 'Ok' and data.get('routes'):
            # Select the route with minimum duration (fastest route)
            fastest_route = min(data['routes'], key=lambda r: r['duration'])
            distance_km = fastest_route['distance'] / 1000.0
            duration_mins = fastest_route['duration'] / 60.0
            return round(distance_km, 2), round(duration_mins)
    except Exception as e:
        print(f"Routing error: {e}")
    return None

