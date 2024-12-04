from typing import List, TypedDict

from utils.functions import read_config

# Default configuration values
DEFAULT_CONFIG = {
    "layout": {
        "left": ["workspaces", "window_title"],
        "middle": ["datetime", "player"],
        "right": [
            "weather",
            "battery",
            "system_tray",
            "updates",
            "hypr_idle",
            "hypr_sunset",
        ],
    },
    "hypr_sunset": {
        "temperature": "2800k",
        "enabled_icon": "󱩌",
        "disabled_icon": "󰛨",
        "icon_size": "12px",
        "enable_label": True,
        "enable_tooltip": True,
    },
    "hypr_idle": {
        "enabled_icon": "",
        "disabled_icon": "",
        "icon_size": "12px",
        "enable_label": True,
        "enable_tooltip": True,
    },
    "battery": {
        "enable_label": True,
        "enable_tooltip": True,
        "interval": 2000,
        "hide_label_when_full": True,
    },
    "cpu": {
        "icon": "",
        "icon_size": "12px",
        "enable_label": True,
        "enable_tooltip": True,
        "interval": 2000,
    },
    "memory": {
        "icon": "",
        "icon_size": "12px",
        "enable_label": True,
        "enable_tooltip": True,
        "interval": 2000,
    },
    "storage": {
        "icon": "󰋊",
        "icon_size": "14px",
        "enable_label": True,
        "enable_tooltip": True,
        "interval": 2000,
    },
    "workspaces": {"count": 8, "occupied": True},
    "window_title": {"length": 20, "enable_icon": True},
    "updates": {
        "os": "arch",
        "icon": "󱧘",
        "interval": 20000,
        "icon_size": "14px",
        "enable_tooltip": True,
        "enable_label": True,
    },
    "weather": {
        "location": "Kathmandu",
        "interval": 20000,
        "enable_tooltip": True,
        "enable_label": True,
    },
    "keyboard": {
        "icon": "󰌌",
        "icon_size": "14px",
        "enable_label": True,
        "enable_tooltip": True,
    },
    "player": {
        "length": 30,
        "enable_tooltip": True,
    },
    "language": {"length": 3},
    "task_bar": {"icon_size": 22},
}


class BaseConfig(TypedDict):
    """Common configuration for some sections"""

    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


class Layout(TypedDict):
    """ayout configuration for different sections of the bar"""

    left: List[str]
    middle: List[str]
    right: List[str]


class HyprSunset(TypedDict, BaseConfig):
    """Configuration for hyprsunset"""

    temperature: str
    enabled_icon: str
    disabled_icon: str


class TaskBar(TypedDict):
    """Configuration for taskbar"""

    icon_size: int


class HyprIdle(TypedDict, BaseConfig):
    """Configuration for hypridle"""

    enabled_icon: str
    disabled_icon: str


class Battery(TypedDict):
    """Configuration for battery"""

    enable_label: bool
    enable_tooltip: bool
    hide_label_when_full: bool
    interval: int


class Cpu(TypedDict, BaseConfig):
    """Configuration for Cpu"""

    icon: str


class Player(TypedDict, BaseConfig):
    """Configuration for bar player"""

    length: int


class Memory(TypedDict, BaseConfig):
    """Configuration for window"""

    icon: str


class Storage(TypedDict, BaseConfig):
    """Configuration for storage"""

    icon: str


class Workspaces(TypedDict):
    """Configuration for Workspaces"""

    count: int
    occupied: bool


class WindowTitle(TypedDict):
    """Configuration for Window"""

    length: int
    enable_icon: bool


class Updates(TypedDict, BaseConfig):
    """Configuration for updates"""

    os: str
    icon: str


class Weather(TypedDict):
    """Configuration for weather"""

    location: str
    interval: int
    enable_tooltip: bool
    enable_label: bool


class Keyboard(TypedDict, BaseConfig):
    """Configuration for keyboard"""

    icon: str


class Language(TypedDict):
    """Configuration for language"""

    length: int


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    layout: Layout
    hypr_sunset: HyprSunset
    hypr_idle: HyprIdle
    battery: Battery
    cpu: Cpu
    memory: Memory
    language: Language
    task_bar: TaskBar
    keyboard: Keyboard
    player: Player
    storage: Storage
    workspaces: Workspaces
    window_title: WindowTitle
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
config: BarConfig = parsed_data
