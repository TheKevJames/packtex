import os
import re
import shutil
import sys
import urllib

from packtex import ctan, local


tex_dir, install_dir, discard_dir, metadata = local.get_dirs()
if not os.path.isfile(metadata):
	open(metadata, 'w').close()


def info():
	installed = []
	meta = open(metadata, 'r').readlines()
	for line in meta:
		installed.append(line.replace('\n', ''))

	installed.sort()
	for inst in installed:
		print '=='.join(inst.split('==')[:2])


def install(package):
	if local.installed(package):
		print 'Could not install package ' + package + '. Error: package is already installed'
	else:
		version, rows, error = ctan.get_data(package)
		if error:
			pass
			# print "\tError:", package, error
			# print 'Could not install package ' + package + '. Error: package is installed by default or is a TeX framework'
		else:
			provides = []
			for row in rows:
				if isinstance(row, unicode):
					filename = re.sub(r'.*/(.*)\.(.*)', r'\1.\2', row)
				else:
					filename = row.td.get_text()
				if len(filename) > 4 and filename[-4] == '.':
					filetype = filename[-3:]
				elif len(filename) > 3 and filename[-3] == '.':
					filetype = filename[-2:]
				else:
					filetype = None
				print "\t", filename
				directory = local.get_path(filetype, package)
				if not os.path.exists(directory):
					os.makedirs(directory)

				path = os.path.join(directory, filename)
				if isinstance(row, unicode):
					url = row
				else:
					url = row.a.get('href')
				if not url.startswith('http'):
					url = 'http://www.ctan.org' + url
				urllib.urlretrieve(url, path)
				if path[-3:] in {'bst', 'cls', 'sty'}:
					provides.append(path)

			while os.path.exists(install_dir):
				provides, requires = local.install_sources(provides, package)
				for req in requires:
					if not local.installed(req) and not local.provided(req):
						install(req)
			provides = list(set(provides))
			provides.sort()

			requires = []
			for fl in provides:
				requires.extend(local.get_requirements(fl))
			requires = list(set(requires))
			for pack in provides:
				name = re.sub(r'.*/(.*)\.(.*)', r'\1', pack)
				if name in requires:
					requires.remove(name)
			requires.sort()

			with open(metadata, 'a') as meta:
				meta.write('=='.join([package, version, '='.join(provides), '='.join(requires)]))
				meta.write('\n')

			for req in requires:
				if not local.installed(req) and not local.provided(req):
					install(req)

	if os.path.exists(discard_dir):
		shutil.rmtree(discard_dir)



def show(package):
	if local.installed(package):
		data = local.get_data(package)
		print '-----'
		print 'Name:', data[0]
		print 'Version:', data[1]
		print 'Provides:', ', '.join([re.sub(r'(.*/)|(\n)', '', fl) for fl in data[2].split('=')])
		print 'Requires:', ', '.join(data[3].split('=')).replace('\n', '')
	else:
		print 'Could not show details for ' + package + '. Error: package is not installed'


def uninstall(package):
	installed = open(metadata, 'r').readlines()
	for inst in installed:
		data = inst.split('==')
		if data[0] == package:
			for fl in data[2].split('='):
				os.remove(fl.replace('\n', ''))

			with open(metadata, 'w') as meta:
				for write_inst in installed:
					if inst != write_inst:
						meta.write(write_inst)
				return

	print 'Could not uninstall package ' + package + '. Error: package is not installed'
	sys.exit(-1)


def upgrade(package):
	exists = None
	installed = open(metadata, 'r').readlines()
	for inst in installed:
		data = inst.split('==')
		if data[0] == package:
			exists = data[1]
			break
	if not exists:
		print 'Could not update package ' + package + '. Error: package is not installed'
		sys.exit(-1)

	ctan = ctan.get_data(package)
	version = ctan.get_version(ctan)
	if version == exists:
		print 'Could not update package ' + package + '. Error: package is alread at latest version'
		return

	uninstall(package)
	install(package)
