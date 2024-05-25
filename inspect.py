from reprlib import Repr

from talon import Context, Module, actions, ctrl, ui

mod = Module()
ctx = Context()

ctx.matches = """
os: mac
"""

REPR = Repr()
REPR.indent = 4


@mod.action_class
class Actions:
    def element_print_hierarchy_at_mouse_pos(
        all_attributes: bool, complex_attributes: bool
    ):
        """Print information about the element at the mouse cursor position and its parents"""

    def element_print_hierarchy(
        element: ui.Element, all_attributes: bool, complex_attributes: bool
    ):
        """Print information about the element and its parents"""

    def element_print_tree_at_mouse_pos(all_attributes: bool, complex_attributes: bool):
        """Print information about the element at the mouse cursor position, its parents and parents' siblings"""

    def element_print_tree(
        element: ui.Element, all_attributes: bool, complex_attributes: bool
    ):
        """Print information about the element, its parents and parents' siblings"""

    def element_print(
        element: ui.Element, all_attributes: bool, complex_attributes: bool
    ):
        """Print information about the element"""


@ctx.action_class("user")
class UserActions:
    def element_print_hierarchy_at_mouse_pos(all_attributes, complex_attributes):
        pos = ctrl.mouse_pos()
        element = ui.element_at(*pos)

        print(f"Element hierarchy at {pos}:")
        actions.user.element_print_hierarchy(
            element, all_attributes, complex_attributes
        )

    def element_print_hierarchy(element, all_attributes, complex_attributes):
        hierarchy = []
        while element is not None:
            hierarchy.append(element_dict(element, all_attributes, complex_attributes))
            try:
                element = element.parent
            except ui.UIErr:
                break

        print("\n".join(map(format_attributes, hierarchy)))

    def element_print_tree_at_mouse_pos(all_attributes, complex_attributes):
        pos = ctrl.mouse_pos()
        element = ui.element_at(*pos)

        print(f"Element tree at {pos}:")
        actions.user.element_print_tree(element, all_attributes, complex_attributes)

    def element_print_tree(element, all_attributes, complex_attributes):
        tree = []
        while element is not None:
            try:
                parent = element.parent
            except ui.UIErr:
                tree.append(
                    [("*0", element_dict(element, all_attributes, complex_attributes))]
                )
                break
            children = [
                (
                    f"*{i}" if c == element else f" {i}",
                    element_dict(c, all_attributes, complex_attributes),
                )
                for i, c in enumerate(parent.children)
            ]
            tree.append(children)
            element = parent

        print(
            "\n".join(
                "\n".join(
                    format_attributes(e, (" " * level) + prefix)
                    for prefix, e in children
                )
                for level, children in enumerate(reversed(tree))
            )
        )

    def element_print(element, all_attributes, complex_attributes):
        print(
            format_attributes(element_dict(element, all_attributes, complex_attributes))
        )


def format_attributes(d, prefix=""):
    return f"{prefix}({', '.join(f'{k}={REPR.repr(v)}' for k, v in d.items())})"


def is_simple(val):
    return type(val) in (int, bool, str)


def element_dict(element, all_attributes, complex_attributes):
    ordered = {}
    attributes = element.dump()

    def push(key):
        if key in attributes:
            val = attributes.pop(key)
            if complex_attributes or is_simple(val):
                ordered[key] = val

    push("AXRole")
    push("AXSubrole")
    push("AXRoleDescription")
    push("AXDescription")
    push("AXIdentifier")
    push("AXDOMIdentifier")
    push("AXTitle")
    push("AXValue")
    push("AXFocused")

    if all_attributes:
        if complex_attributes:
            ordered.update(attributes)
            if attributes := element.parameterized_attrs:
                ordered["parameterized_attrs"] = attributes
        else:
            ordered.update(
                {key: val for key, val in attributes.items() if is_simple(val)}
            )

    if actions := element.actions:
        ordered["actions"] = actions

    return ordered
