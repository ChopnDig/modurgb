from core.models import Color
from plugins.corsair.plugin import CorsairPlugin

def main():
    # safe_mode=True logs only
    plugin = CorsairPlugin(safe_mode=True)
    devices = plugin.discover_devices()

    for device in devices:
        for zone in device.zones:
            plugin.set_color(device.id, zone.id, Color(0, 255, 0))

if __name__ == "__main__":
    main()
