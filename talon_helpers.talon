os: mac
-
^talon copy menu select: user.copy_menu_select()
^talon copy menu key: user.copy_menu_key()
^talon copy menu key pie: user.copy_menu_key_python()

^talon copy app element:
    bundle = app.bundle()
    clip.set_text('ui.apps(bundle="{bundle}")[0].element')
