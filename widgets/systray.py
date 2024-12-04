import gi
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.image import Image
from gi.repository import Gdk, GdkPixbuf, Gray, Gtk
from loguru import logger

from utils.config import BarConfig

gi.require_version("Gray", "0.1")
gi.require_version("Gtk", "3.0")


class SystemTray(Box):
    """A widget to display the system tray items."""

    def __init__(self, config: BarConfig, **kwargs) -> None:
        super().__init__(name="system-tray", style_classes="panel-box", **kwargs)

        self.config = config["system_tray"]

        self.watcher = Gray.Watcher()
        self.watcher.connect("item-added", self.on_item_added)

    def on_item_added(self, _, identifier: str):
        item = self.watcher.get_item_for_identifier(identifier)
        item_button = self.do_bake_item_button(item)
        item.connect("removed", lambda *args: item_button.destroy())
        item_button.show_all()
        self.add(item_button)

    def do_bake_item_button(self, item: Gray.Item) -> Button:
        button = Button()

        button.set_tooltip_text(item.get_property("title"))

        # context menu handler
        button.connect(
            "button-press-event",
            lambda button, event: self.on_button_click(button, item, event),
        )

        # get pixel map of item's icon
        pixmap = Gray.get_pixmap_for_pixmaps(item.get_icon_pixmaps(), 24)

        # convert the pixmap to a pixbuf
        pixbuf: GdkPixbuf.Pixbuf = (
            pixmap.as_pixbuf(self.config["icon_size"], GdkPixbuf.InterpType.HYPER)
            if pixmap is not None
            else Gtk.IconTheme()
            .get_default()
            .load_icon(
                item.get_icon_name(),
                self.config["icon_size"],
                Gtk.IconLookupFlags.FORCE_SIZE,
            )
        )

        # resize/scale the pixbuf
        pixbuf.scale_simple(
            self.config["icon_size"],
            self.config["icon_size"],
            GdkPixbuf.InterpType.HYPER,
        )

        image = Image(pixbuf=pixbuf, pixel_size=self.config["icon_size"])
        button.set_image(image)

        return button

    def on_button_click(self, button, item: Gray.Item, event):
        match event.button:
            case 1:
                try:
                    item.activate(event.x, event.y)
                except Exception as e:
                    logger.error(e)
            case 3:
                menu = item.get_property("menu")
                menu.set_name("system-tray-menu")
                if menu:
                    menu.popup_at_widget(
                        button,
                        Gdk.Gravity.SOUTH,
                        Gdk.Gravity.NORTH,
                        event,
                    )
                else:
                    item.context_menu(event.x, event.y)
