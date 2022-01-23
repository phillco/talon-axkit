from talon import Context, Module, actions, ui, cron
from talon.mac.ui import App, Window

ctx = Context()
mod = Module()


@mod.action_class
class Actions:

    def close_window(window: Window):
        """Close the given window"""

        # Can't close a window that doesn't have a close button
        if "AXCloseButton" not in window.element.attrs:
            return

        try:
            window.element.AXCloseButton.perform("AXPress")
        except Exception as e:
            print(f"Error closing window {window.title}: {e}")

    def close_windows_app(app: App, close_current: bool = True, close_others: bool = True):
        """Closes windows for the given application

        `close_current`: whether to close the current window
        `close_others`: whether to close the non-current window
        """
        for window in app.windows():
            if window == app.active_window and not close_current:
                continue

            if window != app.active_window and not close_others:
                continue

            # NOTE(pcohen): closing can be slow; use cron as cheap multithreading
            cron.after("0s", lambda w=window: actions.user.close_window(w))

    def close_windows(close_current: bool = True, close_others: bool = True, app_name: str = None):
        """Closes windows for the given application name; if None, defaults to the current application

        `close_current`: whether to close the current window
        `close_others`: whether to close the non-current window
        """
        if app_name:
            app = ui.apps(name=app_name)[0]
        else:
            app = ui.active_app()

        actions.user.close_windows_app(app,
                                       close_current=close_current,
                                       close_others=close_others)
