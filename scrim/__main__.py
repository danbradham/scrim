#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pprint import pprint
import click
from .utils import copy_templates, parse_setup, get_console_scripts


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
    if not os.path.exists('setup.py'):
        raise click.UsageError('No setup.py file exists.')

    setup_data = parse_setup('setup.py')
    console_scripts = get_console_scripts(setup_data)

    scripts = []
    if all_entry_points and console_scripts:
        for entry in console_scripts:
            click.echo('Found entry_point: ' + entry)
            more_scripts = copy_templates(entry, auto_write, scripts_path)
            for script in more_scripts:
                click.echo('    Created ' + script)
            scripts.extend(more_scripts)

    elif entry_point:
        if not entry_point in console_scripts:
            click.echo(entry_point + ' not found in your setups entry_points')
            click.echo('You will need to add it afterward if you continue...\n')
            click.confirm('Do you want to continue?', abort=True)
        click.echo('\nCreating scripts for: ' + entry_point)
        more_scripts = copy_templates(entry_point, auto_write, scripts_path)
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
    setup_data = parse_setup('setup.py')
    pprint(setup_data)

if __name__ == '__main__':
    cli()
