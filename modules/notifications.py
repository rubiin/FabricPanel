import time

import gi
from fabric.notifications import (
    Notification,
    NotificationAction,
    NotificationCloseReason,
    Notifications,
)
from fabric.utils import invoke_repeater
from fabric.widgets.box import Box
from fabric.widgets.button import Button
from fabric.widgets.eventbox import EventBox
from fabric.widgets.image import Image
from fabric.widgets.label import Label
from fabric.widgets.revealer import Revealer
from fabric.widgets.wayland import WaylandWindow
from gi.repository import GdkPixbuf, GLib

from shared.customimage import CustomImage
from utils.functions import check_icon_exists

gi.require_version("GdkPixbuf", "2.0")

NOTIFICATION_WIDTH = 400
NOTIFICATION_IMAGE_SIZE = 64
NOTIFICATION_TIMEOUT = 5 * 1000  # 5 seconds


class ActionButton(Button):
    """A button widget to represent a notification action."""

    def __init__(
        self,
        action: NotificationAction,
        action_number: int,
        total_actions: int,
    ):
        self.action = action
        super().__init__(
            label=action.label,
            h_expand=True,
            on_clicked=self.on_clicked,
            style_classes="notification-action",
        )
        if action_number == 0:
            self.add_style_class("start-action")
        elif action_number == total_actions - 1:
            self.add_style_class("end-action")
        else:
            self.add_style_class("middle-action")

    def on_clicked(self, *_):
        self.action.invoke()
        self.action.parent.close("dismissed-by-user")


class NotificationWidget(EventBox):
    """A widget to display a notification."""

    def __init__(self, notification: Notification, **kwargs):
        super().__init__(
            size=(NOTIFICATION_WIDTH, -1),
            **kwargs,
        )

        self.notification_box = Box(
            spacing=8,
            name="notification",
            orientation="v",
        )

        self.connect("button-press-event", self.on_button_press)

        self._notification = notification

        self.time = GLib.DateTime.new_from_unix_local(time.time()).format("%m/%d")

        header_container = Box(
            spacing=8, orientation="h", style_classes="notification-header"
        )

        header_container.children = (
            self.get_icon(notification.app_icon, 25),
            Label(
                markup=str(
                    self._notification.summary
                    if self._notification.summary
                    else notification.app_name,
                ),
                h_align="start",
                style_classes="summary",
                ellipsization="end",
            ),
        )

        header_container.pack_end(
            Box(
                v_align="start",
                children=(
                    Button(
                        image=Image(
                            icon_name=check_icon_exists(
                                "close-symbolic",
                                "window-close-symbolic",
                            ),
                            icon_size=16,
                        ),
                        style_classes="close-button",
                        on_clicked=lambda *_: self._notification.close(
                            "dismissed-by-user"
                        ),
                    ),
                ),
            ),
            False,
            False,
            0,
        )

        body_container = Box(
            spacing=4, orientation="h", style_classes="notification-body"
        )

        # Use provided image if available, otherwise use "notification-symbolic" icon
        if image_pixbuf := self._notification.image_pixbuf:
            body_container.add(
                Box(
                    v_expand=True,
                    v_align="center",
                    children= CustomImage(
                    pixbuf=image_pixbuf.scale_simple(
                        NOTIFICATION_IMAGE_SIZE,
                        NOTIFICATION_IMAGE_SIZE,
                        GdkPixbuf.InterpType.BILINEAR,
                    ),
                    style_classes="image",
                ),
                )
            )

        body_container.add(
            Label(
                markup=self._notification.body,
                line_wrap="word-char",
                ellipsization="end",
                v_align="start",
                h_align="start",
                style_classes="body",
            ),
        )

        actions_container = Box(
            spacing=4,
            orientation="h",
            name="notification-action-box",
            children=[
                ActionButton(action, i, len(self._notification.actions))
                for i, action in enumerate(self._notification.actions)
            ],
            h_expand=True,
        )

        # Add the header, body, and actions to the notification box
        self.notification_box.add(header_container)
        self.notification_box.add(body_container)
        self.notification_box.add(actions_container)

        # Add the notification box to the EventBox
        self.add(self.notification_box)

        # Destroy this widget once the notification is closed
        self._notification.connect(
            "closed",
            lambda *_: (
                parent.remove(self) if (parent := self.get_parent()) else None,  # type: ignore
                self.destroy(),
            ),
            invoke_repeater(
                self.get_timeout(),
                lambda: self._notification.close("expired"),
                initial_call=False,
            ),
        )

    def get_icon(self, app_icon, size) -> Image:
        match app_icon:
            case str(x) if "file://" in x:
                return Image(
                    name="notification-icon",
                    image_file=app_icon[7:],
                    size=size,
                )
            case str(x) if len(x) > 0 and x[0] == "/":
                return Image(
                    name="notification-icon",
                    image_file=app_icon,
                    size=size,
                )
            case _:
                return Image(
                    name="notification-icon",
                    icon_name=app_icon if app_icon else "dialog-information-symbolic",
                    icon_size=size,
                )

    def on_button_press(self, _, event):
        if event.button != 1:
            (self._notification.close("dismissed-by-user"),)

    def get_timeout(self):
        return (
            self._notification.timeout
            if self._notification.timeout != -1
            else NOTIFICATION_TIMEOUT
        )


class NotificationRevealer(Revealer):
    """A widget to reveal a notification."""

    def __init__(self, notification: Notification, **kwargs):
        self.notif_box = NotificationWidget(notification)
        self._notification = notification
        super().__init__(
            child=Box(
                style="margin: 12px;",
                children=[self.notif_box],
            ),
            transition_duration=500,
            transition_type="crossfade",
            **kwargs,
        )

        self.connect(
            "notify::child-revealed",
            lambda *_: self.destroy() if not self.get_child_revealed() else None,
        )

        self._notification.connect("closed", self.on_resolved)

    def on_resolved(
        self,
        notification: Notification,
        reason: NotificationCloseReason,
    ):
        self.set_reveal_child(False)


class NotificationPopup(WaylandWindow):
    """A widget to grab and display notifications."""

    def __init__(self):
        self._server = Notifications()
        self.notifications = Box(
            v_expand=True,
            h_expand=True,
            style="margin: 1px 0px 1px 1px;",
            orientation="v",
            spacing=5,
        )
        self._server.connect("notification-added", self.on_new_notification)

        super().__init__(
            anchor="top right",
            child=self.notifications,
            layer="overlay",
            all_visible=True,
            visible=True,
            exclusive=False,
        )

    def on_new_notification(self, fabric_notif, id):
        new_box = NotificationRevealer(fabric_notif.get_notification_from_id(id))
        self.notifications.add(new_box)
        new_box.set_reveal_child(True)
