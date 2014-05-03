import sys

from packtex import local_info


def arguments(command, args, fail=False):
	if not args:
		print 'Could not', command, 'package(s). Error:', command, 'command requires at least one argument.'
		if fail:
			sys.exit(-1)


def installed(command, package, fail=False):
	pkg = package.lower()
	if not local_info.installed(pkg):
		print 'Could not', command, 'package. Error:', package, 'is not installed.'
		if fail:
			sys.exit(-1)


def msg_ctan_down(fail=False):
	print 'Could not install package. Error: CTAN is down.'
	if fail:
		sys.exit(-1)


def msg_not_on_ctan(package, fail=False):
	print 'Could not install package. Error:', package, 'was not found on CTAN.'
	if fail:
		sys.exit(-1)


def msg_not_package(package, fail=False):
	print 'Could not install package. Error:', package, 'is a TeX system, not a package.'
	if fail:
		sys.exit(-1)


def msg_satisfied(info, parent, fail=False):
	print 'Requirement already satisfied (use \'update\' or \'upgrade\' to upgrade):', info,
	if parent:
		print '(from', parent + ')'
	else:
		print ''
	if fail:
		sys.exit(-1)


def updated(package, down, up, fail=False):
	if down == up and down != 'unversioned':
		print 'Requirement already up-to-date:', package
		if fail:
			sys.exit(-1)


def valid_command(command, fail=False):
	if command not in {'install', 'freeze', 'list', 'remove', 'show', 'uninstall', 'update', 'upgrade'}:
		print 'Could not run PackTeX. Error:', command[0], 'is not a valid command.'
		if fail:
			sys.exit(-1)
