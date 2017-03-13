# -*- coding: utf-8 -*-
__all__ = [
    'SHELLS', 'SCRIM_SHELL', 'SCRIM_PATH', 'SCRIM_AUTO_WRITE',
    'SCRIM_SCRIPT', 'SCRIM_DEBUG'
]
import os
from .utils import get_parent_process

SHELLS = [
    'powershell.exe',
    'cmd.exe'
]
SCRIM_SHELL = os.environ.get('SCRIM_SHELL', None)
SCRIM_PATH = os.environ.get('SCRIM_PATH', None)
SCRIM_AUTO_WRITE = int(os.environ.get('SCRIM_AUTO_WRITE', False))
SCRIM_SCRIPT = os.environ.get('SCRIM_SCRIPT', None)
SCRIM_DEBUG = os.environ.get('SCRIM_DEBUG', False)
