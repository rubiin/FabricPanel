from fabric.widgets.button import Button

from shared.buttontoggle import CommandSwitcher


class HyprIdle(Button):
    """A widget to control the hypridle command."""

    def __init__(self, config, **kwargs):
        super().__init__(**kwargs)
        # Store the configuration for hypridle
        self.config = config["hypr_idle"]

        # Set the command to hypridle
        self.command = "hypridle"

    def create(self):
        # Create a CommandSwitcher to toggle the hypridle command
        return CommandSwitcher(
            command=self.command,
            enabled_icon=self.config["enabled_icon"],
            disabled_icon=self.config["disabled_icon"],
            enable_label=self.config["enable_label"],
            enable_tooltip=self.config["enable_tooltip"],
            name="hypridle",
        )
