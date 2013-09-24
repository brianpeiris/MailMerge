# set these in your settings_local.py file.
CONSUMER_KEY = ''
CONSUMER_SECRET = ''

try:
    from settings_local import *  # nopep8
except ImportError, e:
    raise Exception('Error with your local config: %s' % str(e), e)
