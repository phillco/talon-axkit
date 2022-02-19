from talon import actions, app, cron, ui, Context, Module

from dataclasses import dataclass, field

# XXX actions are being returned out of order; that's a problem if we want to pop up a menu

mod = Module()

mod.list('notification_actions', desc='Notification actions')

@mod.action_class
class Actions:
	def notification_action(index: int, action: str) -> bool:
		"""Perform the specified action on the notification at the specified index"""
		return False

	def notifications_update():
		"""Update notification list to reflect what is currently onscreen"""
		# (poll? not try to keep up? not sure what else to do)

@dataclass(frozen=True)
class Notification:
	identifier: int
	subrole: str = field(default=None, compare=False)
	stackingIdentifier: str = field(default=None, compare=False)
	title: str = field(default=None, compare=False)
	body: str = field(default=None, compare=False)
	# action values are named "Name:<name>\nTarget:0x0\nSelector:(null)"; keys are speakable
	actions: dict[str, str] = field(default=None, compare=False)

	@staticmethod
	def group_identifier(group):
		identifier = getattr(group, 'AXIdentifier', None)

		if identifier is None or not str.isdigit(identifier):
			return None

		return int(identifier)

	@staticmethod
	def from_group(group, identifier):
		stackingIdentifier = getattr(group, 'AXStackingIdentifier')
		subrole = getattr(group, 'AXSubrole')
		actions = group.actions
		if 'AXScrollToVisible' in actions: del actions['AXScrollToVisible'] # not useful
		actions = dict((name.lower(), action) for action, name in actions.items())

		title = None
		try: title = group.children.find_one(AXIdentifier='title').AXValue
		except ui.UIErr: pass
		
		body = None
		try: body = group.children.find_one(AXIdentifier='body').AXValue
		except ui.UIErr: pass

		return Notification(
			identifier=identifier,
			subrole=subrole,
			stackingIdentifier=stackingIdentifier,
			title=title,
			body=body,
			actions=actions)

	@staticmethod
	def notifications_in_window(window):
		notifications = []

		for group in window.children.find(AXRole='AXGroup'):
			if not (identifier := Notification.group_identifier(group)):
				continue

			notification = Notification.from_group(group, identifier)
			notifications.append(notification)

		return notifications

MONITOR = None

ctx = Context()
ctx.matches = r"""
os: mac
"""

ctx.lists['user.notification_actions'] = {}

@ctx.action_class('user')
class UserActions:
	def notification_action(index: int, action: str) -> bool:
		return MONITOR.perform_action(index, action)

	def notifications_update():
		MONITOR.update_notifications()

class NotificationMonitor(object):
	__slots__ = (
		'pid',
		'notifications',
	)

	def __init__(self, app: ui.App):
		self.pid = app.pid
		self.notifications = []

		ui.register('win_open', self.win_open)
		ui.register('win_close', self.win_close)
		ui.register('app_close', self.app_closed)

		self.update_notifications()

	def win_open(self, window):

		if not window.app.pid == self.pid:
			return

		notifications = Notification.notifications_in_window(window)
		self.update_notifications(adding=notifications)

	def notification_groups(self):
		ncui = ui.apps(pid=self.pid)[0]
		for window in ncui.windows():
			for group in window.children.find(AXRole='AXGroup'):
				if not (identifier := Notification.group_identifier(group)):
					continue

				yield identifier, group

	def perform_action(self, index: int, action: str):
		self.update_notifications()

		cron.after('500ms', self.update_notifications)
		if index < 0 or index > len(self.notifications) - 1:
			app.notify(f'Unable to locate notification #{index}', 'Try again?')
			return False

		notification = self.notifications[index]

		for identifier, group in self.notification_groups():
			if identifier != notification.identifier:
				continue

			print('performing', action, 'in', notification.actions)

			if action not in notification.actions:
				# allow closing a notification stack like an individual notification
				if action == 'close' and 'clear all' in notification.actions:
					action = 'clear all'
				else:
					app.notify(f'No such action “{action}”', 'Try again?')
					return False

			group.perform(notification.actions[action])
			return True

		app.notify('Unable to locate notification', 'Try again?')
		return False

	def update_notifications(self, adding=[]):
		if adding:
			self.notifications += adding

		notifications = {}
		ncui = ui.apps(pid=self.pid)[0]
		for identifier, group in self.notification_groups():
			y = group.AXPosition.y

			try:
				notifications[y] = self.notifications[
					self.notifications.index(Notification(identifier=identifier))]
			except ValueError:
				notifications[y] = Notification.from_group(group, identifier)

		self.notifications = list(notifications.values())
		print('notifications:', notifications)

		notification_actions = set()
		for notification in self.notifications:
			notification_actions.update(notification.actions.keys())
		notification_actions = list(notification_actions)
		notification_actions = actions.user.create_spoken_forms_from_list(notification_actions)
		print('actions:', notification_actions)
		if 'close' not in notification_actions and 'clear all' in notification_actions:
			# allow closing a notification stack like an individual notification
			notification_actions['close'] = 'clear all'
		ctx.lists['user.notification_actions'] = notification_actions

	def win_close(self, window):
		if not window.app.pid == self.pid:
			return

		self.update_notifications()

	def app_closed(self, app):
		if app.pid == self.pid:
			ui.unregister('app_close', self.app_closed)

def app_launched(app):
	global MONITOR

	if not app.bundle == 'com.apple.notificationcenterui':
		return

	MONITOR = NotificationMonitor(app)

def monitor():
	global MONITOR

	apps = ui.apps(bundle='com.apple.notificationcenterui')
	if apps:
		MONITOR = NotificationMonitor(apps[0])

	ui.register('app_launch', app_launched)

app.register('ready', monitor)
