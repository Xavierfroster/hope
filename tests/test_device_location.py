import subprocess
import requests

def get_windows_device_location():
    """Attempts to get exact location from Windows System.Device.Location API via PowerShell."""
    ps_cmd = """
    Add-Type -Assembly System.Device
    $watcher = New-Object System.Device.Location.GeoCoordinateWatcher
    $watcher.Start()
    $timeout = 0
    while (($watcher.Status -ne 'Ready') -and ($watcher.Permission -ne 'Denied') -and ($timeout -lt 25)) {
        Start-Sleep -Milliseconds 100
        $timeout++
    }
    if ($watcher.Permission -eq 'Denied') {
        Write-Output "DENIED"
    } elseif ($watcher.Status -eq 'Ready') {
        $loc = $watcher.Position.Location
        Write-Output "$($loc.Latitude),$($loc.Longitude)"
    } else {
        Write-Output "TIMEOUT"
    }
    """
    try:
        res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=5)
        out = res.stdout.strip()
        if out and out not in ["DENIED", "TIMEOUT"] and "," in out:
            parts = out.split(",")
            lat, lon = float(parts[0]), float(parts[1])
            if lat != 0 and lon != 0:
                # Reverse geocode to get city / readable name
                rev_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
                headers = {'User-Agent': 'HOPE-Assistant/1.0'}
                rev_res = requests.get(rev_url, headers=headers, timeout=5).json()
                display_name = rev_res.get('display_name', 'Current Device Location')
                name_parts = display_name.split(',')
                readable = f"{name_parts[0]}, {name_parts[1] if len(name_parts) > 1 else ''}".strip()
                return lat, lon, readable
    except Exception as e:
        print(f"Windows Location error: {e}")
    return None

if __name__ == "__main__":
    loc = get_windows_device_location()
    print("Device location:", loc)
