# -*- coding: utf-8 -*-
__all__ = [
    'this_path', 'relative_path', 'bin_path', 'copy_templates',
    'parse_setup', 'get_console_scripts', 'get_parent_process'
]
import os
from types import ModuleType

this_path = os.path.dirname(__file__)


def relative_path(*args):
    '''os.path.join relative to this package'''

    return os.path.join(this_path, *args)


def bin_path(*args):
    '''os.path.join relative to this packages bin path'''

    return os.path.join(this_path, 'bin', *args)


def copy_templates(entry_point, auto_write, output_dir):
    '''Copy formatted templates from scrim/bin to output directory

    :param entry_point: Name of python console script
    :param auto_write: Sets SCRIM_AUTO_WRITE to True
    :param output_dir: Guess
    '''

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    scripts = []
    for f in os.listdir(bin_path()):
        ext = os.path.splitext(f)[-1]
        template = bin_path(f)
        destination = output_dir + '/' + entry_point + ext
        scripts.append(destination)

        with open(template, 'r') as f:
            code = f.read()
        code = code.replace('{{entry_point}}', entry_point)
        code = code.replace('{{auto_write}}', str(int(auto_write)))

        with open(destination, 'w') as f:
            f.write(code)

    return scripts


def get_parent_process(ok_names, limit=10):
    '''Walk up the process tree until we find a process we like.

    :param ok_names: Return the first one of these processes that we find
    '''
    try:
        import psutil
    except ImportError:
        raise Exception('get_parent_process relies on psutil...please install')

    depth = 0
    this_proc = psutil.Process(os.getpid())
    next_proc = parent = psutil.Process(this_proc.ppid())
    while depth < limit:

        if next_proc.name() in ok_names:
            return next_proc.name()

        next_proc = psutil.Process(next_proc.ppid())
        depth += 1

    return parent.name()


def parse_setup(filepath):
    '''Get the kwargs from the setup function in setup.py'''

    # TODO Need to also parse setup.cfg and merge with the data from below

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
    '''Parse and return a list of console_scripts from the setup_data'''

    # TODO support ini format of entry_points

    if 'entry_points' not in setup_data:
        return []

    console_scripts = setup_data['entry_points'].get('console_scripts', [])
    return [script.split('=')[0].strip() for script in console_scripts]
