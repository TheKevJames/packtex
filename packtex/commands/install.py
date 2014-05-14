import os
import re
import shutil
import subprocess
import sys
import urllib

from .. import (ctan, error, local_info, locations)


def empty(fpath):
    if os.path.isfile(fpath):
        if os.path.getsize(fpath) > 0:
            return False
        else:
            return True
    else:
        return True


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
        elif line.startswith(r'\usepackage'):
            if re.search(r'\{.*?\w.*?\}', line):
                requires.extend([pack.strip(' ') for pack in re.sub(r'\\usepackage.*?\{(.*)\}.*\n', r'\1', line).split(',')])
            else:
                multiline = True
        elif line.startswith(r'\input'):
            if re.search(r'\\input\s.+\n', line):
                requires.append(re.sub(r'\\input\s(.+)(\.|\s\%).*\n', r'\1', line))
            else:
                pass
    return requires


class FolderDiff(object):
    """Folder monitoring functionality for small code-blocks"""
    def __init__(self):
        self.dir = locations.get_tex_dir()

        self.diff = None
        self.final = None
        self.initial = None

    def get_state(self):
        """Get the current directory state"""
        return [os.path.join(dp, f) for dp, _, fn in os.walk(self.dir) for f in fn]

    def __enter__(self):
        self.initial = self.get_state()
        return self

    def __exit__(self, *args):
        self.final = self.get_state()
        self.diff = [item for item in self.final if item not in self.initial]


class ProgressBar(object):
    """Command line progress bar"""
    def __init__(self, msg, length):
        self.current = 0
        self.factor = 1
        if length > 10:
            self.factor = length / 10
            mod = length % 10
            length = 10 + mod

        sys.stdout.write(msg + ' [%s] (downloading %s files)' % ((' ' * length), length))
        sys.stdout.flush()
        sys.stdout.write('\b' * (length + 22 + len(str(length))))

    def __enter__(self):
        self.current = 0
        return self;

    def tick(self):
        """Add one tick to progress bar"""
        self.current += 1
        if self.current == self.factor:
            sys.stdout.write('+')
            sys.stdout.flush()
            self.current = 0

    def __exit__(self, *args):
        sys.stdout.write('\n')


def download(package, soup, provides):
    if isinstance(soup, unicode):
        filename = re.sub(r'.*/(.*)\.(.*)', r'\1.\2', soup)
    else:
        filename = soup.td.get_text()

    if len(filename) > 4 and filename[-4] == '.':
        filetype = filename[-3:]
    elif len(filename) > 3 and filename[-3] == '.':
        filetype = filename[-2:]
    else:
        filetype = None
    directory = locations.get_path(filetype, package)
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = os.path.join(directory, filename)
    if isinstance(soup, unicode):
        url = soup
    else:
        url = soup.a.get('href')
    if not url.startswith('http'):
        url = 'http://www.ctan.org' + url
    urllib.urlretrieve(url, path)

    if len(filename) > 4 and path[-4:] in {'.bst', '.cls', '.sty'}:
        provides.append(path)


def run_workflow(package, parent, version, rows):
    with FolderDiff() as folder:
        print 'Downloading/unpacking', package,
        if parent:
            print '(from', parent + ')'
        else:
            print ''

        provides = []
        with ProgressBar('  Downloading ' + package, len(rows)) as progress:
            for row in rows:
                download(package, row, provides)
                progress.tick()

        failed_dependency = False
        while os.path.exists(locations.get_install_dir()) and not failed_dependency:
            provides, requires = install_sources(provides, package)
            for req in requires:
                if not local_info.installed(req) and not local_info.provided(req):
                    if run(req, package):
                        provides.append(req)
                    else:
                        failed_dependency = True
                        shutil.rmtree(locations.get_install_dir())

        provides = list(set(provides))
        provides.sort()

        requires = []
        for fl in list(provides):
            try:
                requires.extend(get_requirements(fl))
            except IOError:
                provides.remove(fl)
        requires = list(set(requires))
        for pack in provides:
            name = re.sub(r'.*/(.*)\.(.*)', r'\1', pack)
            if name in requires:
                requires.remove(name)
        requires.sort()

        with open(locations.get_metadata_file(), 'a') as meta:
            meta.write('=='.join([package, version, '='.join(provides), '='.join(requires)]))
            meta.write('\n')

        for req in requires:
            if not local_info.installed(req) and not local_info.provided(req):
                if run(req, package):
                    pass
                else:
                    failed_dependency = True

        if os.path.exists(locations.get_discard_dir()):
            shutil.rmtree(locations.get_discard_dir())

    directory = locations.get_path(None, package)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(os.path.join(directory, '.log'), 'w') as txt:
        for line in folder.diff:
            txt.write(line)
            txt.write('\n')

    if failed_dependency:
        print 'Package may have installed incorrectly. Error: a dependency was not found on CTAN.'


