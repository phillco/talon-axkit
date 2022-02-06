import os
from urllib.parse import urlparse, unquote

from talon import Context, Module, actions, ui, app
from talon.mac import applescript

mod = Module()
ctx = Context()
ctx.matches = r"""
os: mac
"""

# TODO(pcohen): support application names
setting_terminal = mod.setting(
    "preferred_terminal",
    type=str,
    default="com.apple.Terminal",
    desc="The application bundle to use in the 'open in terminal' commands (e.g., 'com.apple.Terminal', 'com.googlecode.iterm2')"
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
            if url.scheme == 'file':  # will there ever be other schemes?
                return unquote(url.path)
        except AttributeError:
            pass

        # Fallback to doc
        return window.doc

    def file_manager_terminal_here():
        """Default implementation that opens the current directory in the terminal"""
        path = actions.user.file_manager_current_path()

        if not path:
            app.notify("Can't open terminal", "The current application does not report a path to open")
            return

        if os.path.isfile(path):
            path = os.path.abspath(os.path.join(path, os.pardir))

        if not os.path.exists(path):
            app.notify("Can't open terminal", f"The current application reported a path that doesn't exist: {path}")
            return

        escaped_path = path.replace(r'"', r'\"')
        applescript.run(rf"""
            tell application id "{setting_terminal.get()}"
                activate
                open "{escaped_path}"
            end tell
        """)

@ctx.action_class("edit")
class Actions:
    """Default macOS implementations for edit actions"""

    def selected_text() -> str:
        try:
            return ui.focused_element().AXSelectedText
        except Exception:
            try:
                # TODO(pcohen): extract this focused_element() -> AXFocusedUIElement fallback
                # if we expect to need it in the future.
                return ui.active_app().element.AXFocusedUIElement.AXSelectedText
            except Exception:
                return actions.next()
