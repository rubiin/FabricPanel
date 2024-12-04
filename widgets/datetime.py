from fabric.widgets.box import Box
from fabric.widgets.datetime import DateTime

from utils.config import BarConfig


class DateTimeBox(Box):
    """A widget to display the current date and time."""

    def __init__(self,config: BarConfig, **kwargs):
        super().__init__(name="date-time", style_classes="panel-box", **kwargs)

        self.date_time = DateTime()
        self.children = self.date_time
