os: mac
-
^(note | notification) <number_small> {user.notification_actions}$:
	user.notification_action(number_small - 1, notification_actions)

^(note | notification) update$:
	user.notifications_update()
