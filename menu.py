from talon import Module, app, clip, ui

import re

mod = Module()

def active_menubar():
    return ui.active_app().children.find_one(AXRole='AXMenuBar', max_depth=0)

@mod.action_class
class Actions:
    def copy_menu_select():
        """Copies TalonScript to select the menu item that is currently highlighted"""
        selected_menu = active_menubar()
        menu_path = []
        while True:
            if not selected_menu.AXSelectedChildren:
                break
            selected_item = selected_menu.AXSelectedChildren[0]
            menu_path.append(selected_item.AXTitle.replace('\\', r'\\').replace('|', r'\|'))
            # XXX this is True even if list empty - report Talon bug? children also doesn't support len()
            # print(selected_item.children, bool(selected_item.children))
            try:
                selected_menu = selected_item.children.find_one(AXRole='AXMenu', max_depth=0)
            except ui.UIErr:
                break

        clip.set_text(f'user.menu_select({"|".join(menu_path)!r})')
        app.notify('Copied TalonScript to select menu item', ' ▸ '.join(menu_path))

    def menu_select(menu_path: str) -> bool:
        """Selects the menu item at the specified |-delimited path, or returns False if it does not exist"""
        menu_path = [item_title.replace(r'\\', '\\') for item_title in re.split(r'(?<=[^\\])\|', menu_path)]
        menu_title = menu_path[0]
        try:
            menu_item = active_menubar().children.find_one(AXRole='AXMenuBarItem', AXTitle=menu_title)
        except ui.UIErr:
            app.notify('Unable to locate menu to select', menu_title)
            return False

        for item_title in menu_path[1:]:
            if len(menu_item.AXChildren) == 0:
                break

            menu = menu_item.children[0]
            try:
                menu_item = menu.children.find_one(AXRole='AXMenuItem', AXTitle=item_title, max_depth=0)
            except ui.UIErr:
                app.notify('Unable to locate menu item to select', item_title)
                return False

        if menu_item.AXTitle != menu_path[-1]:
            app.notify('Expected a submenu', menu_item.AXTitle)
            return False

        menu_item.perform('AXPress')
        return True