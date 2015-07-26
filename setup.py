#!/usr/bin/env python
import setuptools

from packtex import __version__


# For reasons why you shouldn't do this, see:
#   https://caremad.io/blog/setup-vs-requirement/
# For all the fucks I give see:
#   /dev/zero
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()
    requirements = filter(lambda x: '==' in x, requirements)
with open('requirements-dev.txt', 'r') as f:
    requirements_dev = f.read().splitlines()
    requirements_dev = filter(lambda x: '==' in x, requirements_dev)


setuptools.setup(
    name='packtex',
    version=__version__,
    description='packtex',
    long_description='An easy-to-use, platform-agnostic *TeX package manager',
    keywords='packtex',
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/packtex.git',
    license='MIT License',
    packages=setuptools.find_packages(exclude=['test']),
    install_requires=requirements,
    tests_require=requirements_dev,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    test_suite='tests',
    extras_require={
        'testing': requirements_dev,
    },
    entry_points={'console_scripts': [
        'packtex = packtex:execute_from_command_line',
    ]},
)
