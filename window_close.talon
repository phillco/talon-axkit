os: mac
--

close window: user.close_windows(1, 0)
close other windows: user.close_windows(0, 1)
close [all] windows: user.close_windows(1, 1)
close all <user.running_applications> windows: user.close_windows(1, 1, user.running_applications)
close other <user.running_applications> windows: user.close_windows(0, 1, user.running_applications)
