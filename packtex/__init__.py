import argparse
import sys

from packtex.manage import info, install, show, uninstall, upgrade

__version__ = 'alpha.2'


def get_params():
	parser = argparse.ArgumentParser(description='PackTeX is a package manager for all TeX derivatives', usage='packtex [-h] [-v] <command> <package name(s)>', add_help=False)
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

	if command[0] == 'install':
		if not packages:
			print 'Cannot install packages. Error: install command requires argument(s).'
			sys.exit(-1)

		for package in packages:
			install(package)
	elif command[0] == 'list':
		info()
	elif command[0] in {'remove', 'uninstall'}:
		if not packages:
			print 'Cannot uninstall packages. Error: uninstall command requires argument(s).'
			sys.exit(-1)

		for package in packages:
			uninstall(package)
	elif command[0] == 'show':
		if not packages:
			print 'Cannot show packages. Error: show command requires argument(s).'
			sys.exit(-1)

		for package in packages:
			show(package)
	elif command[0] in {'update', 'upgrade'}:
		if not packages:
			print 'Cannot upgrade packages. Error: upgrade command requires argument(s).'
			sys.exit(-1)

		for package in packages:
			upgrade(package)
	else:
		print 'Could not run PackTeX. Error: ' + command[0] + ' is not a valid command.'
		sys.exit(-1)
