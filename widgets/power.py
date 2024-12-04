from fabric.widgets.button import Button

from utils.config import BarConfig


class Power(Button):
    """A widget to power off the system."""

    def __init__(self, config: BarConfig, icon="", **kwargs):
        super().__init__(name="power", style_classes="bar-button", **kwargs)
        self.set_label(icon)
