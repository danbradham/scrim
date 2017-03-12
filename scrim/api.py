__all__ = ['Scrim', 'get_scrim']
import os
import atexit
from .globals import SCRIM_AUTO_WRITE, SCRIM_PATH, SCRIM_SHELL, SCRIM_SCRIPT


def init_value(value=None, default=None):
    '''Returns default if value is None'''
    if value is None:
        return default
    return value


class Scrim(list):
    '''The Scrim object is a subclass of list. Append commands to a Scrim that
    you would like to be executed by the Scrim Script that invoked the current
    python process. It helps to think of a Scrim as an interface to the shell
    process where your python code was executed.

    The following environment variables set by Scrim Scripts provide the
    defaults for the Scrim::

    .. envvar:: SCRIM_SHELL

        Name of shell process(powershell.exe, cmd.exe..)
        If this envvar is missing we walk up the process tree until we find a
        compatible shell process.
        Currently only powershell.exe and cmd.exe are implemented

    .. envvar:: SCRIM_PATH

        Path to script file to be written to and then executed after exit

    .. envvar:: SCRIM_AUTO_WRITE

        If True automatically write out the scrim file on program exit

    .. envvar:: SCRIM_SCRIPT

        Path to the Scrim Script that invoked the current python process

    These environment variables should be set by the Scrim shell script, not by
    the user. For testing purposes these values can be overriden by passing in
    any of the following parameters.

    :param shell: Name of the shell process or :envvar:`SCRIM_SHELL`
    :param path: Path to temporary scrim file or :envvar:`SCRIM_PATH`
    :param auto_write: Write scrim file on program exit or :envvar:`SCRIM_AUTO_WRITE`
    :param script: Path to scrim script or :envvar:`SCRIM_AUTO_WRITE`

    .. usage::
        >>> scrimt = Scrim()
        >>> if scrim.shell == 'powershell.exe':
        ...     scrim.append('Write-Host $env:PATH')
        ...
        >>> scrim.write()
    '''

    def __init__(self, path=None, auto_write=None, shell=None, script=None):
        self.shell = init_value(shell, SCRIM_SHELL)
        self.path = init_value(path, SCRIM_PATH)
        self.auto_write = init_value(auto_write, SCRIM_AUTO_WRITE)
        self.script = init_value(script, SCRIM_SCRIPT)
        atexit.register(self.on_exit)

    def __repr__(self):
        args = (self.path, self.auto_write, self.shell, self.script)
        return '{}({}, {}, {}, {})'.format(self.__class__.__name__, *args)

    def to_string(self):
        '''Join this Scrims commands'''

        return '\n'.join(self)

    def write(self):
        '''Write this Scrims commands to its path'''

        if self.path is None:
            raise Exception('Scrims path is None')

        dirname = os.path.dirname(os.path.abspath(self.path))
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                raise OSError('Failed to create root for scrim output.')

        with open(self.path, 'w') as f:
            f.write(self.to_string())

    def on_exit(self):
        if not all([self.auto_write, self, self.script, self.path]):
            return

        self.write()


def get_scrim(path=None, auto_write=None, shell=None, script=None, cache={}):
    '''Usual method of getting a :class:`Scrim` instance. Each instance is
    cached so if you call get_scrim again with the same arguments you get the
    same instance.

    .. seealso:: :class:`Scrim`
    '''

    args = (path, auto_write, shell, script)
    if args not in cache:
        cache[args] = Scrim(*args)
    return cache[args]
