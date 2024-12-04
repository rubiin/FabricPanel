# FabricPanel

A semi-customizable bar written using the [Fabric Widget System](https://github.com/Fabric-Development/fabric) taking inpirations from hyprpanel and waybar for some widgets
More on [Fabric's Wiki](https://wiki.ffpy.org)

---

## Prerequisites

- [JetBrains Nerd Font](https://www.nerdfonts.com)
- [python 3+](https://www.python.org/downloads/)

---

## **Installation**

### Required

Most of these are already installed on existing working machines

```sh
networkmanager

pipewire


## Bluetooth menu utilities
bluez
bluez-utils

## Copy/Paste utilities
wl-clipboard

## Compiler for sass/scss
dart-sass

## Brightness module for OSD
brightnessctl
```

Run the following command to install the required packages:

```sh
# Arch Linux

sudo pacman -S pipewire dart-sass networkmanager wl-clipboard brightnessctl python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python python-pip python-gobject python-psutils python-cairo python-loguru pkgconf

# OpenSUSE

sudo zypper install pipewire networkmanager wl-clipboard brightnessctl python gtk3-devel cairo-devel gtk-layer-shell-devel libgirepository-1_0-1 libgirepository-2_0-0 gobject-introspection-devel python311 python311-pip python311-psutils python311-gobject python311-gobject-cairo python311-pycairo python311-loguru pkgconf
```

### Optional

```sh

## To check for pacman updates in the default script used in the updates module
pacman-contrib

## To record screen through the dashboard record shortcut
gpu-screen-recorder

## To enable the eyedropper color picker with the default snapshot shortcut in the dashboard
hyprpicker

## To enable hyprland's very own blue light filter
hyprsunset

## To enable hyprland's very own idle inhibitor
hypridle

```

### **2. Clone the Repository**

Clone this repository:

```sh
git clone https://github.com/rubiin/FabricPanel.git
cd FabricPanel
```

### **3. Install Dependencies**

Install the requirements:

```sh
pip install -r requirements.txt
```

---

## **Usage**

### **For Hyprland:**

Add the following line to your `hypr.conf` to start FabricPanel automatically:

```sh
exec = python main.py
```

or in virtual environment as

```sh
source "$HOME/bar/.venv/bin/activate" && python "$HOME/bar/main.py"

```

modify the path accordingly

### **For Other Window Managers:**

Use a similar configuration for your respective window manager's autostart setup.

## **Available Modules**

- battery
- workspaces
- window_title
- media
- volume
- weather
- keyboard
- clock
- system_tray
- taskbar
- language
- keyboard
- ram
- cpu
- storage
- cputemp
- updates
- hypr_sunset
- hypr_idle

> [!WARNING]
> This is still in early development and will include breaking changes
