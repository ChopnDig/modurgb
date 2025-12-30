from typing import List
from core.models import RGBDevice, RGBZone, Color
from plugins.base import RGBPlugin

class MockPlugin(RGBPlugin):
    """
    A mock RGB plugin for testing the core system without hardware.
    """

    def __init__(self):
        # Predefine a mock device with one zone
        self.mock_devices = [
            RGBDevice(
                id="mock_keyboard_01",
                name="Mock Keyboard",
                manufacturer="Mock Inc.",
                zones=[RGBZone(id="keyboard_main", led_count=104)]
            )
        ]

    def discover_devices(self) -> List[RGBDevice]:
        print("[MockPlugin] Discovering devices...")
        return self.mock_devices

    def set_color(self, device_id: str, zone_id: str, color: Color) -> None:
        print(
            f"[MockPlugin] Set color called: Device={device_id}, "
            f"Zone={zone_id}, Color=({color.r}, {color.g}, {color.b})"
        )
