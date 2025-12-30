from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Color:
    """Represents an RGB color."""
    r: int
    g: int
    b: int

@dataclass(frozen=True)
class RGBZone:
    """Represents a logical LED zone on a device."""
    id: str
    led_count: int

@dataclass(frozen=True)
class RGBDevice:
    """Represents a physical RGB device."""
    id: str
    name: str
    manufacturer: str
    zones: List[RGBZone]
