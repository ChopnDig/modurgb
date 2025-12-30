from abc import ABC, abstractmethod
from typing import List
from core.models import RGBDevice, Color

class RGBPlugin(ABC):
    """
    Base interface for all RGB device plugins.
    All plugins must inherit from this class and implement its methods.
    """

    @abstractmethod
    def discover_devices(self) -> List[RGBDevice]:
        """
        Discover all devices this plugin can control.

        Returns:
            List[RGBDevice]: Devices found by this plugin.
        """
        pass

    @abstractmethod
    def set_color(self, device_id: str, zone_id: str, color: Color) -> None:
        """
        Set a solid color on a device's zone.

        Args:
            device_id (str): The unique ID of the device.
            zone_id (str): The unique ID of the zone within the device.
            color (Color): The color to set.
        """
        pass
