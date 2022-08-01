import re

from talon import Module, app, clip, ctrl, ui

mod = Module()

# Only documentation I can find is this email from Eric Schlegel in 2004:
# https://lists.apple.com/archives/accessibility-dev/2004/Apr/msg00019.html

# from <HIToolbox/Menus.h>
kMenuNoModifiers = 0  # Mask for no modifiers
kMenuShiftModifier = 1 << 0  # Mask for shift key modifier
kMenuOptionModifier = 1 << 1  # Mask for option key modifier
kMenuControlModifier = 1 << 2  # Mask for control key modifier
kMenuNoCommandModifier = 1 << 3  # Mask for no command key modifier

# observed
kMenuFnGlobeModifier = 1 << 4  # Not in Menus.h, but works

# from <HIToolbox/Menus.h>
kMenuNullGlyph = 0x00  # Null (always glyph 1)
kMenuTabRightGlyph = 0x02  # Tab to the right key (for left-to-right script systems)
kMenuTabLeftGlyph = 0x03  # Tab to the left key (for right-to-left script systems)
kMenuEnterGlyph = 0x04  # Enter key
kMenuShiftGlyph = 0x05  # Shift key
kMenuControlGlyph = 0x06  # Control key
kMenuOptionGlyph = 0x07  # Option key
kMenuSpaceGlyph = 0x09  # Space (always glyph 3) key
# Delete to the right key (for right-to-left script systems)
kMenuDeleteRightGlyph = 0x0A
kMenuReturnGlyph = 0x0B  # Return key (for left-to-right script systems)
kMenuReturnR2LGlyph = 0x0C  # Return key (for right-to-left script systems)
kMenuNonmarkingReturnGlyph = 0x0D  # Nonmarking return key
kMenuPencilGlyph = 0x0F  # Pencil key
kMenuDownwardArrowDashedGlyph = 0x10  # Downward dashed arrow key
kMenuCommandGlyph = 0x11  # Command key
kMenuCheckmarkGlyph = 0x12  # Checkmark key
kMenuDiamondGlyph = 0x13  # Diamond key
kMenuAppleLogoFilledGlyph = 0x14  # Apple logo key (filled)
kMenuParagraphKoreanGlyph = 0x15  # Unassigned (paragraph in Korean)
kMenuDeleteLeftGlyph = 0x17  # Delete to the left key (for left-to-right script systems)
kMenuLeftArrowDashedGlyph = 0x18  # Leftward dashed arrow key
kMenuUpArrowDashedGlyph = 0x19  # Upward dashed arrow key
kMenuRightArrowDashedGlyph = 0x1A  # Rightward dashed arrow key
kMenuEscapeGlyph = 0x1B  # Escape key
kMenuClearGlyph = 0x1C  # Clear key
kMenuLeftDoubleQuotesJapaneseGlyph = 0x1D  # Unassigned (left double quotes in Japanese)
# Unassigned (right double quotes in Japanese)
kMenuRightDoubleQuotesJapaneseGlyph = 0x1E
kMenuTrademarkJapaneseGlyph = 0x1F  # Unassigned (trademark in Japanese)
kMenuBlankGlyph = 0x61  # Blank key
kMenuPageUpGlyph = 0x62  # Page up key
kMenuCapsLockGlyph = 0x63  # Caps lock key
kMenuLeftArrowGlyph = 0x64  # Left arrow key
kMenuRightArrowGlyph = 0x65  # Right arrow key
kMenuNorthwestArrowGlyph = 0x66  # Northwest arrow key
kMenuHelpGlyph = 0x67  # Help key
kMenuUpArrowGlyph = 0x68  # Up arrow key
kMenuSoutheastArrowGlyph = 0x69  # Southeast arrow key
kMenuDownArrowGlyph = 0x6A  # Down arrow key
kMenuPageDownGlyph = 0x6B  # Page down key
kMenuAppleLogoOutlineGlyph = 0x6C  # Apple logo key (outline)
kMenuContextualMenuGlyph = 0x6D  # Contextual menu key
kMenuPowerGlyph = 0x6E  # Power key
kMenuF1Glyph = 0x6F  # F1 key
kMenuF2Glyph = 0x70  # F2 key
kMenuF3Glyph = 0x71  # F3 key
kMenuF4Glyph = 0x72  # F4 key
kMenuF5Glyph = 0x73  # F5 key
kMenuF6Glyph = 0x74  # F6 key
kMenuF7Glyph = 0x75  # F7 key
kMenuF8Glyph = 0x76  # F8 key
kMenuF9Glyph = 0x77  # F9 key
kMenuF10Glyph = 0x78  # F10 key
kMenuF11Glyph = 0x79  # F11 key
kMenuF12Glyph = 0x7A  # F12 key
kMenuF13Glyph = 0x87  # F13 key
kMenuF14Glyph = 0x88  # F14 key
kMenuF15Glyph = 0x89  # F15 key
kMenuControlISOGlyph = 0x8A  # Control key (ISO standard)
kMenuEjectGlyph = 0x8C  # Eject key (available on Mac OS X 10.2 and later)
kMenuEisuGlyph = 0x8D  # Japanese eisu key (available in Mac OS X 10.4 and later)
kMenuKanaGlyph = 0x8E  # Japanese kana key (available in Mac OS X 10.4 and later)
kMenuF16Glyph = 0x8F  # F16 key (available in SnowLeopard and later)
kMenuF17Glyph = 0x90  # F17 key (available in SnowLeopard and later)
kMenuF18Glyph = 0x91  # F18 key (available in SnowLeopard and later)
kMenuF19Glyph = 0x92  # F19 key (available in SnowLeopard and later)

