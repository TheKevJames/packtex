import re

from .. import (error, local_info)


def run(package):
    if isinstance(package, list):
        for pkg in package:
            run(pkg)
        return

    pkg = package.lower()
    error.installed('show', pkg, fail=True)

    data = local_info.get_data(pkg)
    print '-----'
    print 'Name:', data[0]
    print 'Version:', data[1]
    print 'Provides:', ', '.join([re.sub(r'(.*/)|(\n)', '', fl)
                                  for fl in data[2].split('=')])
    print 'Requires:', ', '.join(data[3].split('=')).replace('\n', '')
