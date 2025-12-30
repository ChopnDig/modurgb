from core.models import Color
from plugins.corsair.plugin import CorsairPlugin

def main():
    plugin = CorsairPlugin(safe_mode=False)  # Set False to light K70
    devices = plugin.discover_devices()

    for device in devices:
        for zone in device.zones:
            plugin.set_color(device.id, zone.id, Color(0, 255, 0))  # Green

if __name__ == "__main__":
    main()
