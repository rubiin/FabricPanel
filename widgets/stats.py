import psutil
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.label import Label

from utils.config import BarConfig
from utils.functions import convert_bytes, text_icon
from utils.icons import ICONS


class Cpu(Box):
    """A widget to display the current CPU usage."""

    def __init__(self, config: BarConfig):
        # Initialize the Box with specific name and style
        super().__init__(name="cpu", style_classes="panel-box")

        self.config = config["cpu"]

        # Create a TextIcon with the specified icon and size
        self.text_icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )
        self.children = self.text_icon
        self.cpu_level_label = Label(label="0%", style_classes="panel-text")

        # Set up a repeater to call the update_label method at specified intervals
        invoke_repeater(self.config["interval"], self.update_label, initial_call=True)

    def update_label(self):
        # Update the label with the current CPU usage if enabled
        if self.config["enable_label"]:
            self.cpu_level_label.set_label(f"{psutil.cpu_percent()}%")
            self.children = (self.text_icon, self.cpu_level_label)

        return True


class Memory(Box):
    """A widget to display the current memory usage."""

    def __init__(self, config: BarConfig):
        # Initialize the Box with specific name and style
        super().__init__(name="memory", style_classes="panel-box")

        self.config = config["memory"]

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )
        self.children = self.icon
        self.memory_level_label = Label(label="0%", style_classes="panel-text")

        # Set up a repeater to call the update_values method at specified intervals
        invoke_repeater(self.config["interval"], self.update_values, initial_call=True)

    def update_values(self):
        # Get the current memory usage
        self.used_memory = psutil.virtual_memory().used
        self.total_memory = psutil.virtual_memory().total
        self.percent_used = psutil.virtual_memory().percent

        # Update the label with the used memory if enabled
        if self.config["enable_label"]:
            self.memory_level_label.set_label(self.get_used())
            self.children = (self.icon, self.memory_level_label)

        # Update the tooltip with the memory usage details if enabled
        if self.config["enable_tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {psutil.virtual_memory().percent}%\n{ICONS['memory']} {self.get_used()}/{self.get_total()}",
            )

        return True

    def get_used(self):
        return f"{format(convert_bytes(self.used_memory, 'gb'),'.1f')}GB"

    def get_total(self):
        return f"{format(convert_bytes(self.total_memory, 'gb'),'.1f')}GB"


class Storage(Box):
    """A widget to display the current storage usage."""

    def __init__(self, config: BarConfig):
        # Initialize the Box with specific name and style
        super().__init__(name="storage", style_classes="panel-box")
        self.config = config["storage"]

        # Create a TextIcon with the specified icon and size
        self.icon = text_icon(
            icon=self.config["icon"],
            size=self.config["icon_size"],
            props={"style_classes": "panel-text-icon"},
        )

        self.children = self.icon
        self.storage_level_label = Label(label="0", style_classes="panel-text")

        # Set up a repeater to call the update_values method at specified intervals
        invoke_repeater(self.config["interval"], self.update_values, initial_call=True)

    def update_values(self):
        # Get the current disk usage
        self.disk = psutil.disk_usage("/")

        # Update the label with the used storage if enabled
        if self.config["enable_label"]:
            self.storage_level_label.set_label(f"{self.get_used()}")
            self.children = (self.icon, self.storage_level_label)

        # Update the tooltip with the storage usage details if enabled
        if self.config["enable_tooltip"]:
            self.set_tooltip_text(
                f"󰾆 {self.disk.percent}%\n{ICONS['storage']} {self.get_used()}/{self.get_total()}",
            )

        return True

    def get_used(self):
        return f"{format(convert_bytes(self.disk.used, 'gb'),'.1f')}GB"

    def get_total(self):
        return f"{format(convert_bytes(self.disk.total, 'gb'),'.1f')}GB"
