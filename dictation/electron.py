from typing import Optional

from talon import Context, Module, actions, ui
from talon.mac.ui import App
from talon.ui import UIErr

ctx = Context()
ctx.matches = "os: mac"

mod = Module()
setting_electron_accessibility = mod.setting(
    "enable_electron_accessibility",
    type=bool,
    default=False,
    desc="Tells Electron apps to enable their accessibility trees, so that you can use accessibility dictation with them. Note that this could cause worse performance, depending on the app.",
)


@mod.action_class
class ModActions:
    def enable_electron_accessibility(app: Optional[App] = None):
        """Enables AX support in Electron - may affect performance"""
        if not app:
            app = ui.active_app()

        try:
            app.element.AXManualAccessibility = True
        except UIErr:
            # This will raise "Error setting element attribute" even on success.
            pass


def app_activate(app):
    if setting_electron_accessibility.get():
        actions.user.enable_electron_accessibility(app)


ui.register("app_activate", app_activate)
