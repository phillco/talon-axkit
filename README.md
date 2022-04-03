```
░█████╗░██╗░░██╗██╗░░██╗██╗████████╗
██╔══██╗╚██╗██╔╝██║░██╔╝██║╚══██╔══╝
███████║░╚███╔╝░█████═╝░██║░░░██║░░░
██╔══██║░██╔██╗░██╔═██╗░██║░░░██║░░░
██║░░██║██╔╝╚██╗██║░╚██╗██║░░░██║░░░
╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░
```

Experimental [Talon](https://talonvoice.com/) integrations using macOS accessibility APIs.

## Features

- **Menu actions:** You can easily generate actions to directly run any item in an application's menu (the one in the menubar), as if you had clicked on it. "talon copy menu select" will generate the Talonscript to run the menu item underneath the cursor. You can then add that to your talon files to run that menu item directly in response to a command.
- **Closing/minimize/fullscreening windows:** Several flexible commands for closing/minimizing/fullscreening windows (the current one, everything but the current one, or everything -- for the current app, or even for apps that are not focused.)
- **Window documents:** Commands for manipulating the "document" of the current window. In macOS, this is typically the file being edited (for an editor), or the directory you're viewing (for Finder, or your terminal). You can reveal its location in Finder ("document reveal"), copy its path to the clipboard ("document copy path"), and open it either in the default application ("document open"), or a specific application "document open in Sublime".

## Coming soon

- **Slack and Discord channel navigation:** Switch directly to channels with a single voice command; a list of channels in the grammar increases accuracy.
- **Interacting with native UI elements in the current window:** For example, clicking buttons or links by name, selecting text areas, etc. Some of this will depend on the performance of the target application.
- **Window navigation using lists:** Switch between windows of the current application, or a non-focused application, by specifying a subset of the window title (a list grammar increases accuracy). Handy for switching between projects in your editor, for example.
- **Accessibility dictation:** A provider for context-aware dictation that can work instantly in supported applications, instead of doing the cursor selection dance. We can also directly insert into the text field.
- **Accessibility _editing_:** Navigate and/or directly edit the current input field by referring to words (e.g. "select the quick brown fox"; "go before jumps", "replace dog with cat"). You can also select tokens by name in your editor ("select get list from csv" would select "get_list_from_csv").

## Possibly coming soon

(Depends on community interest)

- **Autodictate:** Automatically switch to dictation mode when focusing a text area in any application, then automatically switch back to command mode when you deselect it.

## Installation

Clone alongside knausj in your `.talon/user` folder:

```
$ cd ~/.talon/user/
$ git clone https://github.com/phillco/talon_axkit.git
```

This repo requires a [knausj](https://github.com/knausj85/knausj_talon) checkout in your user/ folder, but it doesn't need to be super recent -- anything after April 2021 should work.

## Help wanted

We would love a couple of beta testers and/or code reviewers. Reach out in #talon-mac if you are interested!

## Why a separate repo?

The goal is for most of this to be upstreamed eventually, but a small repository allows us to experiment and iterate more quickly in the short term without having to synchronize knausj versions (this allows us to ship without waiting for Phil to merge his fork of knausj from early 2021. :D).
