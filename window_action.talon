os: mac
-- {user.window_actions} window: user.action_windows(user.window_actions, 1, 0)
{user.window_actions} other windows: user.action_windows(user.window_actions, 0, 1)
{user.window_actions} [all] windows: user.action_windows(user.window_actions, 1, 1)
{user.window_actions} all <user.running_applications> windows:
    user.action_windows(user.window_actions, 1, 1, user.running_applications)
{user.window_actions} other <user.running_applications> windows:
    user.action_windows(user.window_actions, 0, 1, user.running_applications)

fullscreen enter: user.action_windows("fullscreen", 1, 0)
fullscreen exit: key(cmd-ctrl-f)