# observed
kMenuMicrophoneGlyph = 0x96

# from <HIToolbox/Events.h>
kVK_ANSI_A = 0x00
kVK_ANSI_S = 0x01
kVK_ANSI_D = 0x02
kVK_ANSI_F = 0x03
kVK_ANSI_H = 0x04
kVK_ANSI_G = 0x05
kVK_ANSI_Z = 0x06
kVK_ANSI_X = 0x07
kVK_ANSI_C = 0x08
kVK_ANSI_V = 0x09
kVK_ANSI_B = 0x0B
kVK_ANSI_Q = 0x0C
kVK_ANSI_W = 0x0D
kVK_ANSI_E = 0x0E
kVK_ANSI_R = 0x0F
kVK_ANSI_Y = 0x10
kVK_ANSI_T = 0x11
kVK_ANSI_1 = 0x12
kVK_ANSI_2 = 0x13
kVK_ANSI_3 = 0x14
kVK_ANSI_4 = 0x15
kVK_ANSI_6 = 0x16
kVK_ANSI_5 = 0x17
kVK_ANSI_Equal = 0x18
kVK_ANSI_9 = 0x19
kVK_ANSI_7 = 0x1A
kVK_ANSI_Minus = 0x1B
kVK_ANSI_8 = 0x1C
kVK_ANSI_0 = 0x1D
kVK_ANSI_RightBracket = 0x1E
kVK_ANSI_O = 0x1F
kVK_ANSI_U = 0x20
kVK_ANSI_LeftBracket = 0x21
kVK_ANSI_I = 0x22
kVK_ANSI_P = 0x23
kVK_ANSI_L = 0x25
kVK_ANSI_J = 0x26
kVK_ANSI_Quote = 0x27
kVK_ANSI_K = 0x28
kVK_ANSI_Semicolon = 0x29
kVK_ANSI_Backslash = 0x2A
kVK_ANSI_Comma = 0x2B
kVK_ANSI_Slash = 0x2C
kVK_ANSI_N = 0x2D
kVK_ANSI_M = 0x2E
kVK_ANSI_Period = 0x2F
kVK_ANSI_Grave = 0x32
kVK_ANSI_KeypadDecimal = 0x41
kVK_ANSI_KeypadMultiply = 0x43
kVK_ANSI_KeypadPlus = 0x45
kVK_ANSI_KeypadClear = 0x47
kVK_ANSI_KeypadDivide = 0x4B
kVK_ANSI_KeypadEnter = 0x4C
kVK_ANSI_KeypadMinus = 0x4E
kVK_ANSI_KeypadEquals = 0x51
kVK_ANSI_Keypad0 = 0x52
kVK_ANSI_Keypad1 = 0x53
kVK_ANSI_Keypad2 = 0x54
kVK_ANSI_Keypad3 = 0x55
kVK_ANSI_Keypad4 = 0x56
kVK_ANSI_Keypad5 = 0x57
kVK_ANSI_Keypad6 = 0x58
kVK_ANSI_Keypad7 = 0x59
kVK_ANSI_Keypad8 = 0x5B
kVK_ANSI_Keypad9 = 0x5C

