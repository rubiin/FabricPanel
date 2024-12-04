from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from shared.widget_conrainer import WidgetContainer
from utils.config import config
from widgets import (
    AUDIO_WIDGET,
    Battery,
    ClickCounter,
    Cpu,
    DateTimeBox,
    HyprIdle,
    HyprSunset,
    KeyboardLayout,
    LanguageBox,
    Memory,
    Mpris,
    Storage,
    Updates,
    VolumeWidget,
    Weather,
    WindowTitle,
    WorkSpaces,
)
from widgets.systray import SystemTray
from widgets.taskbar import TaskBar


class StatusBar(Window):
    """A widget to display the status bar panel."""

    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            margin="10px 10px -2px 10px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        # TODO: fix this . This is initialized by default
        self.widgets_list = {
            # Workspaces: Displays the list of workspaces or desktops
            "workspaces": WorkSpaces(config),
            "system_tray": SystemTray(config),
            "taskbar": TaskBar(),
            "keyboard": KeyboardLayout(config),
            # WindowTitle: Shows the title of the current window
            "window_title": WindowTitle(config),
            # LanguageBox: Displays the current language selection
            "language": LanguageBox(),
            # DateTime: Displays the current date and time
            "datetime": DateTimeBox(),
            # HyprSunset: Provides information about the sunset time based on location
            "hypr_sunset": HyprSunset(config).create(),
            # HyprIdle: Shows the idle time for the system
            "hypr_idle": HyprIdle(config).create(),
            # Battery: Displays the battery status with optional label and tooltip
            "battery": Battery(config),
            # Cpu: Displays CPU usage information with optional label and tooltip
            "cpu": Cpu(config),
            # ClickCounter: Tracks the number of clicks on a widget or component
            "click_counter": ClickCounter(),
            # Memory: Displays the system's memory usage
            "memory": Memory(config),
            # Storage: Shows the system's storage usage (e.g., disk space)
            "storage": Storage(config),
            # Weather: Displays the weather for a given city (e.g., Kathmandu)
            "weather": Weather(config),
            # Player: Displays information about the current media player status
            "player": Mpris(config),
            # Updates: Shows available system updates based on the OS
            "updates": Updates(config),
        }

        layout = self.make_layout()

        self.system_tray = self.widgets_list["system_tray"]

        self.status_container = WidgetContainer()
        self.status_container.add(VolumeWidget()) if AUDIO_WIDGET is True else None

        self.battery = self.widgets_list["battery"]
        self.cpu = self.widgets_list["cpu"]

        self.click_counter = self.widgets_list["clickcounter"]

        self.memory = self.widgets_list["memory"]
        self.storage = self.widgets_list["storage"]
        self.weather = self.widgets_list["weather"]
        self.player = self.widgets_list["player"]
        self.updates = self.widgets_list["updates"]

        self.children = CenterBox(
            name="panel-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=layout["left_children"],
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=layout["middle_children"],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.status_container,
                    self.updates,
                    self.battery,
                    self.system_tray,
                ],
            ),
        )

        self.show_all()

    def make_layout(self):
        layout = {"left_children": [], "middle_children": [], "right_children": []}

        # firset set of widgets (Left)
        layout["left_children"].extend(
            self.widgets_list[widget] for widget in self.config["layout"]["left"]
        )

        # second set of widgets (Center)
        layout["middle_children"].extend(
            self.widgets_list[widget] for widget in self.config["layout"]["middle"]
        )

        return layout
