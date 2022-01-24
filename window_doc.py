import os
import subprocess
from talon import Context, Module, actions, ui, app, clip
from typing import Optional
from urllib.parse import urlparse, unquote

ctx = Context()
mod = Module()

default_ctx = Context()
default_ctx.matches = r"""
os: mac
"""

OPEN_CMD_PATH = "/usr/bin/open"

@default_ctx.action_class("user")
class user_actions:
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


@mod.action_class
class Actions:
    def represented_file_is_valid(doc: str) -> bool:
        """Returns whether the given document path is valid, showing alerts if not."""

        if not doc:
            app.notify("No document available", "The current window doesn't expose its document information")
            return False

        if not os.path.exists(doc):
            app.notify("Document doesn't exist",
                       f"The current window's document doesn't seem to exist on disk:\n\n{doc}")
            return False

        return True

    def open_current_doc(cmd: str = None) -> Optional[subprocess.CompletedProcess]:
        """Opens the current document in the default open handler, or passing it to {cmd}.

        If {cmd} is an application, it is launched with the document passed as a parameter.
        """

        doc = actions.user.file_manager_current_path()
        if not actions.user.represented_file_is_valid(doc):
            return None

        if cmd.endswith(".app"):
            return subprocess.run([OPEN_CMD_PATH, "-a", cmd, "--args", doc])

        return subprocess.run([cmd if cmd else OPEN_CMD_PATH, doc])

    def copy_current_doc_path_path(cmd: str = None) -> bool:
        """Copies the path of the current document to the clipboard; returns success"""

        doc = actions.user.file_manager_current_path()
        if not actions.user.represented_file_is_valid(doc):
            return False

        clip.set_text(doc)
        return True

    def reveal_current_doc() -> Optional[subprocess.CompletedProcess]:
        """Reveals the current application's document in Finder"""

        doc = actions.user.file_manager_current_path()
        if not actions.user.represented_file_is_valid(doc):
            return None

        if not doc:
            app.notify("No document to open", "The current application doesn't expose its document information")
            return None

        return subprocess.run([OPEN_CMD_PATH, "-R", doc])
