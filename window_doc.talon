os: mac
--

document open: user.open_current_doc()
document open in <user.launch_applications>: user.open_current_doc_in_app(user.launch_applications)
document open in <user.running_applications>: user.open_current_doc_in_app(user.running_applications)
document (reveal|show): user.reveal_current_doc()
document copy path: user.copy_current_doc_path()
