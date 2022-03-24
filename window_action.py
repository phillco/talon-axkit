from talon import Context, Module, actions, app, ui

if app.platform == "mac":
    from talon.mac.ui import App, Window
else:
    App = Window = None

ctx = Context()
mod = Module()

mod.list("window_actions", desc="Actions that can be applied to windows")
ctx.lists["self.window_actions"] = ["close", "minimize", "fullscreen"]

property_mapping = {
    "close": "AXCloseButton",
    "minimize": "AXMinimizeButton",
    # NOTE(pcohen): doesn't exist on windows that themselves are full screen,
    # so you can only go one way for now
    "fullscreen": "AXFullScreenButton",
}


@mod.action_class
class Actions:

    # TODO(pcohen): this could use a better name
    # "actions" here refers to what you can do with the traffic light icons
    # (close, minimize, zoom/full screen)
    def action_window(window: Window, action: str = "close"):
        """Actions the given window"""
        prop = property_mapping[action]

        # Can't close a window that doesn't have a close button
        if prop not in window.element.attrs:
            return

        for retry in range(0, 3):
            try:
                window.element[prop].perform("AXPress")
                return
            except Exception as e:
                print(f"Error {action}'ing window {window.title}: {type(e)} {e}")

    def action_windows_app(
        app: App, action: str = "close", on_current: bool = True, on_others: bool = True
    ):
        """Actions windows for the given application

        `on_current`: whether to affect the current window
        `on_others`: whether to affect the non-current window
        """
        for window in app.windows():
            if window == app.active_window and not on_current:
                continue

            if window != app.active_window and not on_others:
                continue

            # NOTE(pcohen): I used to have a cron() here but it doesn't seem to speed it up
            # (at least not with any single application)
            actions.user.action_window(window, action)

    def action_windows(
        action: str = "close",
        on_current: bool = True,
        on_others: bool = True,
        app_name: str = None,
    ):
        """Closes windows for the given application name; if None, defaults to the current application

        `on_current`: whether to affect the current window
        `on_others`: whether to affect the non-current window
        """
        if app_name:
            app = ui.apps(name=app_name)[0]
        else:
            app = ui.active_app()

        actions.user.action_windows_app(
            app, action, on_current=on_current, on_others=on_others
        )
