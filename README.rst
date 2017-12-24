=====
Scrim
=====
.. image:: https://travis-ci.org/danbradham/scrim.svg?branch=master
    :target: https://travis-ci.org/danbradham/scrim

A *scrim* is a piece of cloth that's opaque until lit from behind. Like a scrim, **Scrim** provides opaque scripts to wrap python command line tools and a transparent python api to send shell commands up to the user's shell.


Why would I need Scrim?
=======================
When writing command line tools in python, changes to--let's say--environment variables, don't persist when the python process exits. This means we can't write certain types of tools in pure python, we need to revert to our shell's scripting language instead. That's why tools like virtualenvwrapper are written in shell scripting languages instead of pure python. **Scrim** provides opaque shell scripts that wrap your python cli, so you can continue writing the interfaces for your python programs in python.


How does it work?
=================
.. image:: images/scrim_diagram.png

In this diagram the *Scrim Script* is the opaque shell script provided by the scrim package. Following along with the diagram, the *User* calls the cli command. This invokes the *Scrim Script* which sets these environment variables:

  - **SCRIM_SHELL** - name of the shell process (powershell.exe, cmd.exe)
  - **SCRIM_PATH** - path to temp script which python will write
  - **SCRIM_SCRIPT** - full path to the Scrim Script
  - **SCRIM_AUTO_WRITE** - whether or not to automatically write the temp script when python exits.

Then the *Scrim Script* invokes the actual *Python CLI* passing all arguments from the *User*. The *Python CLI* can now use the scrim api to append commands to a list. When the python program exits, the list of commands is written to a temporary script file. The *Scrim Script* now continues and executes the temporary script file if it exists. Finally the *Scrim Script* removes any temporary files and unsets the above environment variables.


Quickstart
==========
First add **Scrim** scripts to your project using **Scrim's** cli.

::

    > cd mytool
    > scrim add --entry_point pymytool

    Creating scripts for: pymytool
        Created bin/mytool.bat
        Created bin/mytool.ps1
        Created bin/mytool.sh

    Add the following section to your package setup:

    scripts=[
        'bin/mytool.bat',
        'bin/mytool.ps1',
        'bin/mytool.sh'
    ],

Assume that *mytool* is a python project containing a setup.py file. Here we've provided `scrim add` with the name of the entry_point to our python cli. If you've got multiple entry_points already defined in your package you can use::

    > scrim add --all_entry_points
    ...

This will add *Scrim Scripts* to each console_script you've defined in entry_points.

Now that you're project has Scrim added to it let's take a look at the python side.

::

    import click
    from scrim import get_scrim
    scrim = get_scrim()

    @click.command()
    def mytool():
        scrim.set_env('MYTOOL', "Hello World!")

    if __name__ == '__main__':
        mytool()

We use `get_scrim` to get an instance of `Scrim`. Then we append commands to the scrim and those will be written to a shell script when python exits. After python exits the *scrim script* will check to see if a shell script exists and execute it. In this case the environment variable *MYTOOL* will be set to *Hello World!*.


Installing a library that uses Scrim
====================================

Windows
-------
A simple `pip install` will do you. The scrim scripts
will be picked up normally from your command line, you won't even know they
are there!

Unix Systems
------------
In addition to your standard `pip install` you also have to source the scrim
script after installation. It usually ends up in one of these locations:

  - {virtualenv_path}/bin/{entry_point}.sh
  - /usr/local/bin/{entry_point}.sh


Supported Shells
================

  - bash
  - cmd
  - powershell


To Do
=====

  - More tests...
  - Support more shells: fish, csh, zsh...
  - Add more commands to the `Scrim`
  - Extend scrim cli to better support a variety of entry_points scenarios

    - Currently we only capture `setup` entry_points when defined as a
      dict.
    - We also only support entry_points beginning with py.
    - Parse setup.cfg in addition to setup.py


Tests
=====
Use nose to manually run the scrim test suite.

::

    > nosetests -v -s --with-doctest
