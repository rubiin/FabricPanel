import threading

from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.label import Label
from loguru import logger

from services.weather import WeatherInfo
from utils.config import BarConfig


class Weather(Box):
    """A widget to display the current weather."""

    def __init__(
        self,
        config: BarConfig,
    ):
        # Initialize the Box with specific name and style
        super().__init__(name="weather", style_classes="panel-box")

        self.config = config["weather"]

        self.weather_label = Label(
            label="Fetching weather...",
            style_classes="panel-text",
        )
        self.children = self.weather_label

        # Set up a repeater to call the update_label method at specified intervals
        invoke_repeater(self.config["interval"], self.update_label, initial_call=True)

    def update_label(self):
        weather_thread = threading.Thread(
            target=self.fetch_weather_in_thread,
            args=(self.config["location"],),
        )
        weather_thread.start()
        # Continue running the main program (non-blocking)
        logger.info(
            "[Weather] Weather information is being fetched in a separate thread...",
        )

    # This function will run the weather fetch in a separate thread
    def fetch_weather_in_thread(self, city: str):
        weather = WeatherInfo()
        res = weather.simple_weather_info(city)
        # Update the label with the weather icon and temperature
        self.weather_label.set_label(f"{res['icon']} {res['temperature']}")

        # Update the tooltip with the city and weather condition if enabled
        if self.config["enable_tooltip"]:
            self.set_tooltip_text(f"{res['city']}, {res['condition']}".strip("'"))
        return True
