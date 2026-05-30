import requests

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

def get_current_location():
    """Gets current location (lat, lon) based on IP address."""
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data['status'] == 'success':
            return data['lat'], data['lon'], data['city']
    except Exception as e:
        print(f"IP Location error: {e}")
    return None

def get_route_info(start_coords, end_coords):
    """Gets distance and duration between two points using OSRM."""
    try:
        # OSRM format is lon,lat;lon,lat
        url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=false"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data['code'] == 'Ok':
            route = data['routes'][0]
            distance_km = route['distance'] / 1000.0
            duration_mins = route['duration'] / 60.0
            return round(distance_km, 2), round(duration_mins)
    except Exception as e:
        print(f"Routing error: {e}")
    return None
