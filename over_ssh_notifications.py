# -*- coding: utf-8 -*-

"""
Forward notifications over a socket, to be displayed in a remote notification
service (growl, libnotify, etc)

See https://github.com/guyzmo/irssi-over-ssh-notifications.git

"""

import socket

SCRIPT_NAME = 'over-ssh-notifications'
SCRIPT_AUTHOR = 'Rui Abreu Ferreira'
SCRIPT_VERSION = '0.1'
SCRIPT_LICENSE = 'WTFPL'
SCRIPT_DESC = 'over ssh notifications for weechat'

try:
    import weechat
    IN_WEECHAT = True
except ImportError:
    IN_WEECHAT = False
    

def send_notification(summary, message):
    """Send notification to remote irssi-notify-listener"""
    msg = "%s : %s\n" % (message, summary)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect( (weechat.config_get_plugin("host"), 
                int(weechat.config_get_plugin("port"))) 
                )
        sock.send(msg)
        sock.close()
    except:
        pass

def notify_hl(*args):
    """Hook for message highlight - callback(data, signal, message)"""
    send_notification("WeeChat", args[2])
    return weechat.WEECHAT_RC_OK

def notify_priv(*args):
    """Hook for private messages - callback(data, signal, message)"""
    send_notification("WeeChat", args[2])
    return weechat.WEECHAT_RC_OK

def setup_weechat():
    """Setup weechat python plugin:
    * Add default settings for host and port
    * Register plugins
    """
    settings = {
        "host"      : "localhost",
        "port"      : '4222',
    }
    
    for opt, val in settings.items():
        if not weechat.config_get_plugin(opt):
            weechat.config_set_plugin(opt, val)
    
    # Hooks
    weechat.hook_signal("weechat_pv", "notify_priv", "")
    weechat.hook_signal("weechat_highlight", "notify_hl", "")

if __name__ == '__main__' and IN_WEECHAT and weechat.register(
    SCRIPT_NAME,
    SCRIPT_AUTHOR,
    SCRIPT_VERSION,
    SCRIPT_LICENSE,
    SCRIPT_DESC, '', ''):

    setup_weechat()
