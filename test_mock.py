from core.models import Color
from plugins.mock.plugin import MockPlugin

def main():
    plugin = MockPlugin()
    devices = plugin.discover_devices()
    for device in devices:
        for zone in device.zones:
            plugin.set_color(device.id, zone.id, Color(255, 0, 0))

if __name__ == "__main__":
    main()
