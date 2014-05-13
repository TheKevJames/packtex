from .. import (ctan, error, local_info)
from . import (install, uninstall)


def run(package):
    if isinstance(package, list):
        for pkg in package:
            run(pkg)
        return

    pkg = package.lower()
    error.installed('upgrade', pkg, fail=True)

    installed_version = local_info.get_data(pkg)[1]
    version, _ = ctan.get_data(pkg)

    error.updated(package, installed_version, version, fail=True)

    uninstall.run(package)
    install.run(package)
