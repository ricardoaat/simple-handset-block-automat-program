""" Handy util functions module  """
import logging
import datetime
from modules.Colors import Colors

def logconsole(message, action):
    """ Logs and display message in console """
    now = datetime.datetime.today()
    now = now.strftime("[%Y-%m-%d %H:%M:%S]:")
    if action == "i":
        logging.info(now + message)
        print now + message
    elif action == "e":
        logging.error(Colors.FAIL + now + message + Colors.ENDC)
        print Colors.FAIL + "Error: " + message + Colors.ENDC
    else:
        logging.info(now + message)

