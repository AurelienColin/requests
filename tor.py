import socks
import socket
from stem import Signal
from stem.control import Controller
import time

CONTROLLER = None
CONNEXION = False
TIME_AFTER_RENEWING_TOR = 2

socks.set_default_proxy()


def renew_tor(time_after_newewing_tor=TIME_AFTER_RENEWING_TOR):
    """Create a connexion to Tor or renew it if it already exist"""
    global CONNEXION
    global CONTROLLER
    if not CONNEXION:
        CONTROLLER = Controller.from_port(port=9151)
        CONNEXION = True
    CONTROLLER.authenticate()
    CONTROLLER.signal(Signal.NEWNYM)
    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket
    time.sleep(time_after_newewing_tor)
