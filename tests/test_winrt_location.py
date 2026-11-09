import subprocess
import requests

def get_device_location():
    """Queries Windows Location API via PowerShell."""
    ps_cmd = """
    $code = @"
    using System;
    using System.Threading.Tasks;
    using Windows.Devices.Geolocation;

    public class WinGeo {
        public static string GetLocation() {
            try {
                var g = new Geolocator();
                var task = Task.Run(async () => await g.GetGeopositionAsync());
                if (task.Wait(4000)) {
                    var pos = task.Result.Coordinate.Point.Position;
                    return pos.Latitude + "," + pos.Longitude;
                }
            } catch (Exception ex) {
                return "ERR: " + ex.Message;
            }
            return "TIMEOUT";
        }
    }
"@
    try {
        Add-Type -TypeDefinition $code -Language CSharp
        [WinGeo]::GetLocation()
    } catch {
        Write-Output "FAIL: $_"
    }
    """
    try:
        res = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=8)
        out = res.stdout.strip()
        print("Device Location Raw Output:", out)
        if out and "," in out and not out.startswith("ERR") and not out.startswith("FAIL") and not out.startswith("TIMEOUT"):
            parts = out.split(",")
            lat, lon = float(parts[0]), float(parts[1])
            rev_url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            headers = {'User-Agent': 'HOPE-Assistant/1.0'}
            rev_res = requests.get(rev_url, headers=headers, timeout=5).json()
            display_name = rev_res.get('display_name', 'Device Pinpoint Location')
            name_parts = display_name.split(',')
            readable = f"{name_parts[0]}, {name_parts[1] if len(name_parts) > 1 else ''}".strip()
            return lat, lon, readable
    except Exception as e:
        print("Device Location Exception:", e)
    return None

if __name__ == "__main__":
    print("Result:", get_device_location())
