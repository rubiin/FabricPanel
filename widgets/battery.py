import math

import psutil
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.image import Image
from fabric.widgets.label import Label

from utils.config import BarConfig
from utils.functions import format_time


class Battery(Box):
    """A widget to display the current battery status."""

    def __init__(
        self,
        config: BarConfig,
    ):
        # Initialize the Box with specific name and style
        super().__init__(name="battery", style_classes="panel-box")
        self.config = config["battery"]
        self.full_battery_level = 100

        # Set up a repeater to call the update_battery_status method
        invoke_repeater(
            self.config["interval"], self.update_battery_status, initial_call=True
        )

    def update_battery_status(self):
        """Update the battery status by fetching the current battery information
        and updating the widget accordingly.
        """
        # Get the battery status
        battery = psutil.sensors_battery()

        if battery is None:
            self.hide()
            return None

        battery_percent = round(battery.percent) if battery else 0

        battery_label = Label(label=f"{battery_percent}%", style_classes="panel-text")

        is_charging = battery.power_plugged if battery else False

        battery_icon = Image(
            icon_name=self.get_icon_name(
                battery_percent=battery_percent,
                is_charging=is_charging,
            ),
            icon_size=14,
        )

        self.children = battery_icon

        # Update the label with the battery percentage if enabled
        if self.config["enable_label"]:
            self.children = (battery_icon, battery_label)

            ## Hide the label when the battery is full
            if (
                self.config["hide_label_when_full"]
                and battery_percent == self.full_battery_level
            ):
                self.children = battery_icon

        # Update the tooltip with the battery status details if enabled
        if self.config["enable_tooltip"]:
            if battery_percent == self.full_battery_level:
                self.set_tooltip_text("Full")
            elif is_charging and battery_percent < self.full_battery_level:
                self.set_tooltip_text(f"Time to full: {format_time(battery.secsleft)}")
            else:
                self.set_tooltip_text(f"Time to empty: {format_time(battery.secsleft)}")

        return True

    def get_icon_name(self, battery_percent: int, is_charging: bool):
        """Determine the icon name based on the battery percentage and charging status."""
        # Determine the icon name based on the battery percentage and charging status
        if battery_percent == self.full_battery_level:
            return "battery-level-100-charged-symbolic"
        icon_level = math.floor(battery_percent / 10) * 10
        return (
            f"battery-level-{icon_level}{'-charging' if is_charging else ''}-symbolic"
        )
