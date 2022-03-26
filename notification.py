from dataclasses import dataclass, field
from itertools import chain
from typing import Optional

from talon import Context, Module, actions, app, cron, ui

# XXX actions are being returned out of order; that's a problem if we want to pop up a menu

mod = Module()

mod.list("notification_actions", desc="Notification actions")
mod.list("notification_apps", desc="Notification apps")

try:
    from rich.console import Console

    def print(obj: any, *args):
        """Pretty prints the object"""
        console = Console(color_system="truecolor", soft_wrap=True)
        if args:
            console.out(obj, *args)
        else:
            console.print(obj)

except ImportError:
    pass


@mod.action_class
class Actions:
    def notification_action(index: int, action: str) -> bool:
        """Perform the specified action on the notification (stack) at the specified index"""
        return False

    def notification_app_action(app_name: str, action: str) -> bool:
        """Perform the specified action on the first notification (stack) for the specified app"""
        return False

    def notifications_update():
        """Update notification list to reflect what is currently onscreen"""
        # (poll? not try to keep up? not sure what else to do)

    def notification_center():
        """Display or hide Notification Center"""


@dataclass(frozen=True)
class Notification:
    identifier: int
    subrole: str = field(default=None, compare=False)
    app_name: str = field(default=None, compare=False)
    stacking_identifier: str = field(default=None, compare=False)
    title: str = field(default=None, compare=False)
    body: str = field(default=None, compare=False)
    # action values are named "Name:<name>\nTarget:0x0\nSelector:(null)"; keys are speakable
    actions: dict[str, str] = field(default=None, compare=False)

    @staticmethod
    def group_identifier(group):
        identifier = getattr(group, "AXIdentifier", None)

        if identifier is None or not str.isdigit(identifier):
            return None

        return int(identifier)

    @staticmethod
    def from_group(group, identifier):
        actions = group.actions
        if "AXScrollToVisible" in actions:
            del actions["AXScrollToVisible"]  # not useful
        # XXX create_spoken_forms_from_list doesn't handle apostrophes correctly
        # https://github.com/knausj85/knausj_talon/issues/780
        actions = {
            name.lower().replace("’", "'"): action for action, name in actions.items()
        }

        title = None
        try:
            title = group.children.find_one(AXIdentifier="title").AXValue
        except ui.UIErr:
            pass

        body = None
        try:
            body = group.children.find_one(AXIdentifier="body").AXValue
        except ui.UIErr:
            pass

        return Notification(
            identifier=identifier,
            subrole=group.AXSubrole,
            app_name=group.AXDescription,
            stacking_identifier=group.AXStackingIdentifier,
            title=title,
            body=body,
            actions=actions,
        )

    @staticmethod
    def notifications_in_window(window):
        notifications = []

        for group in window.children.find(AXRole="AXGroup"):
            if not (identifier := Notification.group_identifier(group)):
                continue

            notification = Notification.from_group(group, identifier)
            notifications.append(notification)

        return notifications


MONITOR = None

ctx = Context()
ctx.matches = r"""
os: mac
"""

ctx.lists["user.notification_actions"] = {}
ctx.lists["user.notification_apps"] = {}


@ctx.action_class("user")
class UserActions:
    def notification_action(index: int, action: str) -> bool:
        return MONITOR.perform_action(action, index=index)

    def notification_app_action(app_name: str, action: str) -> bool:
        return MONITOR.perform_action(action, app_name=app_name)

    def notifications_update():
        MONITOR.update_notifications()

    def notification_center():
        cc = ui.apps(bundle="com.apple.controlcenter")[0]
        cc.element.children.find_one(AXRole="AXMenuBar", max_depth=0).children.find_one(
            AXRole="AXMenuBarItem",
            AXSubrole="AXMenuExtra",
            AXIdentifier="com.apple.menuextra.clock",
            max_depth=0,
        ).perform("AXPress")


