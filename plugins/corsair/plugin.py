from typing import List
from core.models import RGBDevice, RGBZone, Color
from plugins.base import RGBPlugin

try:
    import cuesdk
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("[CorsairPlugin] cuesdk not installed. Running in safe mode.")

class CorsairPlugin(RGBPlugin):
    """
    Modular Corsair RGB plugin for K70 and other keyboards.
    Safe: only writes to hardware if `safe_mode=False`.
    """

    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self.devices: List[RGBDevice] = []

        if SDK_AVAILABLE:
            self.sdk = cuesdk.CueSdk()
            self._discover_devices()
        else:
            self.sdk = None
            self._add_mock_device()

    def _add_mock_device(self):
        """Add a fallback mock device for testing."""
        self.devices = [
            RGBDevice(
                id="corsair_k70_mock",
                name="Corsair K70 (mocked)",
                manufacturer="Corsair",
                zones=[RGBZone(id="keyboard_main", led_count=104)]
            )
        ]

    def _discover_devices(self):
        """Safe discovery placeholder; extend to real hardware later."""
        # For now, add a mock device
        self._add_mock_device()
        print("[CorsairPlugin] Safe discovery: mock device added")

    def discover_devices(self) -> List[RGBDevice]:
        print("[CorsairPlugin] Discovering devices...")
        return self.devices

    def set_color(self, device_id: str, zone_id: str, color: Color) -> None:
        """
        Set a solid color for a device zone.
        Writes to hardware only if safe_mode=False.
        """
        print(f"[CorsairPlugin] Device={device_id}, Zone={zone_id}, Color=({color.r}, {color.g}, {color.b})")

        if not self.safe_mode and SDK_AVAILABLE:
            # Here is where per-LED write code will go
            # Example placeholder:
            # self.sdk.set_led_colors(leds, led_colors)
            print("[CorsairPlugin] Safe mode OFF: hardware write would occur here")