# keycodes for keys that are independent of keyboard layout
kVK_Return = 0x24
kVK_Tab = 0x30
kVK_Space = 0x31
kVK_Delete = 0x33
kVK_Escape = 0x35
kVK_Command = 0x37
kVK_Shift = 0x38
kVK_CapsLock = 0x39
kVK_Option = 0x3A
kVK_Control = 0x3B
kVK_RightCommand = 0x36
kVK_RightShift = 0x3C
kVK_RightOption = 0x3D
kVK_RightControl = 0x3E
kVK_Function = 0x3F
kVK_F17 = 0x40
kVK_VolumeUp = 0x48
kVK_VolumeDown = 0x49
kVK_Mute = 0x4A
kVK_F18 = 0x4F
kVK_F19 = 0x50
kVK_F20 = 0x5A
kVK_F5 = 0x60
kVK_F6 = 0x61
kVK_F7 = 0x62
kVK_F3 = 0x63
kVK_F8 = 0x64
kVK_F9 = 0x65
kVK_F11 = 0x67
kVK_F13 = 0x69
kVK_F16 = 0x6A
kVK_F14 = 0x6B
kVK_F10 = 0x6D
kVK_F12 = 0x6F
kVK_F15 = 0x71
kVK_Help = 0x72
kVK_Home = 0x73
kVK_PageUp = 0x74
kVK_ForwardDelete = 0x75
kVK_F4 = 0x76
kVK_End = 0x77
kVK_F2 = 0x78
kVK_PageDown = 0x79
kVK_F1 = 0x7A
kVK_LeftArrow = 0x7B
kVK_RightArrow = 0x7C
kVK_DownArrow = 0x7D
kVK_UpArrow = 0x7E

# ISO keyboards only
kVK_ISO_Section = 0x0A

# JIS keyboards only
kVK_JIS_Yen = 0x5D
kVK_JIS_Underscore = 0x5E
kVK_JIS_KeypadComma = 0x5F
kVK_JIS_Eisu = 0x66
kVK_JIS_Kana = 0x68

VK_NAMES = {
    kVK_Return: "enter",
    kVK_Tab: "tab",
    kVK_Space: "space",
    kVK_Delete: "backspace",
    kVK_Escape: "esc",
    # kVK_Command: '',
    # kVK_Shift: '',
    # kVK_CapsLock: '',
    # kVK_Option: '',
    # kVK_Control: '',
    # kVK_RightCommand: '',
    # kVK_RightShift: '',
    # kVK_RightOption: '',
    # kVK_RightControl: '',
    # kVK_Function: '',
    # kVK_F17: '',
    # kVK_VolumeUp: '',
    # kVK_VolumeDown: '',
    # kVK_Mute: '',
    kVK_F18: "f18",
    kVK_F19: "f19",
    kVK_F20: "f20",
    kVK_F5: "f5",
    kVK_F6: "f6",
    kVK_F7: "f7",
    kVK_F3: "f3",
    kVK_F8: "f8",
    kVK_F9: "f9",
    kVK_F11: "f11",
    kVK_F13: "f13",
    kVK_F16: "f16",
    kVK_F14: "f14",
    kVK_F10: "f10",
    kVK_F12: "f12",
    kVK_F15: "f15",
    # kVK_Help: '',
    kVK_Home: "home",
    kVK_PageUp: "pageup",
    kVK_ForwardDelete: "delete",
    kVK_F4: "f4",
    kVK_End: "end",
    kVK_F2: "f2",
    kVK_PageDown: "pagedown",
    kVK_F1: "f1",
    kVK_LeftArrow: "left",
    kVK_RightArrow: "right",
    kVK_DownArrow: "down",
    kVK_UpArrow: "up",
    # kVK_ISO_Section: '',
    # kVK_JIS_Yen: '',
    # kVK_JIS_Underscore: '',
    # kVK_JIS_KeypadComma: '',
    # kVK_JIS_Eisu: '',
    # kVK_JIS_Kana: '',
}


