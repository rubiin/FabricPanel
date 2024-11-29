from typing import cast
from fabric.widgets.box import Box
from fabric.widgets.eventbox import EventBox
from fabric.widgets.revealer import Revealer
from fabric.widgets.label import Label
from fabric.widgets.image import Image
from fabric.widgets.button import Button
from fabric.widgets.wayland import WaylandWindow
from fabric.notifications import Notifications, Notification
from fabric.utils import invoke_repeater, bulk_connect

from gi.repository import GdkPixbuf

NOTIFICATION_WIDTH = 360
NOTIFICATION_IMAGE_SIZE = 64
NOTIFICATION_TIMEOUT = 10 * 1000  # 10 seconds


class NotificationPopupWidget(EventBox):
    def __init__(self, notification: Notification, **kwargs):
        super().__init__(
            **kwargs,
        )

        notif_box = Box(
            name="notification",
            spacing=8,
            orientation="v",
            size=(NOTIFICATION_WIDTH, -1),
        )

        self.children = notif_box

        self._notification = notification

        body_container = Box(spacing=4, orientation="h")

        if image_pixbuf := self._notification.image_pixbuf:
            body_container.add(
                Image(
                    pixbuf=image_pixbuf.scale_simple(
                        NOTIFICATION_IMAGE_SIZE,
                        NOTIFICATION_IMAGE_SIZE,
                        GdkPixbuf.InterpType.BILINEAR,
                    )
                )
            )

        body_container.add(
            Box(
                spacing=4,
                orientation="v",
                children=[
                    # a box for holding both the "summary" label and the "close" button
                    Box(
                        orientation="h",
                        children=[
                            Label(
                                label=self._notification.summary,
                                ellipsization="middle",
                            )
                            .build()
                            .add_style_class("summary")
                            .unwrap(),
                        ],
                        h_expand=True,
                        v_expand=True,
                    )
                    # add the "close" button
                    .build(
                        lambda box, _: box.pack_end(
                            Button(
                                image=Image(
                                    icon_name="close-symbolic",
                                    icon_size=16,
                                ),
                                v_align="center",
                                h_align="end",
                                on_clicked=lambda *_: self._notification.close(),
                            ),
                            False,
                            False,
                            0,
                        )
                    ),
                    Label(
                        label=self._notification.body,
                        line_wrap="word-char",
                        v_align="start",
                        h_align="start",
                    )
                    .build()
                    .add_style_class("body")
                    .unwrap(),
                ],
                h_expand=True,
                v_expand=True,
            )
        )

        notif_box.add(body_container)

        self.actions_revealer = Revealer(
            transition_type="slide_down",
            reveal_child=False,
        )

        if actions := self._notification.actions:
            self.actions_revealer.children = Box(
                spacing=4,
                orientation="h",
                children=[
                    Button(
                        h_expand=True,
                        v_expand=True,
                        label=action.label,
                        on_clicked=lambda *_, action=action: action.invoke(),
                    )
                    for action in actions
                ],
            )

        notif_box.add(self.actions_revealer)

        bulk_connect(
            self,
            {
                "enter-notify-event": lambda *_: (
                    self.actions_revealer.set_reveal_child(True),
                ),
                "leave-notify-event": lambda *_: (
                    self.actions_revealer.set_reveal_child(False)
                ),
            },
        )

        # destroy this widget once the notification is closed

        self._notification.connect(
            "closed",
            lambda *_: (
                parent.remove(self) if (parent := self.get_parent()) else None,  # type: ignore
                self.destroy(),
            ),
        )

        # automatically close the notification after the timeout period
        invoke_repeater(
            NOTIFICATION_TIMEOUT,
            lambda: self._notification.close("expired"),
            initial_call=False,
        )


class NotificationsPopup(WaylandWindow):
    def __init__(self, **kwargs):
        super().__init__(
            margin="8px 8px 8px 8px",
            anchor="top right",
            child=Box(
                size=2,  # so it's not ignored by the compositor
                spacing=4,
                orientation="v",
            ).build(
                lambda viewport, _: Notifications(
                    on_notification_added=lambda notifs_service, nid: viewport.add(
                        NotificationPopupWidget(
                            cast(
                                Notification,
                                notifs_service.get_notification_from_id(nid),
                            )
                        )
                    )
                )
            ),
            visible=True,
            all_visible=True,
            **kwargs,
        )