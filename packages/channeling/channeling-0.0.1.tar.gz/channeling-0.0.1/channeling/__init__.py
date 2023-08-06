"""
Channeling - a Discord bot.
"""
__version__ = "0.0.1"
__license__ = "BSD"
__year__ = "2020"
__author__ = "Predrag Mandic"
__author_email__ = "predrag@nul.one"
__copyright__ = "Copyright {} {} <{}>".format(
    __year__, __author__, __author_email__)

class ansi:
    ''' 
    ANSI colors for pretty output.
    '''
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'
    yellow = '\033[93m'
    bold = '\033[1m'
    underline = '\033[4m'
    end = '\033[0m'

class ChannelingException(Exception):
    """Generic channeling exception."""
    pass