def install_sources(provides, package):
    old_files = []
    files = []
    while True:
        old_files.append(files)
        files = os.listdir(locations.get_install_dir())
        if files in old_files:
            break

        requires = []
        for f in files:
            if not os.path.isfile(os.path.join(locations.get_install_dir(), f)):
                continue

            if f.endswith('.dtx'):
                for other in files:
                    if other.endswith('.ins'):
                        continue
                    elif other.endswith('.drv'):
                        continue

                try:
                    print '  building', f[:-4]
                    subprocess.call(['tex', '-interaction=batchmode', f], stdout=open(os.devnull, 'w'), cwd=locations.get_install_dir())

                    dest_dir = locations.get_path('sty', package)
                    if not os.path.exists(dest_dir):
                        os.makedirs(dest_dir)
                    dest_file = f[:-3] + 'sty'

                    orig = os.path.join(locations.get_install_dir(), dest_file)
                    dest = os.path.join(dest_dir, dest_file)
                    os.rename(orig, dest)
                    for t in ('dtx', 'ins', 'tex'):
                        fl = orig[:-3] + t
                        if os.path.isfile(fl):
                            os.remove(fl)

                    provides.append(dest)
                except OSError:
                    tex_dep = os.path.join(locations.get_install_dir(), f[:-3] + 'tex')
                    if os.path.isfile(tex_dep):
                        requires.extend(get_requirements(tex_dep))
            elif f.endswith('.drv'):
                subprocess.call(['latex', '-interaction=batchmode', f], stdout=open(os.devnull, 'w'), cwd=locations.get_install_dir())
                os.remove(os.path.join(locations.get_install_dir(), f))
            elif f.endswith('.dvi'):
                # subprocess.call(['dvipdfm', f], stdout=open(os.devnull, 'w'), cwd=locations.get_install_dir())
                os.remove(os.path.join(locations.get_install_dir(), f))
            elif f.endswith('.ins'):
                local_requires = []
                local_requires.extend(get_requirements(os.path.join(locations.get_install_dir(), f)))
                tex_dep = os.path.join(locations.get_install_dir(), f[:-3] + 'tex')
                if os.path.isfile(tex_dep):
                    local_requires.extend(get_requirements(tex_dep))

                for req in list(local_requires):
                    if req == package:
                        local_requires.remove(req)
                        continue
                    elif local_info.installed(req) or local_info.provided(req):
                        local_requires.remove(req)
                        continue
                    for pack in provides:
                        name = re.sub(r'.*/(.*)\.(.*)', r'\1.\2', pack)
                        if req + '.sty' == name:
                            local_requires.remove(req)
                            break
                        elif req == name:
                            local_requires.remove(req)
                            break

                if local_requires:
                    requires.extend(local_requires)
                else:
                    print '  building', f[:-4]
                    subprocess.call(['latex', '-interaction=batchmode', f], stdout=open(os.devnull, 'w'), cwd=locations.get_install_dir())

                    for line in open(os.path.join(locations.get_install_dir(), f), 'r').readlines():
                        if line.startswith(r'\generate'):
                            if 'file' in line:
                                sty, dtx = re.sub(r'\\generate.*\\file.*?\{(.*\..*)\}.*\\from.*?\{(.*\.[^\}]*)\}.*', r'\1\t\2', line).split('\t')
                                sty, dtx = sty.replace('\n', ''), dtx.replace('\n', '')

                                filetype = sty[-3:]
                                if filetype == 'tex':
                                    filetype = 'sty'
                                dest_dir = locations.get_path(filetype, package)
                                if not os.path.exists(dest_dir):
                                    os.makedirs(dest_dir)

                                orig = os.path.join(locations.get_install_dir(), sty)
                                dest = os.path.join(dest_dir, sty)
                                os.rename(orig, dest)

                                dtx_path = os.path.join(locations.get_install_dir(), dtx)
                                if os.path.isfile(dtx_path):
                                    os.remove(dtx_path)

                                if 'discard' not in dest_dir:
                                    provides.append(dest)

                    os.remove(os.path.join(locations.get_install_dir(), f))
            elif f.endswith('.pdf'):
                dest_dir = locations.get_path('pdf', package)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                orig = os.path.join(locations.get_install_dir(), f)
                dest = os.path.join(dest_dir, f)
                os.rename(orig, dest)

                fl = orig[:-3] + 'tex'
                if os.path.isfile(fl):
                    os.remove(fl)
            elif f.endswith('.sty'):
                dest_dir = locations.get_path('sty', package)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                orig = os.path.join(locations.get_install_dir(), f)
                dest = os.path.join(dest_dir, f)
                os.rename(orig, dest)
                provides.append(dest)

    install_dir = locations.get_install_dir()
    if not requires:
        for f in os.listdir(install_dir):
            orig = os.path.join(install_dir, f)

            if empty(orig):
                pass
            elif f.endswith('.tex'):
                dest_dir = locations.get_path('sty', package)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                dest = os.path.join(dest_dir, f)
                os.rename(orig, dest)
            else:
                dest_dir = locations.get_path(f[-3:], package)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)

                dest = os.path.join(dest_dir, f)
                os.rename(orig, dest)
        shutil.rmtree(install_dir)
    return provides, requires


def run(package, parent=None):
    if isinstance(package, list):
        for pkg in package:
            run(pkg)
        return
    else:
        ext_file = os.path.join(os.getcwd(), package)
        if os.path.isfile(ext_file):
            if package.endswith('.txt'):
                for line in open(ext_file, 'r').readlines():
                    run(line.split('==')[0])
            elif package.endswith('.tex') or package.endswith('.sty'):
                for req in get_requirements(ext_file):
                    run(req)

            return

    pkg = package.lower()
    if local_info.installed(pkg):
        data = local_info.get_data(pkg)
        error.msg_satisfied(data[0] + '==' + data[1], parent, fail=False)
    else:
        version, rows = ctan.get_data(pkg, parent)
        if version and rows:
            run_workflow(package, parent, version, rows)
        elif rows == '-1':
            return False
    return True
