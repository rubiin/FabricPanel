from fabric import Fabricator
from fabric.utils import bulk_connect, exec_shell_command
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer

from utils.config import BarConfig
from utils.icons import ICONS


class Mpris(EventBox):
    """A widget to control the MPRIS."""

    def __init__(
        self,
        config: BarConfig,
    ) -> None:
        # Initialize the EventBox with specific name and style
        super().__init__(name="mpris")
        self.config = config["player"]

        self.label = Label(label="Nothing playing", style_classes="panel-text")
        self.text_icon = Label(label=ICONS["play"], style="padding: 0 10px;")

        self.revealer = Revealer(
            name="player-revealer",
            transition_type="slide-right",
            transition_duration=300,
            child=self.label,
            reveal_child=False,
        )

        self.revealer.set_reveal_child(True)

        self.box = Box(
            style_classes="panel-box",
            children=[self.text_icon, self.revealer],
        )

        self.children = self.box

        # Connect the button press event to the play_pause method
        bulk_connect(
            self,
            {
                "button-press-event": lambda *_: self.play_pause(),
            },
        )

        player_info = Fabricator(
            poll_from=lambda: {
                "status": str(exec_shell_command("playerctl status").strip("\n")),
                "info": str(
                    exec_shell_command(
                        'playerctl metadata --format "{{ title }} - {{ artist }}"',
                    ).strip("\n"),
                ),
            },
            stream=True,
        )

        # Connect the playerInfo changes to the get_current method
        player_info.connect(
            "changed",
            lambda _, value: (self.get_current(value)),
        )

    def get_current(self, value):
        # Get the current player info and status
        info = value["info"]
        trucated_info = (
            value["info"]
            if len(value["info"]) < self.config["length"]
            else value["info"][:30]
        )
        status = value["status"]

        if self.config["enable_tooltip"]:
            self.set_tooltip_text(info)

        # Update the label and icon based on the player status
        if status == "Playing":
            self.set_visible(True)
            self.text_icon.set_label(ICONS["pause"])
            self.label.set_label(trucated_info)

        elif status == "Paused":
            self.set_visible(True)
            self.text_icon.set_label(ICONS["play"])
            self.label.set_label(trucated_info)

        else:
            self.set_visible(False)

        return True

    def play_pause(self, *_):
        # Toggle play/pause using playerctl
        exec_shell_command("playerctl play-pause")
