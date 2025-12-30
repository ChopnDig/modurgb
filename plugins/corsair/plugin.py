# corsain plugin, currently parked as sdk is incompatible with icue current version
from typing import List
from core.models import RGBDevice, RGBZone, Color
from plugins.base import RGBPlugin

try:
    from cuesdk import CueSdk, CorsairDeviceFilter, CorsairDeviceType, CorsairError
    from cuesdk.structs import CorsairLedColor
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("[CorsairPlugin] cuesdk not installed. Running in safe mode.")

class CorsairPlugin(RGBPlugin):
    """
    Corsair RGB plugin for K70 using cue-sdk-python 4.0.84.
    safe_mode=True logs only, safe_mode=False writes to keyboard.
    """

    def __init__(self, safe_mode: bool = True):
        self.safe_mode = safe_mode
        self.devices: List[RGBDevice] = []
        self._device_led_ids = {}  # device_id -> list of led IDs

        if SDK_AVAILABLE:
            self.sdk = CueSdk()
            self._discover_devices()
        else:
            self.sdk = None
            self._add_mock_device()

    def _add_mock_device(self):
        self.devices = [
            RGBDevice(
                id="corsair_k70_mock",
                name="Corsair K70 (mocked)",
                manufacturer="Corsair",
                zones=[RGBZone(id="keyboard_main", led_count=104)]
            )
        ]
        self._device_led_ids["corsair_k70_mock"] = list(range(104))

    def _discover_devices(self):
        if not SDK_AVAILABLE or self.safe_mode:
            self._add_mock_device()
            print("[CorsairPlugin] Safe discovery: mock device added")
            return

        devices, err = self.sdk.get_devices(
            CorsairDeviceFilter(device_type_mask=CorsairDeviceType.CDT_Keyboard)
        )
        if err != CorsairError.CE_Success or not devices:
            print("[CorsairPlugin] No Corsair keyboards found, adding mock device")
            self._add_mock_device()
            return

        for device in devices:
            info = self.sdk.get_device_info(device.device_id)
            leds, err_leds = self.sdk.get_leds(device.device_id)
            if err_leds != CorsairError.CE_Success:
                continue

            device_key = f"corsair_{device.device_id}"
            self.devices.append(
                RGBDevice(
                    id=device_key,
                    name=info.model,
                    manufacturer="Corsair",
                    zones=[RGBZone(id="keyboard_main", led_count=len(leds))]
                )
            )
            self._device_led_ids[device_key] = [led.led_id for led in leds]

        print(f"[CorsairPlugin] Discovered {len(self.devices)} device(s)")

    def discover_devices(self) -> List[RGBDevice]:
        print("[CorsairPlugin] Discovering devices...")
        return self.devices

    def set_color(self, device_id: str, zone_id: str, color: Color) -> None:
        print(f"[CorsairPlugin] Device={device_id}, Zone={zone_id}, Color=({color.r}, {color.g}, {color.b})")

        if not self.safe_mode and SDK_AVAILABLE:
            led_ids = self._device_led_ids.get(device_id, [])
            if not led_ids:
                print(f"[CorsairPlugin] No LEDs found for device {device_id}")
                return

            # Build LED colors with full brightness (a=255)
            led_colors = [CorsairLedColor(led_id, color.r, color.g, color.b, 255) for led_id in led_ids]

            # New API: set_led_colors_buffer writes immediately; no flush needed
            self.sdk.set_led_colors_buffer(device_id=device_id, led_colors=led_colors)
            print("[CorsairPlugin] Color written to keyboard")
