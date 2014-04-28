from packtex import locations


def run():
	installed = []
	meta = open(locations.get_metadata_file(), 'r').readlines()
	for line in meta:
		installed.append(line.replace('\n', ''))

	installed.sort()
	for inst in installed:
		print '=='.join(inst.split('==')[:2])