class NotificationMonitor:
    __slots__ = (
        "pid",
        "notifications",
    )

    def __init__(self, app: ui.App):
        self.pid = app.pid
        self.notifications = []

        ui.register("win_open", self.win_open)
        ui.register("win_close", self.win_close)
        ui.register("app_close", self.app_closed)

        self.update_notifications()

    def win_open(self, window):

        if not window.app.pid == self.pid:
            return

        notifications = Notification.notifications_in_window(window)
        self.update_notifications(adding=notifications)

    def notification_groups(self):
        ncui = ui.apps(pid=self.pid)[0]
        for window in ncui.windows():
            for group in window.children.find(AXRole="AXGroup"):
                if not (identifier := Notification.group_identifier(group)):
                    continue

                yield identifier, group

    def perform_action(
        self, action: str, index: Optional[int] = None, app_name: str = None
    ):
        self.update_notifications()

        cron.after("500ms", self.update_notifications)

        notification = None
        if index is not None:
            if index < 0 or index > len(self.notifications) - 1:
                app.notify(f"Unable to locate notification #{index + 1}", "Try again?")
                return False

            notification = self.notifications[index]
        elif app_name is not None:
            try:
                notification = next(
                    notification
                    for notification in self.notifications
                    if notification.app_name == app_name
                )
            except StopIteration:
                app.notify(
                    f"Unable to locate notification for {app_name}", "Try again?"
                )
                return False

        for identifier, group in self.notification_groups():
            if identifier != notification.identifier:
                continue

            print(f"performing {action} in {notification.actions}")

            if action not in notification.actions:
                # allow closing a notification stack like an individual notification
                if action == "close" and "clear all" in notification.actions:
                    action = "clear all"
                else:
                    app.notify(f"No such action “{action}”", "Try again?")
                    return False

            group.perform(notification.actions[action])
            return True

        app.notify("Unable to locate notification", "Try again?")
        return False

    def update_notifications(self, adding=[]):
        if adding:
            self.notifications += adding

        notifications = {}
        for identifier, group in self.notification_groups():
            y = group.AXPosition.y

            try:
                notifications[y] = self.notifications[
                    self.notifications.index(Notification(identifier=identifier))
                ]
            except ValueError:
                notifications[y] = Notification.from_group(group, identifier)

        self.notifications = list(notifications.values())
        if notifications:
            print(notifications)

        notification_actions = set()
        notification_apps = set()

        for notification in self.notifications:
            notification_actions.update(notification.actions.keys())
            notification_apps.add(notification.app_name)

        notification_actions = list(notification_actions)
        # XXX create_spoken_forms_from_list doesn't handle apostrophes correctly
        # https://github.com/knausj85/knausj_talon/issues/780
        apostrophe_words = {
            word.replace("'", " "): word
            for word in chain.from_iterable(
                action.split() for action in notification_actions
            )
            if "'" in word
        }
        words_to_exclude = [word.split(" ")[0] for word in apostrophe_words]
        notification_actions = actions.user.create_spoken_forms_from_list(
            notification_actions, words_to_exclude=words_to_exclude
        )
        if apostrophe_words:
            notification_actions = {
                spoken_form.replace(mangled_word, word): action
                for mangled_word, word in apostrophe_words.items()
                for spoken_form, action in notification_actions.items()
                if "apostrophe" not in spoken_form
            }
        if notification_actions:
            print("actions", notification_actions)

        if "close" not in notification_actions and "clear all" in notification_actions:
            # allow closing a notification stack like an individual notification
            notification_actions["close"] = "clear all"
        ctx.lists["user.notification_actions"] = notification_actions

        # XXX use app name overrides from knausj?
        notification_apps = actions.user.create_spoken_forms_from_list(
            notification_apps
        )
        ctx.lists["user.notification_apps"] = notification_apps
        if notification_apps:
            print("apps", notification_apps)

    def win_close(self, window):
        if not window.app.pid == self.pid:
            return

        self.update_notifications()

    def app_closed(self, app):
        if app.pid == self.pid:
            ui.unregister("app_close", self.app_closed)


def app_launched(app):
    global MONITOR

    if not app.bundle == "com.apple.notificationcenterui":
        return

    MONITOR = NotificationMonitor(app)


def monitor():
    global MONITOR

    apps = ui.apps(bundle="com.apple.notificationcenterui")
    if apps:
        MONITOR = NotificationMonitor(apps[0])

    ui.register("app_launch", app_launched)


app.register("ready", monitor)
