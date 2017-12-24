# -*- coding: utf-8 -*-
'''
==============
scrim.commands
==============
Implements functionality available across multiple shell scripting languages.
'''
from __future__ import absolute_import
import abc
from collections import namedtuple
from fstrings import f
import ntpath
import posixpath

ABC = abc.ABCMeta('ABC', (object,), {})
Command = namedtuple('Command', 'name args kwargs')
RawCommand = namedtuple('RawCommand', 'command required_shell')


class CommandExecutor(object):
    '''Forward commands to the specified ShellCommands implementation.
    RawCommands are returned as-is if the shell matches the RawCommands
    required_shell. You shouldn't need to use this class directly.
    '''

    def __call__(self, command, shell):

        if isinstance(command, Command):
            method = getattr(SHELL_COMMANDS[shell], command.name)
            return method(*command.args, **command.kwargs)

        elif isinstance(command, RawCommand):
            if shell == command.required_shell:
                return command.command

        else:
            raise TypeError(f(
                'command must be Command or RawCommand not {}', type(command)
            ))


class ShellCommands(ABC):
    '''Defines the interface for all ShellCommand implementations. These are
    the common commands we want to define for all shells.

    Sometimes commands are available across multiple shells like: cd. For
    clarity we define these commands for each implementation anyways instead of
    using inheritance.

    We only cover commands with functonality present in all the shells we
    support. Special cases can be handled using :meth:`Scrim.raw`.

    When choosing a method name for a command, generally use the most well
    known and widely used command. This will frequently come from bash. For
    example given the choice between `cat` in bash, `type` in batch, and
    `Get-Content` in powershell, we choose `cat` as the method name.

    In special cases we define methods that cover similar functionality for
    multiple shells like: `set_env` and `unset_env`. No shell has `set_env`
    or `unset_env` commands, but, powershell does have special syntax for
    setting and unsetting environment variables and bash has `export`.
    Therefore, we define `set_env` and `unset_env` for all implementations,
    even when batch has no direct analogy. This provides users with a
    memorable set of commands that cover all shells.

    Attributes:
        shell: Should match the SCRIM_SHELL value set in one of the scrim
            scripts. For example:

        - scrim.bat defines SCRIM_SHELL as cmd.exe
        - scrim.ps1 defines SCRIM_SHELL as powershell.exe
        - scrim.sh defines SCRIM_SHELL as bash
    '''

    @abc.abstractproperty
    def shell(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, expression):
        raise NotImplementedError

    @abc.abstractmethod
    def echo(self, message):
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, var, value):
        raise NotImplementedError

    @abc.abstractmethod
    def unset(self, var):
        raise NotImplementedError

    @abc.abstractmethod
    def set_env(self, var, value):
        raise NotImplementedError

    @abc.abstractmethod
    def unset_env(self, var):
        raise NotImplementedError

    @abc.abstractmethod
    def cd(self, path):
        raise NotImplementedError

    @abc.abstractmethod
    def pushd(self, path):
        raise NotImplementedError

    @abc.abstractmethod
    def popd(self):
        raise NotImplementedError

    @abc.abstractmethod
    def cat(self):
        raise NotImplementedError


class BatchCommands(ShellCommands):

    shell = 'cmd.exe'

    def execute(self, expression):
        return f('call {expression}')

    def echo(self, message):
        return f('echo {message}')

    def set(self, var, value):
        return f('set "{var}={value}"')

    def unset(self, var):
        return f('set "{var}="')

    set_env = set
    unset_env = unset

    def cd(self, path):
        path = ntpath.normpath(path)
        return f('cd {path}')

    def pushd(self, path):
        path = ntpath.normpath(path)
        return f('pushd {path}')

    def popd(self):
        return 'popd'

    def cat(self, path):
        path = ntpath.normpath(path)
        return f('type {path}')


class PowershellCommands(ShellCommands):

    shell = 'powershell.exe'

    def execute(self, expression):
        return f('Invoke-Expression {expression}')

    def echo(self, message):
        return f('Write-Host {message}')

    def set(self, var, value):
        return f('${var}={value}')

    def unset(self, var, value):
        return f('Remove-Variable {var}')

    def set_env(self, var, value):
        return f('$env:{var}={value}')

    def unset_env(self, var, value):
        return f('Remove-Item Env:{var}')

    def cd(self, path):
        path = ntpath.normpath(path)
        return f('cd {path}')

    def pushd(self, path):
        path = ntpath.normpath(path)
        return f('Push-Location -Path "{path}"')

    def popd(self):
        return 'Pop-Location'

    def cat(self, path):
        path = ntpath.normpath(path)
        return f('Get-Content {path}')


class BashCommands(ShellCommands):

    shell = 'bash'

    def execute(self, expression):
        return f('$({expression})')

    def echo(self, message):
        return f('echo {message}')

    def set(self, var, value):
        return f('{var}={value}')

    def unset(self, var):
        return f('unset {var}')

    def set_env(self, var, value):
        return f('export {var}={value}')

    def unset_env(self, var):
        return f('unset {var}')

    def cd(self, path):
        path = posixpath.normpath(path)
        return f('cd {path}')

    def pushd(self, path):
        path = posixpath.normpath(path)
        return f('pushd {path}')

    def popd(self):
        return 'popd'

    def cat(self, path):
        path = posixpath.normpath(path)
        return f('cat {path}')


SHELL_COMMANDS = dict((c.shell, c()) for c in ShellCommands.__subclasses__())
