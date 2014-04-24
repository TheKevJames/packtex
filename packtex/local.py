import os
import re
import shutil
import subprocess


paths = {
	'afm': ['TEXMF', 'fonts', 'afm'],
	'bst': ['TEXMF', 'bibtex', 'bst', 'PACKAGE'],
	'cls': ['TEXMF', 'tex', 'latex', 'base'],
	'def': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
	'dtx': ['TEXMF', 'install'],
	'dvi': ['TEXMF', 'install'],
	'enc': ['TEXMF', 'fonts', 'enc'],
	'etx': ['TEXMF', 'install'],
	'fd':  ['TEXMF', 'tex', 'latex', 'fss'],
	'ins': ['TEXMF', 'install'],
	'ist': ['TEXMF', 'discard'],
	'log': ['TEXMF', 'discard'],
	'lox': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
	'map': ['TEXMF', 'fonts', 'map'],
	'mtx': ['TEXMF', 'install'],
	'otf': ['FONT'],
	'pdf': ['TEXMF', 'doc'],
	'pfb': ['TEXMF', 'fonts', 'type1'],
	'sty': ['TEXMF', 'tex', 'latex', 'PACKAGE'],
	'tex': ['TEXMF', 'install'],
	'txt': ['TEXMF', 'discard'],
	'ttf': ['TEXMF', 'fonts', 'truetype'],
	'vf':  ['TEXMF', 'fonts', 'vf'],
}


font_dir = os.path.join(os.environ['HOME'], '.fonts')
tex_dir = os.path.join(os.environ['HOME'], 'texmf')
discard_dir = os.path.join(tex_dir, 'discard')
install_dir = os.path.join(tex_dir, 'install')
metadata = os.path.join(tex_dir, '.metadata')


def get_data(package):
	for line in open(metadata, 'r').readlines():
		splt = line.split('==')
		if splt[0] == package:
			return splt


def get_dirs():
	return tex_dir, install_dir, discard_dir, metadata


def get_path(filetype, package):
	if filetype:
		try:
			path = '/'.join(paths[filetype])
		except KeyError:
			path = '/'.join(paths['log'])
	else:
		path = '/'.join(paths['sty'])
	path = path.replace('FONT', font_dir)
	path = path.replace('TEXMF', tex_dir)
	path = path.replace('PACKAGE', package)
	return path


def get_requirements(fl):
	requires = []
	multiline = False
	for line in open(fl, 'r').readlines():
		if line.startswith(r'\RequirePackage'):
			if re.search(r'\{.*?\w.*?\}', line):
				requires.extend([pack.strip(' ') for pack in re.sub(r'\\RequirePackage(WithOptions)?.*?\{(.*)\}.*\n', r'\2', line).split(',')])
			else:
				multiline = True
		elif multiline:
			if '}' in line:
				multiline = False
			elif '{' in line:
				pass
			else:
				requires.append(re.sub(r'\s*(\w+).*\n', r'\1', line).strip(' '))
	return requires


def get_valid_filetypes():
	return paths.keys()


def installed(package):
	for line in open(metadata, 'r').readlines():
		if line.split('==')[0] == package:
			return True
	return False


def install_sources(provides, package):
	old_files = []
	files = []
	while True:
		old_files.append(files)
		files = os.listdir(install_dir)
		if files in old_files:
			break

		requires = []
		for f in files:
			if not os.path.isfile(os.path.join(install_dir, f)):
				continue

			if f.endswith('dtx'):
				for other in files:
					if other.endswith('ins'):
						continue

				try:
					print '  building', f[:-4]
					subprocess.call(['tex', '-interaction=batchmode', f], stdout=open(os.devnull, 'w'), cwd=install_dir)

					dest_dir = get_path('sty', package)
					if not os.path.exists(dest_dir):
						os.makedirs(dest_dir)
					dest_file = f[:-3] + 'sty'

					orig = os.path.join(install_dir, dest_file)
					dest = os.path.join(dest_dir, dest_file)
					os.rename(orig, dest)
					for t in ('dtx', 'ins', 'tex'):
						fl = orig[:-3] + t
						if os.path.isfile(fl):
							os.remove(fl)

					provides.append(dest)
				except OSError:
					tex_dep = os.path.join(install_dir, f[:-3] + 'tex')
					if os.path.isfile(tex_dep):
						requires.extend(get_requirements(tex_dep))
			elif f.endswith('dvi'):
				# subprocess.call(['dvipdfm', f], stdout=open(os.devnull, 'w'), cwd=install_dir)
				os.remove(os.path.join(install_dir, f))
			elif f.endswith('ins'):
				local_requires = []
				tex_dep = os.path.join(install_dir, f[:-3] + 'tex')
				if os.path.isfile(tex_dep):
					requires.extend(get_requirements(tex_dep))

				for req in list(local_requires):
					if installed(req) or provided(req):
						local_requires.remove(req)
					for pack in provides:
						if req + '.sty' == re.sub(r'.*/(.*)\.(.*)', r'\1.\2', pack):
							local_requires.remove(req)

				if local_requires:
					requires.extend(local_requires)
				else:
					print '  building', f[:-4]
					subprocess.call(['latex', '-interaction=batchmode', f], stdout=open(os.devnull, 'w'), cwd=install_dir)

					for line in open(os.path.join(install_dir, f), 'r').readlines():
						if line.startswith(r'\generate'):
							if 'file' in line:
								sty, dtx = re.sub(r'\\generate.*\\file.*?\{(.*\..*)\}.*\\from.*?\{(.*\.[^\}]*)\}.*', r'\1\t\2', line).split('\t')
								sty, dtx = sty.replace('\n', ''), dtx.replace('\n', '')

								filetype = sty[-3:]
								if filetype == 'tex':
									filetype = 'sty'
								dest_dir = get_path(filetype, package)
								if not os.path.exists(dest_dir):
									os.makedirs(dest_dir)

								orig = os.path.join(install_dir, sty)
								dest = os.path.join(dest_dir, sty)
								os.rename(orig, dest)

								dtx_path = os.path.join(install_dir, dtx)
								if os.path.isfile(dtx_path):
									os.remove(dtx_path)

								if 'discard' not in dest_dir:
									provides.append(dest)

					os.remove(os.path.join(install_dir, f))
			elif f.endswith('pdf'):
				dest_dir = get_path('pdf', package)
				if not os.path.exists(dest_dir):
					os.makedirs(dest_dir)

				orig = os.path.join(install_dir, f)
				dest = os.path.join(dest_dir, f)
				os.rename(orig, dest)
			elif f.endswith('sty'):
				dest_dir = get_path('sty', package)
				if not os.path.exists(dest_dir):
					os.makedirs(dest_dir)

				orig = os.path.join(install_dir, f)
				dest = os.path.join(dest_dir, f)
				os.rename(orig, dest)
				provides.append(dest)

	if not requires:
		for f in os.listdir(install_dir):
			if f.endswith('tex'):
				dest_dir = get_path('sty', package)
				if not os.path.exists(dest_dir):
					os.makedirs(dest_dir)

				orig = os.path.join(install_dir, f)
				dest = os.path.join(dest_dir, f)
				os.rename(orig, dest)
			else:
				dest_dir = get_path(f[-3:], package)
				if not os.path.exists(dest_dir):
					os.makedirs(dest_dir)

				orig = os.path.join(install_dir, f)
				dest = os.path.join(dest_dir, f)
				os.rename(orig, dest)
		shutil.rmtree(install_dir)
	return provides, requires


def provided(package):
	for line in open(metadata, 'r').readlines():
		for provide in line.split('==')[2]:
			if package in provide:
				return True
	return False
