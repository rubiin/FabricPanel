from fabric.hyprland.widgets import Language
from fabric.utils import FormattedString, truncate
from fabric.widgets.box import Box

from utils.config import BarConfig


class LanguageBox(Box):
    """A widget to display the current language."""

    def __init__(self, config: BarConfig, **kwargs):
        super().__init__(name="language", style_classes="panel-box", **kwargs)

        self.config = config["language"]

        self.lang = Language(
            formatter=FormattedString(
                "{truncate(language,length,suffix)}",
                truncate=truncate,
                length=self.config["length"],
                suffix="",
            ),
        )
        ## TODO: add tool tip

        self.children = self.lang