def active_menu_bar():
    return ui.active_app().children.find_one(AXRole="AXMenuBar", max_depth=0)


def selected_menu_and_path():
    """Returns selected element in menu bar, and path to it"""
    selected_menu = active_menu_bar()
    menu_path = []
    while True:
        if not selected_menu.AXSelectedChildren:
            break
        selected_menu = selected_menu.AXSelectedChildren[0]

        if not (title := selected_menu.get("AXTitle")):
            return selected_menu, menu_path

        menu_path.append(selected_menu.AXTitle)
        # XXX(nriley) this is True even if list empty - report Talon bug? children also doesn't support len()
        # print(selected_menu.children, bool(selected_menu.children))
        try:
            selected_menu = selected_menu.children.find_one(
                AXRole="AXMenu", max_depth=0
            )
        except ui.UIErr:
            break

    return selected_menu, menu_path


def mouse_pos_menu_and_path():
    """Returns element in menu bar under cursor, and path to it"""
    menu_path = []
    element_at_mouse_pos = ui.element_at(*ctrl.mouse_pos())
    if element_at_mouse_pos.AXRole in ("AXMenu", "AXMenuItem", "AXMenuBarItem"):
        menu = element_at_mouse_pos
        while True:
            if menu.AXRole in ("AXMenuItem", "AXMenuBarItem"):
                menu_path.append(menu.AXTitle)
            menu = menu.AXParent
            if menu.AXRole == "AXMenu":
                menu = menu.AXParent
            elif menu.AXRole == "AXMenuBar":
                menu_path.reverse()
                break
        else:  # not in menu bar
            return None, []

    return element_at_mouse_pos, menu_path


def selected_menu_path_strategy():
    """Returns 'selected' element in menu bar, path to it and strategy used to find it"""
    selected_menu, selected_menu_path = selected_menu_and_path()

    if (
        selected_menu_path
        and hasattr(ui, "element_at")
        and selected_menu.AXRole != "AXMenuItem"
    ):
        element_at_mouse_pos, mouse_pos_menu_path = mouse_pos_menu_and_path()
        if element_at_mouse_pos and len(mouse_pos_menu_path) > len(selected_menu_path):
            return (
                element_at_mouse_pos,
                mouse_pos_menu_path,
                "Found under mouse pointer",
            )

    return selected_menu, selected_menu_path, "Found selected"

