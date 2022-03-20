from talon import Context, Module

ctx = Context()
ctx.matches = """
os: mac
app: messages
"""
mod = Module()

@ctx.action_class
class Actions:
    
    def accessibility_adjust_context_for_application(el, context):
        # Messages reports an empty buffer as having None as content instead of "".
        # We use None as a signal for "accessibility not available", so make sure it is reported as "".
        if context.content is None:
            context.content = ""
        
        return context
