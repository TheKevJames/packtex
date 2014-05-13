from .. import locations


def run(method):
    installed = []
    meta = open(locations.get_metadata_file(), 'r').readlines()
    for line in meta:
        installed.append(line.replace('\n', ''))

    installed.sort()
    for inst in installed:
        splitted = inst.split('==')
        if method == 'freeze':
            print '=='.join(splitted[:2])
        elif method == 'list':
            print splitted[0] + ' (' + splitted[1] + ')'
