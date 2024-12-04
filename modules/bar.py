from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.wayland import WaylandWindow as Window

from utils.config import config
from widgets import (
    Battery,
    Cpu,
    DateTimeBox,
    KeyboardLayout,
    LanguageBox,
    Memory,
    Mpris,
    Storage,
    Updates,
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
            "workspaces": WorkSpaces,
            "system_tray": SystemTray,
            "task_bar": TaskBar,
            "keyboard": KeyboardLayout,
            # WindowTitle: Shows the title of the current window
            "window_title": WindowTitle,
            # LanguageBox: Displays the current language selection
            "language": LanguageBox,
            # DateTime: Displays the current date and time
            "datetime": DateTimeBox,
            # HyprSunset: Provides information about the sunset time based on location
            # "hypr_sunset": HyprSunset.create(),
            # # HyprIdle: Shows the idle time for the system
            # "hypr_idle": HyprIdle.create(),
            # Battery: Displays the battery status with optional label and tooltip
            "battery": Battery,
            # Cpu: Displays CPU usage information with optional label and tooltip
            "cpu": Cpu,
            # # ClickCounter: Tracks the number of clicks on a widget or component
            # "click_counter": ClickCounter(),
            # Memory: Displays the system's memory usage
            "memory": Memory,
            # Storage: Shows the system's storage usage (e.g., disk space)
            "storage": Storage,
            # Weather: Displays the weather for a given city (e.g., Kathmandu)
            "weather": Weather,
            # Player: Displays information about the current media player status
            "player": Mpris,
            # Updates: Shows available system updates based on the OS
            "updates": Updates,
        }

        layout = self.make_layout()



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
                children=layout["right_children"],
            ),
        )

        self.show_all()

    def make_layout(self):
        layout = {"left_children": [], "middle_children": [], "right_children": []}

        # firset set of widgets (Left)
        layout["left_children"].extend(
           self.widgets_list[widget](config) for widget in config["layout"]["left"]
        )

        # second set of widgets (Center)
        layout["middle_children"].extend(
            self.widgets_list[widget](config) for widget in config["layout"]["middle"]
        )

             # second set of widgets (Center)
        layout["right_children"].extend(
            self.widgets_list[widget](config) for widget in config["layout"]["right"]
        )


        return layout
