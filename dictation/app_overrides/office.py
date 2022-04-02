from talon import Context, Module, ui

ctx = Context()
mod = Module()

mod.apps.excel_mac = """
os: mac
and app.bundle: com.microsoft.Excel
"""
mod.apps.powerpoint_mac = r"""
os: mac
and app.bundle: com.microsoft.Powerpoint
"""
mod.apps.word_mac = r"""
os: mac
and app.bundle: com.microsoft.Word
"""
mod.apps.outlook_mac = r"""
os: mac
and app.bundle: com.microsoft.Outlook
"""
mod.apps.office_mac = r"""
app: excel_mac
app: powerpoint_mac
app: word_mac
app: outlook_mac
"""

ctx.matches = """
app: office_mac
"""


@ctx.action_class("user")
class UserActions:
    def dictation_current_element():
        # Work around focused element being initially set incorrectly
        # in Mac Office apps.
        el = ui.focused_element()
        role = el.AXRole
        if role == "AXTextArea":
            return el
        elif (role == "AXScrollArea") or (  # Outlook, PowerPoint
            role == "AXSplitGroup" and el.get("AXIdentifier") == "Document Pane"  # Word
        ):
            for textarea in el.children.find(AXRole="AXTextArea"):
                if textarea.AXSelectedTextRange.left is not None:  # NSNotFound
                    return textarea
