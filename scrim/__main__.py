#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from pprint import pprint
import click
from scrim.utils import copy_templates, parse_setup, get_console_scripts


@click.group()
def cli():
    '''Provides transparent scripts to wrap python cli tools.'''


@cli.command()
@click.option('--entry_point', default=None)
@click.option('--all_entry_points', is_flag=True, default=False)
@click.option('--auto_write', is_flag=True, default=True)
@click.option('--scripts_path', default='bin')
def add(entry_point, all_entry_points, auto_write, scripts_path):
    '''Add Scrim scripts for a python project'''

    click.echo()
    if not entry_point and not all_entry_points:
        raise click.UsageError(
            'Missing required option: --entry_point or --all_entry_points'
        )
    if not os.path.exists('setup.py'):
        raise click.UsageError('No setup.py found.')

    setup_data = parse_setup('setup.py')
    console_scripts = get_console_scripts(setup_data)

    scripts = []
    if all_entry_points and console_scripts:

        # Make sure our entry points start with py
        for entry in console_scripts:
            if not entry.startswith('py'):
                click.echo('Your python entry_points must start with py.')
                click.echo('Found: ' + entry)
                raise click.Abort()

        for entry in console_scripts:
            click.echo('Found entry_point: ' + entry)
            py_entry_point = entry
            entry_point = entry[2:]
            more_scripts = copy_templates(
                entry_point,
                py_entry_point,
                auto_write,
                scripts_path
            )

            for script in more_scripts:
                click.echo('    Created ' + script)

            scripts.extend(more_scripts)

    elif entry_point:
        if not entry_point.startswith('py'):
            click.echo('Your python entry_points must start with py.')
            raise click.Abort()
        if entry_point not in console_scripts:
            click.echo(entry_point + ' not found in your setups entry_points')
            click.echo('You will need to add it afterward if you continue...')
            click.echo('')
            click.confirm('Do you want to continue?', abort=True)

        click.echo('\nCreating scripts for: ' + entry_point)
        py_entry_point = entry_point
        entry_point = entry_point[2:]
        more_scripts = copy_templates(
            entry_point,
            py_entry_point,
            auto_write,
            scripts_path
        )

        for script in more_scripts:
            click.echo('    Created ' + script)

        scripts.extend(more_scripts)

    click.echo('\n\nAdd the following section to your package setup:\n')
    click.echo('scripts=[')
    for script in scripts:
        click.echo("    '{}',".format(script))
    click.echo('],')


@cli.command()
def print_setup():
    '''Print setup.py setup kwargs'''
    setup_data = parse_setup('setup.py')
    pprint(setup_data)


if __name__ == '__main__':
    cli()
