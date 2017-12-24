# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from functools import partial
import shutil
from scrim import get_scrim, copy_templates
from scrim.globals import *

data_path = partial(os.path.join, os.path.dirname(__file__), '.testdata')


def setup_module():
    if not os.path.exists(data_path()):
        os.makedirs(data_path())


def teardown_module():
    shutil.rmtree(data_path())


def test_get_scrim():
    '''Test scrim.get_scrim'''

    assert id(get_scrim()) == id(get_scrim())

    scrim = get_scrim()
    assert scrim.path == SCRIM_PATH
    assert scrim.shell == SCRIM_SHELL
    assert scrim.auto_write == SCRIM_AUTO_WRITE
    assert scrim.script == SCRIM_SCRIPT

    kwargs = dict(
        path=data_path('.scrim'),
        auto_write=False,
        shell='powershell.exe',
        script=None
    )
    s = get_scrim(**kwargs)
    assert id(s) == id(get_scrim(**kwargs))


def test_scrim():
    '''Test scrim.write'''

    scrim = get_scrim(data_path('.scrim'), shell='cmd.exe')
    scrim.raw('line 01', scrim.shell)
    scrim.raw('line 02', scrim.shell)
    scrim.write()

    assert os.path.exists(scrim.path)

    with open(scrim.path, 'r') as f:
        text = f.read()

    assert scrim.to_string() == text

    scrim = get_scrim(
        path=data_path('.scrim2'),
        auto_write=False,
        shell='cmd.exe',
        script='null'
    )
    scrim.raw('Hello', scrim.shell)
    scrim.on_exit()
    assert not os.path.exists(scrim.path)

    scrim.auto_write = True
    scrim.on_exit()
    assert os.path.exists(scrim.path)
    scrim.auto_write = False


def test_copy_templates():
    '''Test scrim.utils.copy_templates'''

    scripts = copy_templates('test', 'pytest', True, data_path('bin'))
    assert all([os.path.exists(s) for s in scripts])
