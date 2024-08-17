os: mac
-
element hierarchy: user.element_print_hierarchy_at_mouse_pos(false, false)
element hierarchy more: user.element_print_hierarchy_at_mouse_pos(true, false)
element hierarchy all: user.element_print_hierarchy_at_mouse_pos(true, true)

element tree: user.element_print_tree_at_mouse_pos(false, false)
element tree more: user.element_print_tree_at_mouse_pos(true, false)
element tree all: user.element_print_tree_at_mouse_pos(true, true)

focused hierarchy:
    focused_element = user.focused_element_safe()
    if focused_element: user.element_print_hierarchy(focused_element, false, false)
focused hierarchy more:
    focused_element = user.focused_element_safe()
    if focused_element: user.element_print_hierarchy(focused_element, true, false)
focused hierarchy all:
    focused_element = user.focused_element_safe()
    if focused_element: user.element_print_hierarchy(focused_element, true, true)

focused tree:
    focused_element = user.focused_element_safe()
    if focused_element: user.element_print_tree(focused_element, false, false)
focused tree more:
    focused_element = user.focused_element_safe()
    if focused_element: user.element_print_tree(focused_element, true, false)
focused tree all:
    focused_element = user.focused_element_safe()
    if focused_element: user.element_print_tree(focused_element, true, true)
