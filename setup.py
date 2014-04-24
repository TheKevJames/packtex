#!/usr/bin/env python
import io
import os
from pip.req import parse_requirements
import re
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand
import sys


if sys.argv[-1] == 'publish':
	os.system('python setup.py sdist bdist_wheel upload')
	sys.exit()


def read(*filenames, **kwargs):
	encoding = kwargs.get('encoding', 'utf-8')
	sep = kwargs.get('sep', '\n')
	buf = []
	for filename in filenames:
		with io.open(filename, encoding=encoding) as f:
			buf.append(f.read())
	return sep.join(buf)

def find_version(*file_paths):
	version_file = read(os.path.join(*file_paths))
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError('Unable to find version string.')

try:
	long_description = read('README.rst')
except IOError:
	long_description = read('README.md')

requires = [str(ir.req) for ir in parse_requirements('requirements.txt')]

class PyTest(TestCommand):
	def finalize_options(self):
		TestCommand.finalize_options(self)
		self.test_args = []
		self.test_suite = True

	def run_tests(self):
		import pytest

		errcode = pytest.main(self.test_args)
		sys.exit(errcode)

setup(
	name='packtex',
	version=find_version('packtex', '__init__.py'),
	description='Auto-generated description',
	long_description=long_description,
	keywords='packtex',
	author='@TheKevJames (auto-generated)',
	author_email='KevinJames@thekev.in (auto-generated)',
	url='https://github.com/TheKevJames/packtex.git',
	license='MIT License',
	packages=find_packages(exclude=['test']),
	include_package_data=True,
	entry_points={'console_scripts': [
		'packtex = packtex:execute_from_command_line',
	]},
	install_requires=requires,
	tests_require=['pytest'],
	zip_safe=False,
	classifiers=[
		'Programming Language :: Python',
		'Development Status :: 1 - Planning',
		'Natural Language :: English',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
	],
	test_suite='test',
	extras_require={
		'testing': ['pytest'],
	},
)
