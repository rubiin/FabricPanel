import json

from fabric.utils import (
    bulk_connect,
    exec_shell_command_async,
    get_relative_path,
    invoke_repeater,
)
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from loguru import logger

from utils.functions import text_icon
from utils.icons import ICONS

class Updates(EventBox):
    """A widget to display the number of available updates."""

    def __init__(
        self,
        os: str,
        icon: str = ICONS["updates"],
        icon_size="14px",
        interval: int = 30 * 60000,
        enable_label=True,
        enable_tooltip=True,
        **kwargs,
    ):
        # Initialize the EventBox with specific name and style
        super().__init__(name="updates", **kwargs)
        self.enable_label = enable_label
        self.enable_tooltip = enable_tooltip
        # Create a TextIcon with the specified icon and size
        self.text_icon = text_icon(
            icon,
            size=icon_size,
            props={"style_classes": "panel-text-icon"},
        )
        self.os = os

        # for some reason, the style class is not being applied to the eventbox
        self.box = Box(style_classes="panel-box")

        self.children = self.box

        self.box.children = self.text_icon
        self.update_level_label = Label(label="0", style_classes="panel-text")

        # Show initial value of 0 if label is enabled
        if self.enable_label:
            self.box.children = (self.text_icon, self.update_level_label)

        # Set up a repeater to call the update method at specified intervals
        invoke_repeater(interval, self.update, initial_call=True)

        # Connect the button press event to the update method
        bulk_connect(
            self,
            {"button-press-event": lambda *_: self.update()},
        )

    def update_values(self, value: str):
        # Parse the JSON value
        value = json.loads(value)

        # Update the label if enabled
        if self.enable_label:
            self.update_level_label.set_label(value["total"])

        # Update the tooltip if enabled
        if self.enable_tooltip:
            self.set_tooltip_text(value["tooltip"])
        return True

    def update(self):
        # Get the path to the update script
        filename = get_relative_path("../assets/scripts/updates.sh")

        logger.info("[Updates] Checking for updates...")

        # Execute the update script asynchronously and update values
        exec_shell_command_async(
            f"{filename} -{self.os}",
            lambda output: self.update_values(output),
        )

        return True
