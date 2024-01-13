import os
from urllib.parse import unquote, urlparse

from talon import Context, Module, actions, app, settings, ui
from talon.mac import applescript

mod = Module()
ctx = Context()
ctx.matches = r"""
os: mac
"""

# TODO(pcohen): support application names
mod.setting(
    "preferred_terminal",
    type=str,
    default="com.apple.Terminal",
    desc="The application bundle to use in the 'open in terminal' commands (e.g., 'com.apple.Terminal', 'com.googlecode.iterm2')",
)


@ctx.action_class("user")
class user_actions:
    """Default macOS implementations for user actions"""

    def file_manager_current_path():
        """A generic fallback for that will use `window.doc` to provide the current path
        in applications that don't implement a more specific function."""

        # NOTE(pcohen): using AXDocument because active_window().doc
        # returns URL-encoded path sometimes: https://github.com/talonvoice/talon/issues/473
        window = ui.active_window()
        try:
            url = urlparse(window.element.AXDocument)
            if url.scheme == "file":  # will there ever be other schemes?
                return unquote(url.path)
        except AttributeError:
            pass

        # Fallback to doc
        return window.doc

    def file_manager_terminal_here():
        """Default implementation that opens the current directory in the terminal"""
        path = actions.user.file_manager_current_path()

        if not path:
            app.notify(
                "Can't open terminal",
                "The current application does not report a path to open",
            )
            return

        if os.path.isfile(path):
            # If the application gave a file, open the terminal in its parent directory.
            path = os.path.abspath(os.path.join(path, os.pardir))

        if not os.path.exists(path):
            app.notify(
                "Can't open terminal",
                f"The current application reported a path that doesn't exist: {path}",
            )
            return

        escaped_path = path.replace(r'"', r"\"")
        applescript.run(
            rf"""
            tell application id "{settings.get('user.preferred_terminal')}"
                activate
                open "{escaped_path}"
            end tell
        """
        )


@ctx.action_class("edit")
class Actions:
    """Default macOS implementations for edit actions"""

    def selected_text() -> str:
        try:
            selected_text = ui.focused_element().AXSelectedText
            if not selected_text:
                # Some partially-accessible applications incorrectly report empty selections sometimes, and this can be
                # quite bad depending on the use case. For maximum safety we have to fall back to the clipboard
                # implementation in this case. This could be customized if we knew the application was fully
                # trustworthy.
                #
                # See https://github.com/phillco/talon-axkit/issues/59
                return actions.next()

            return selected_text
        except Exception:
            return actions.next()
