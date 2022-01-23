from typing import Union

from talon import Context, Module, actions, ui, app

import os

ctx = Context()
mod = Module()

@mod.action_class
class Actions:

    def file_manager_current_path_or_doc():
        """Returns the current path being viewed/edited, first trying `file_manager_current_path` (in case it's implemented more
        specifically), then falling back to `window.doc`.
        """

        path = actions.user.file_manager_current_path()
        if not path:
            return ui.active_window().doc.replace("%20", " ")

    def validate_document(doc: str):
        """Returns whether the given document path is valid, showing alerts if not."""

        if not doc:
            app.notify("No document to open", "The current application doesn't expose its document information")
            return False

        if not os.path.exists(doc):
            app.notify("Document doesn't exist", f"The current application's document doesn't seem to exist on disk:\n\n{doc}")
            return False

        return True

    def open_current_doc(cmd: str = None):
        """Opens the current document in the default open handler, or passing it to {cmd}"""

        doc = actions.user.file_manager_current_path_or_doc()
        if not actions.user.validate_document(doc):
            return

        if cmd:
            return actions.user.system_command_nb(f"{cmd} \"{doc}\"")
        else:
            return actions.user.system_command_nb(f"open \"{doc}\"")

    def reveal_current_doc():
        """Reveals the current application's document in Finder"""

        doc = actions.user.file_manager_current_path_or_doc()
        if not actions.user.validate_document(doc):
            return

        if not doc:
            app.notify("No document to open", "The current application doesn't expose its document information")
            return

        return actions.user.system_command_nb(f"open -R \"{doc}\"")

