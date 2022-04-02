import time
import traceback

from talon import Module, actions, cron, noise, ui

try:
    from talon.mac.ui import Element
except ImportError:
    Element = type(None)

HISS_DEBUG_ENABLED = True

mod = Module()
setting_enabled = mod.setting(
    "hiss_to_debug_accessibility",
    type=bool,
    default=False,
    desc="Use a hissing sound to print accessibility debugging information to the Talon log.",
)
setting_threshold = mod.setting(
    "hiss_to_debug_accessibility_threshold",
    type=float,
    default=0.35,
    desc="If hiss_to_debug_accessibility is enabled, the hissing duration (in seconds) needed to trigger the debug output.",
)


@mod.action_class
class Actions:
    def debug_accessibility(el: Element = None):
        """Prints information about the currently focused UI element to the terminal, for debugging"""

        if not el:
            el = ui.focused_element()

        try:
            # TODO(pcohen): make this work without Rich installed
            from rich.console import Console

            console = Console(color_system="truecolor", soft_wrap=True)

            console.rule(f"{str(el)}'s attributes:")

            # Attempt to sort the keys by relying on insertion order.
            attributed = {}
            for k in sorted(el.attrs):
                attributed[k] = el.get(k)

            console.print(attributed, markup=False)
        except Exception as e:
            print(f'Exception while debugging accessibility: "{e}":')
            traceback.print_exc()


active_hiss = {"cron": None}


def hiss_over_threshold():
    if not active_hiss.get("start"):
        return False

    return time.time() - active_hiss["start"] > setting_threshold.get()


def stop_hiss():
    trigger = hiss_over_threshold()

    if active_hiss["cron"]:
        cron.cancel(active_hiss["cron"])
        active_hiss["cron"] = None

    active_hiss["start"] = None

    if trigger:
        actions.user.debug_accessibility()


def check_hiss():
    if hiss_over_threshold():
        stop_hiss()


def start_hiss():
    active_hiss["start"] = time.time()
    active_hiss["cron"] = cron.interval("32ms", check_hiss)


def on_hiss(noise_active: bool):
    if not setting_enabled.get():
        return

    if noise_active:
        start_hiss()
    else:
        stop_hiss()


noise.register("hiss", on_hiss)
