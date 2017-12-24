# -*- coding: utf-8 -*-
'''
=============
scrim.globals
=============
Defines variables passed into the python script via Environment Variables by
scrim scripts. If SCRIM_SHELL is None, then the python script was not executed
by a scrim script.

    SHELLS (list): list of available shells
    SCRIM_SHELL (str): Parent shell, one of the above SHELLS
    SCRIM_PATH (str): Path to output shell script
    SCRIM_AUTO_WRITE (bool): Write to SCRIM_PATH when python exits?
    SCRIM_SCRIPT (str): Path to the scrim script that invoked python
    SCRIM_DEBUG (bool): Is scrim script running in debug mode?
'''
from __future__ import absolute_import
import os
__all__ = [
    'SHELLS', 'SCRIM_SHELL', 'SCRIM_PATH', 'SCRIM_AUTO_WRITE',
    'SCRIM_SCRIPT', 'SCRIM_DEBUG'
]

SHELLS = [
    'powershell.exe',
    'cmd.exe',
    'bash'
]
SCRIM_SHELL = os.environ.get('SCRIM_SHELL', None)
SCRIM_PATH = os.environ.get('SCRIM_PATH', None)
SCRIM_AUTO_WRITE = bool(os.environ.get('SCRIM_AUTO_WRITE', False))
SCRIM_SCRIPT = os.environ.get('SCRIM_SCRIPT', None)
SCRIM_DEBUG = bool(os.environ.get('SCRIM_DEBUG', False))
