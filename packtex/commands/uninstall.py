import os
import shutil

from .. import (error, locations)


def run(package):
    if isinstance(package, list):
        for pkg in package:
            run(pkg)
        return

    pkg = package.lower()
    error.installed('uninstall', pkg, fail=True)

    directory = locations.get_path(None, pkg)
    log_file = os.path.join(directory, '.log')
    for line in open(log_file, 'r').readlines():
        os.remove(line.replace('\n', ''))
    shutil.rmtree(directory)

    installed = open(locations.get_metadata_file(), 'r').readlines()
    with open(locations.get_metadata_file(), 'w') as meta:
        for pack in installed:
            if pack.split('==')[0] != pkg:
                meta.write(pack)
    print 'Successfully uninstalled', pkg
