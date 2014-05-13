from . import locations


def get_data(package):
    for line in open(locations.get_metadata_file(), 'r').readlines():
        splt = line.split('==')
        if splt[0] == package:
            return splt


def installed(package):
    for line in open(locations.get_metadata_file(), 'r').readlines():
        if line.split('==')[0] == package:
            return True
    return False


def provided(package):
    for line in open(locations.get_metadata_file(), 'r').readlines():
        for provide in line.split('==')[2]:
            if package in provide:
                return True
    return False
