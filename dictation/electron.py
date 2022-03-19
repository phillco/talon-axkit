from typing import Optional

from talon import Context, ui, Module
from talon.mac.ui import App
from talon.ui import UIErr

ctx = Context()
ctx.matches = "os: mac"

mod = Module()

@mod.action_class
class ModActions:
    def enable_electron_accessibility(app: Optional[App] = None):
        """Enables AX support in Electron - may affect performance"""
        if not app:
            app = ui.active_app()
        
        try:
            app.element.AXManualAccessibility = True
        except UIErr as e:
            # It's expected to get "Error setting element attribute", 
            pass

