from dataclasses import dataclass
from typing import Optional

from talon import Context, ui, Module, actions
from talon.mac.ui import Element
from talon.types import Span

ctx = Context()
ctx.matches = "os: mac"

mod = Module()
setting_accessibility_dictation = mod.setting(
    "accessibility_dictation",
    type=bool,
    default=False,
    desc="Use accessibility APIs to implement context aware dictation.",
)

# Default number of characters to use to acquire context. Somewhat arbitrary.
# The current dictation formatter doesn't need very many, but that could change in the future.
DEFAULT_CONTEXT_CHARACTERS = 30


@dataclass
class AccessibilityContext:
    """Records the context needed for dictation"""
    content: str
    selection: Span

    def left_context(self, num_chars: int = DEFAULT_CONTEXT_CHARACTERS) -> str:
        """Returns `num_chars`' worth of context to the left of the cursor"""
        start = max(0, self.selection.left - num_chars)
        return self.content[start:self.selection.left]

    def right_context(self, num_chars: int = DEFAULT_CONTEXT_CHARACTERS) -> str:
        """Returns `num_chars`' worth of context to the right of the cursor"""
        end = min(self.selection.right + num_chars, len(self.content))
        return self.content[self.selection.right:end]


@mod.action_class
class ModActions:

    def accessibility_dictation_enabled():
        """Just exports `setting_accessibility_dictation` for use in other files"""
        return setting_accessibility_dictation.get()

    def accessibility_adjust_context_for_application(el: Element,
                                                     context: AccessibilityContext) -> AccessibilityContext:
        """Sometimes the accessibility context reported by the application is wrong, but fixable
        in predictable ways (this is most common in Electron apps).
        
        This method can be overwritten in those applications to do so.
        """
        return context

    def accessibility_create_dictation_context(el: Element) -> Optional[AccessibilityContext]:
        """Creates a `AccessibilityContext` representing the state of the input buffer
        for dictation mode
        """
        if not actions.user.accessibility_dictation_enabled():
            return None

        if not el or not el.attrs:
            # No accessibility support.
            return None

        # NOTE(pcohen): In Microsoft apps (Word, OneNote). 
        selection = el.get("AXSelectedTextRange")
        if selection is None:
            selection = Span(0, 0)
        context = AccessibilityContext(content=el.get("AXValue"), selection=selection)

        # Support application-specific overrides:
        context = actions.user.accessibility_adjust_context_for_application(el, context)

        # If we don't appear to have any accessibility information, don't use it.
        if context.content is None or context.selection is None:
            return None

        return context


@ctx.action_class("self")
class Actions:
    """Wires this in to the knausj dictation formatter"""

    def dictation_peek_left(clobber=False):
        context = actions.user.accessibility_create_dictation_context(ui.focused_element())
        if context is None:
            return actions.next()

        return context.left_context()

    def dictation_peek_right():
        context = actions.user.accessibility_create_dictation_context(ui.focused_element())
        if context is None:
            return actions.next()

        return context.right_context()
