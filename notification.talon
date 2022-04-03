os: mac
-
^(note | notification) <number_small> {user.notification_actions}$:
	user.notification_action(number_small - 1, notification_actions)

^(note | notification) {user.notification_actions} <number_small>$:
	user.notification_action(number_small - 1, notification_actions)

^(note | notification) {user.notification_actions} {user.notification_apps}$:
	user.notification_app_action(notification_apps, notification_actions)

^(note | notification) {user.notification_apps} {user.notification_actions}$:
	user.notification_app_action(notification_apps, notification_actions)

^(note | notification) update$:
	user.notifications_update()

^(note | notification) center$:
	user.notification_center()
	user.notifications_update()
