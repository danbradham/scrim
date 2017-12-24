# -*- coding: utf-8 -*-
'''
=========
scrim.api
=========
'''
from __future__ import absolute_import
import os
import atexit
from fstrings import f
from scrim.globals import (
    SHELLS,
    SCRIM_AUTO_WRITE,
    SCRIM_PATH,
    SCRIM_SHELL,
    SCRIM_SCRIPT
)
from scrim.commands import CommandExecutor, Command, RawCommand
from scrim.utils import init_attr
__all__ = ['Scrim', 'get_scrim']


try:
    basestring
except NameError:
    basestring = (str, bytes)


class Scrim(object):
    '''
    Arguments:
        shell: Name of the shell process. Defaulst to :envvar:`SCRIM_SHELL`
        path: Path to temporary scrim file. Defaults to :envvar:`SCRIM_PATH`
        auto_write: Write scrim file on program exit. Defaults to
                    :envvar:`SCRIM_AUTO_WRITE`
        script: Path to scrim script. Defaults to :envvar:`SCRIM_AUTO_WRITE`

    Usage:
        >>> scrim = Scrim()
        >>> scrim.echo('Hello World!')
        >>> scrim.to_cmd()
        'echo Hello World!'
    '''

    def __init__(self, path=None, auto_write=None, shell=None, script=None):
        self.shell = init_attr(shell, SCRIM_SHELL)
        self.path = init_attr(path, SCRIM_PATH)
        self.auto_write = init_attr(auto_write, SCRIM_AUTO_WRITE)
        self.script = init_attr(script, SCRIM_SCRIPT)
        self.command_executor = CommandExecutor()
        self.commands = []
        atexit.register(self.on_exit)

    def __repr__(self):
        args = (
            repr(self.path),
            repr(self.auto_write),
            repr(self.shell),
            repr(self.script)
        )
        return f("<{}>({}, {}, {}, {})", self.__class__.__name__, *args)

    def _add(self, name, *args, **kwargs):
        '''Appends a command to the scrims list of commands. You should not
        need to use this.'''

        self.commands.append(Command(name, args, kwargs))

    def execute(self, expression):
        '''Execute the specified expression or script.

        Arguments:
            expression (str): An expression or script file to execute
        '''

        self._add('execute', expression)

    def echo(self, message):
        '''Write to stdout.

        Arguments:
            message (str): Message to write
        '''

        self._add('echo', message)

    def set(self, var, value):
        '''Set a variable.

        Arguments:
            var (str): variable name
            value (Any): value to write
        '''

        self._add('set', var, value)

    def unset(self, var):
        '''Unset a variable.

        Arguments:
            var (str): variable name
        '''

        self._add('unset', var)

    def set_env(self, var, value):
        '''Set an environment variable. Depending on shell this is identical
        to :meth:`set`

        Arguments:
            var (str): variable name
            value (Any): value to write
        '''

        self._add('set_env', var, value)

    def unset_env(self, var):
        '''Unset an environment variable. Depending on shell this is identical
        to :meth:`unset`

        Arguments:
            var (str): variable name
        '''

        self._add('unset_env', var)

    def cd(self, path):
        '''Change directory.

        Arguments:
            path (str): Path to directory
        '''
        self._add('cd', path)

    def pushd(self, path):
        '''Push a directory onto the stack and navigate to it.

        Arguments:
            path (str): Path to directory
        '''
        self._add('pushd', path)

    def popd(self):
        '''Pop a directory from the stack and navigate to previous directory
        on stack
        '''

        self._add('popd')

    def raw(self, command, required_shell):
        '''Append a raw command to the scrim. This text will be appeneded to
        the output of :meth:`scrim.to_string` verbatim. Use required_shell to
        specify the shell which this raw command is applicable to.

        Examples:
            >>> scrim = Scrim()
            >>> scrim.raw('cat text.txt', 'bash')
            >>> scrim.raw('type text.txt', 'cmd.exe')
            >>> scrim.raw('Get-Content text.txt', 'powershell.exe')
            >>> scrim.to_bash()
            'cat text.txt'
            >>> scrim.to_cmd()
            'type text.txt'
            >>> scrim.to_powershell()
            'Get-Content text.txt'
        '''

        if not isinstance(command, basestring):
            raise TypeError(f('{command} must be a string'))

        if required_shell not in SHELLS:
            raise ValueError(f('{required_shell} must be one of {SHELLS}'))

        self.commands.append(RawCommand(command, required_shell))

    def to_string(self, shell=None):
        '''Use the command executor to retrieve the text of the scrim script
        compatible with the provided shell. If no shell is provided, use
        :attr:`scrim.shell`.

        Attributes:
            shell (str): Which shell should we return a script for
                cmd.exe, powershell.exe, bash...

        Returns:
            str
        '''

        shell = shell or self.shell
        lines = []
        for c in self.commands:
            text = self.command_executor(c, shell)
            if text is not None:
                lines.append(text)

        return '\n'.join(lines)

    def to_cmd(self):
        '''scrim.to_powershell() == scrim.to_string('powershell')

        Returns:
            str
        '''

        return self.to_string('cmd.exe')

    def to_powershell(self):
        '''scrim.to_powershell() == scrim.to_string('powershell')

        Returns:
            str
        '''

        return self.to_string('powershell.exe')

    def to_bash(self):
        '''scrim.to_bash() == scrim.to_string('bash')

        Returns:
            str
        '''

        return self.to_string('bash')

    def write(self):
        '''Write this Scrims commands to its path'''

        if self.path is None:
            raise Exception('Scrim.path is None')

        dirname = os.path.dirname(os.path.abspath(self.path))
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                raise OSError('Failed to create root for scrim output.')

        with open(self.path, 'w') as f:
            f.write(self.to_string())

    def on_exit(self):
        '''atexit callback. If :attr:`Scrim.auto_write` is True write the
        scrim to :attr:`Scrim.path` as :attr:`Scrim.shell`'''

        if not all([self.auto_write, self.commands, self.script, self.path]):
            return

        self.write()


def get_scrim(path=None, auto_write=None, shell=None, script=None, cache={}):
    '''Get a :class:`Scrim` instance. Each instance is cached so if you call
    get_scrim again with the same arguments you get the same instance.

    See also:
        :class:`Scrim`
    '''

    args = (path, auto_write, shell, script)
    if args not in cache:
        cache[args] = Scrim(*args)
    return cache[args]
