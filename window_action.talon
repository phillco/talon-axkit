os: mac
-

# Targeting the windows of the current application:
window {user.window_actions}: user.action_windows(user.window_actions, 1, 0)
window {user.window_actions} other: user.action_windows(user.window_actions, 0, 1)
window {user.window_actions} all: user.action_windows(user.window_actions, 1, 1)

# Targeting the windows of any arbitrary application:
<user.running_applications> window {user.window_actions}:
    user.action_windows(user.window_actions, 1, 0, user.running_applications)
<user.running_applications> window {user.window_actions} other:
    user.action_windows(user.window_actions, 0, 1, user.running_applications)
<user.running_applications> window {user.window_actions} all:
    user.action_windows(user.window_actions, 1, 1, user.running_applications)

# Entering and exiting fullscreen mode.
fullscreen enter: user.action_windows("fullscreen", 1, 0)
<user.running_applications> fullscreen enter:
    user.action_windows("fullscreen", 1, 0, user.running_applications)
fullscreen exit: key(cmd-ctrl-f)

# Legacy commands which use verb-noun:
{user.window_actions} window: user.action_windows(user.window_actions, 1, 0)
{user.window_actions} other windows: user.action_windows(user.window_actions, 0, 1)
{user.window_actions} [all] windows: user.action_windows(user.window_actions, 1, 1)
{user.window_actions} all <user.running_applications> windows:
    user.action_windows(user.window_actions, 1, 1, user.running_applications)
{user.window_actions} other <user.running_applications> windows:
    user.action_windows(user.window_actions, 0, 1, user.running_applications)
