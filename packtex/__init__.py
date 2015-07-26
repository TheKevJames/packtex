import argparse

from . import error
from .commands import (info, install, show, uninstall, upgrade)


__version__ = 'v0.1.9-beta'


def get_params():
    parser = argparse.ArgumentParser(description='PackTeX is a package manager for all *TeX derivatives.', usage='packtex [-h] [-v] <command> <package name(s)>', add_help=False)
    required = parser.add_argument_group('required')
    required.add_argument('command', nargs=1, help='Command to execute')
    optional = parser.add_argument_group('options')
    optional.add_argument('packages', nargs='*', help='Name of package(s) to run <command> against (if command calls for packages)')
    system = parser.add_argument_group('information')
    system.add_argument('-h', '--help', action='help')
    system.add_argument('-v', '--version', action='version', version='PackTeX v' + __version__)
    args = parser.parse_args()

    return args.command, args.packages


def execute_from_command_line():
    command, packages = get_params()
    error.valid_command(command[0], fail=True)

    if command[0] in {'install'}:
        error.arguments(command[0], packages, fail=True)

        install.run(packages)
    elif command[0] in {'freeze', 'list'}:
        info.run(command[0])
    elif command[0] in {'remove', 'uninstall'}:
        error.arguments(command[0], packages, fail=True)

        uninstall.run(packages)
    elif command[0] in {'reinstall'}:
        error.arguments(command[0], packages, fail=True)

        uninstall.run(packages)
        install.run(packages)
    elif command[0] == 'show':
        error.arguments(command[0], packages, fail=True)

        show.run(packages)
    elif command[0] in {'update', 'upgrade'}:
        error.arguments(command[0], packages, fail=True)

        upgrade.run(packages)
