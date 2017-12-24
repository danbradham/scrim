# -*- coding: utf-8 -*-
'''
===========
scrim.utils
===========
'''
from __future__ import absolute_import
import io
import os
from types import ModuleType
__all__ = [
    'this_path', 'relative_path', 'bin_path', 'copy_templates',
    'parse_setup', 'get_console_scripts', 'init_attr'
]

this_path = os.path.dirname(__file__)
NEWLINE_MAP = {
    '.ps1': '\r\n',
    '.bat': '\r\n',
    '.sh': '\n',
    '.csh': '\n',
    '.fish': '\n',
    '.zsh': '\n',
}


def relative_path(*args):
    '''os.path.join relative to this package'''

    return os.path.join(this_path, *args)


def bin_path(*args):
    '''os.path.join relative to this packages bin path'''

    return os.path.join(this_path, 'bin', *args)


def init_attr(value=None, default=None):
    '''Returns default if value is None'''
    if value is None:
        return default
    return value


def copy_templates(entry_point, py_entry_point, auto_write, output_dir):
    '''Copy formatted templates from scrim/bin to output directory

    Attributes:
        entry_point: Name of shell script
        py_entry_point: Name of python console script
        auto_write: Sets SCRIM_AUTO_WRITE to True
        output_dir: Guess
    '''

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scripts = []
    for f in os.listdir(bin_path()):
        ext = os.path.splitext(f)[-1]
        newline = NEWLINE_MAP.get(ext, '\n')
        template = bin_path(f)
        destination = output_dir + '/' + entry_point + ext
        scripts.append(destination)

        with io.open(template, 'r') as f:
            code = f.read()
        code = code.replace('{{entry_point}}', entry_point)
        code = code.replace('{{py_entry_point}}', py_entry_point)
        code = code.replace('{{auto_write}}', str(int(auto_write)))

        with io.open(destination, 'w', newline=newline) as f:
            f.write(code)

    return scripts


def parse_setup(filepath):
    '''Get the kwargs from the setup function in setup.py'''
    # TODO: Need to parse setup.cfg and merge with the data from below

    # Monkey patch setuptools.setup to capture keyword arguments
    setup_kwargs = {}

    def setup_interceptor(**kwargs):
        setup_kwargs.update(kwargs)

    import setuptools
    setuptools_setup = setuptools.setup
    setuptools.setup = setup_interceptor

    # Manually compile setup.py
    with open(filepath, 'r') as f:
        code = compile(f.read(), '', 'exec')
    setup = ModuleType('setup')
    exec(code, setup.__dict__)

    # Remove monkey patch
    setuptools.setup = setuptools_setup
    return setup_kwargs


def get_console_scripts(setup_data):
    '''Parse and return a list of console_scripts from setup_data'''

    # TODO: support ini format of entry_points
    # TODO: support setup.cfg entry_points as available in pbr

    if 'entry_points' not in setup_data:
        return []

    console_scripts = setup_data['entry_points'].get('console_scripts', [])
    return [script.split('=')[0].strip() for script in console_scripts]
