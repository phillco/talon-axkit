import os
import subprocess
from typing import Optional

from talon import Context, Module, actions, app, clip

ctx = Context()
mod = Module()

default_ctx = Context()
default_ctx.matches = r"""
os: mac
"""

OPEN_CMD_PATH = "/usr/bin/open"


@mod.action_class
class Actions:
    def represented_file_is_valid(doc: str) -> bool:
        """Returns whether the given document path is valid, showing alerts if not."""

        if not doc:
            app.notify(
                "No document available",
                "The current window doesn't expose its document information",
            )
            return False

        if not os.path.exists(doc):
            app.notify(
                "Document doesn't exist",
                f"The current window's document doesn't seem to exist on disk:\n\n{doc}",
            )
            return False

        return True

    def open_current_doc(cmd: str = None) -> Optional[subprocess.CompletedProcess]:
        """Opens the current document in the default open handler, or passing it to {cmd}."""

        doc = actions.user.file_manager_current_path()
        if not actions.user.represented_file_is_valid(doc):
            return None

        return subprocess.run([cmd if cmd else OPEN_CMD_PATH, doc])

    def open_current_doc_in_app(
        app_or_path: str = None,
    ) -> Optional[subprocess.CompletedProcess]:
        """Opens the current document in the given application, which could be a path or name of a running application."""

        doc = actions.user.file_manager_current_path()
        if not actions.user.represented_file_is_valid(doc):
            return None

        if app_or_path.endswith(".app") and os.path.exists(app_or_path):
            path = app_or_path
        else:
            application = actions.user.get_running_app(app_or_path)
            if not application:
                app.notify(
                    "Couldn't find application",
                    f"Couldn't find a running app named {application}",
                )
                return
            path = application.path

        return subprocess.run([OPEN_CMD_PATH, "-a", path, doc])

    def copy_current_doc_path(cmd: str = None) -> bool:
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
            app.notify(
                "No document to open",
                "The current application doesn't expose its document information",
            )
            return None

        return subprocess.run([OPEN_CMD_PATH, "-R", doc])