def selected_menu_key_path_strategy():
    """Returns Talon-format key equivalent of the menu item that is currently highlighted,
    , path to it and strategy used to find it"""
    selected_menu, menu_path, strategy = selected_menu_path_strategy()

    if (not selected_menu) or selected_menu.AXRole != "AXMenuItem":
        app.notify("No menu bar item selected or under the mouse pointer")
        return None, None, None

    key_char = selected_menu.get("AXMenuItemCmdChar")
    modifiers = selected_menu.get("AXMenuItemCmdModifiers")
    glyph = selected_menu.get("AXMenuItemCmdGlyph")
    virtual_key = selected_menu.get("AXMenuItemCmdVirtualKey")

    menu_keys = []

    if modifiers is not None:
        if not (modifiers & kMenuNoCommandModifier):
            menu_keys.append("cmd")
        if modifiers & kMenuShiftModifier:
            menu_keys.append("shift")
        if modifiers & kMenuOptionModifier:
            menu_keys.append("alt")
        if modifiers & kMenuControlModifier:
            menu_keys.append("ctrl")
        if modifiers & kMenuFnGlobeModifier:
            menu_keys.append("fn")

    got_key = False

    if key_char is not None:
        menu_keys.append(key_char.lower())
        got_key = True

    if not got_key and virtual_key is not None:
        if key_name := VK_NAMES.get(virtual_key):
            menu_keys.append(key_name)
            got_key = True

    # XXX(nriley) consider accounting for glyphs in some cases
    # Example: "Num Lock" in Terminal has kVK_Escape but kMenuClearGlyph
    # However, cmd-esc works fine to trigger it

    if not got_key:
        no_key_message = []
        if virtual_key is not None:
            no_key_message.append(f"virtual key code {virtual_key:X}")
        if glyph is not None:
            no_key_message.append(f"glyph {glyph:X}")
        if no_key_message:
            print("Unsupported key with", ", ".join(no_key_message))
            print(selected_menu.dump())
            app.notify("Key not supported", "\n".join(no_key_message))
        else:
            app.notify("Key not found")
        return None, None, None

    return "-".join(menu_keys), menu_path, strategy

@mod.action_class
class Actions:
    def copy_menu_select():
        """Copies TalonScript to select the menu item that is currently highlighted"""
        _, menu_path, strategy = selected_menu_path_strategy()

        if not menu_path:
            app.notify("No menu bar item selected or under the mouse pointer")
            return

        escaped_menu_path = [
            title.replace("\\", r"\\").replace("|", r"\|") for title in menu_path
        ]

        clip.set_text(f'user.menu_select({"|".join(escaped_menu_path)!r})')
        app.notify(
            "Copied TalonScript to select menu item",
            body=f'{" ▸ ".join(menu_path)}\n{strategy}',
        )

    def copy_menu_key():
        """Copies TalonScript to press the key equivalent of the menu item that is currently highlighted"""

        menu_key, menu_path, strategy = selected_menu_key_path_strategy()

        talonscript = f'key({menu_key})'
        clip.set_text(talonscript)
        app.notify(
            f"Copied TalonScript: {talonscript}",
            body=f'{" ▸ ".join(menu_path)}\n{strategy}',
        )

    def copy_menu_key_python():
        """Copies Python to press the key equivalent of the menu item that is currently highlighted"""

        menu_key, menu_path, strategy = selected_menu_key_path_strategy()

        python = f'actions.key("{menu_key}")'
        clip.set_text(python)
        app.notify(
            f"Copied Python: {python}",
            body=f'{" ▸ ".join(menu_path)}\n{strategy}',
        )


    def menu_select(menu_path: str) -> bool:
        """Selects the menu item at the specified |-delimited path, or returns False if it does not exist"""
        menu_path = [
            item_title.replace(r"\\", "\\").replace(r"\|", "|")
            for item_title in re.split(r"(?<=[^\\])\|", menu_path)
        ]
        menu_title = menu_path[0]
        try:
            menu_item = active_menu_bar().children.find_one(
                AXRole="AXMenuBarItem", AXTitle=menu_title
            )
        except ui.UIErr:
            app.notify("Unable to locate menu to select", menu_title)
            return False

        for item_title in menu_path[1:]:
            if len(menu_item.AXChildren) == 0:
                break

            menu = menu_item.children[0]
            try:
                menu_item = menu.children.find_one(
                    AXRole="AXMenuItem", AXTitle=item_title, max_depth=0
                )
            except ui.UIErr:
                app.notify("Unable to locate menu item to select", item_title)
                return False

        if menu_item.AXTitle != menu_path[-1]:
            app.notify("Expected a submenu", menu_item.AXTitle)
            return False

        menu_item.perform("AXPress")
        return True
