
from typing import List, TypedDict

from utils.functions import read_config

# Default configuration values
DEFAULT_CONFIG = {
    "layout": {
        "left": ["workspaces", "windowtitle"],
        "middle": ["datetime", "player"],
        "right": ["weather", "battery","system_tray", "updates", "hypridle", "hyprsunset"]
    },
    "hyprsunset": {
        "temperature": "2800k",
        "enabled_icon": "󱩌",
        "disabled_icon": "󰛨",
        "icon_size": "12px",
        "enable_label": False,
        "enable_tooltip": True
    },
    "hypridle": {
        "enabled_icon": "",
        "disabled_icon": "",
        "icon_size": "12px",
        "enable_label": False,
         "enable_tooltip": True
    },
    "battery": {
        "enable_label": True,
        "enable_tooltip": True,
        "interval": 2000
    },
    "cpu": {
        "icon": "",
        "icon_size": "12px",
        "enable_label": False,
        "enable_tooltip": True,
        "interval": 2000
    },
    "memory": {
        "icon": "",
        "icon_size": "12px",
        "enable_label": False,
        "enable_tooltip": True,
        "interval": 2000
    },
    "storage": {
        "icon": "󰋊",
        "icon_size": "14px",
        "enable_label": False,
        "enable_tooltip": True,
        "interval": 2000
    },
    "workspaces": {
        "count": 8,
        "occupied": True
    },
    "window": {
        "length": 20,
        "enable_icon": True
    },
    "updates": {
        "os": "arch",
        "icon": "󱧘",
        "icon_size": "14px"
    },
    "weather": {
        "location": "Kathmandu"
    }
}








# Define the TypedDict types for various configurations

class BaseConfig(TypedDict):
    """Common configuration for some sections"""
    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int

# Layout configuration for different sections of the bar
class Layout(TypedDict):
    """Configuration for Window"""

    left: List[str]
    middle: List[str]
    right: List[str]


# Configuration for HyprSunset
class HyprSunset(TypedDict,BaseConfig):
    """Configuration for Window"""

    temperature: str
    enabled_icon: str
    disabled_icon: str



# Configuration for HyprIdle
class HyprIdle(TypedDict,BaseConfig):
    """Configuration for hypridle"""

    enabled_icon: str
    disabled_icon: str



# Configuration for Battery
class Battery(TypedDict):
    """Configuration for battery"""

    enable_label: bool
    enable_tooltip: bool
    interval: int


# Configuration for CPU
class Cpu(TypedDict,BaseConfig):
    """Configuration for Cpu"""

    icon: str


# Configuration for Memory
class Memory(TypedDict, BaseConfig):
    """Configuration for window"""

    icon: str



# Configuration for Storage
class Storage(TypedDict, BaseConfig):
    """Configuration for storage"""

    icon: str



# Configuration for Workspaces
class Workspaces(TypedDict):
    """Configuration for Workspaces"""

    count: int


# Configuration for Window
class WindowTitle(TypedDict):
    """Configuration for Window"""

    length: int
    enable_icon: bool


# Configuration for Updates
class Updates(TypedDict,BaseConfig):
    """Configuration for Updates"""
    os: str
    icon: str



# Configuration for Weather
class Weather(TypedDict):
    """Configuration for weather"""

    location: str
    interval: int
    enable_tooltip: bool
    enable_label: bool


# Main configuration that includes all other configurations
class Config(TypedDict):
    """Main configuration"""

    layout: Layout
    hyprsunset: HyprSunset
    hypridle: HyprIdle
    battery: Battery
    cpu: Cpu
    memory: Memory
    storage: Storage
    workspaces: Workspaces
    window: WindowTitle
    updates: Updates
    weather: Weather


# Read the configuration from the JSON file
parsed_data = read_config()


# Merge the parsed data with the default configuration
def merge_defaults(data: dict, defaults: dict):
    return {**defaults, **data}


# Now, `parsed_data` is a Python dictionary
# You can access individual items like this:
layout = parsed_data["layout"]

for key, value in parsed_data.items():
    if key in DEFAULT_CONFIG:
        parsed_data[key] = merge_defaults(value, DEFAULT_CONFIG[key])


# Optionally, cast the parsed data to match our TypedDict using type hints
config: Config = parsed_data
