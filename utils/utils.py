import json
from typing import Literal
from fabric.widgets.label import Label
import psutil
import datetime
from fabric.utils import get_relative_path


# Function to read the configuration file
def read_config():
    with open(get_relative_path("../config.json"), "r") as file:
        # Load JSON data into a Python dictionary
        data = json.load(file)
    return data


# Function to create a text icon label
def TextIcon(icon: str, size: str = "24px", props: dict = None):
    label_props = {
        "label": str(icon),  # Directly use the provided icon name
        "name": "nerd-icon",
        "style": f"font-size: {size}; ",  # Set font family for Material Icons
        "h_align": "center",  # Align horizontally
        "v_align": "center",  # Align vertically
    }

    if props:
        label_props.update(props)

    return Label(**label_props)


# Function to format time in hours and minutes
def format_time(secs: int):
    mm, _ = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d h %02d min" % (hh, mm)


# Function to convert bytes to kilobytes, megabytes, or gigabytes
def convert_bytes(bytes: int, to: Literal["kb", "mb", "gb"]):
    multiplier = 1

    if to == "mb":
        multiplier = 2
    elif to == "gb":
        multiplier = 3

    return bytes / (1024**multiplier)


# Function to get the system uptime
def uptime():
    return datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S")
