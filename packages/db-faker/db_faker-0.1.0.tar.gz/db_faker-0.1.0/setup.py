#!/usr/bin/env python

"""The setup script."""
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

VERSION = '0.1.0'

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

# Generating the requirements of the package from the requirements.txt file
lib_folder = os.path.dirname(os.path.realpath(__file__))
requirements_file = lib_folder + '/requirements.txt'
requirements = []
if os.path.isfile(requirements_file):
    with open(requirements_file, "r") as reqs:
        requirements = reqs.read().splitlines()

# Requirements for setup the package
setup_requirements = ['pytest-runner', ]

# Requirements for testing the package
test_requirements = ['pytest>=6', ]


# https://circleci.com/blog/continuously-deploying-python-packages-to-pypi-with-circleci/
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = os.getenv('CIRCLE_TAG')

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


# Setup function
setup(
    author="Pablo Barrientos",
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="CLI application that handles the creation of fake data to databases",
    entry_points={
        'console_scripts': [
            'db_faker=db_faker.cli:main',
        ],
        "db_faker.commands": [
            "validate-schema=db_faker.commands.validate_schema:ValidateSchema",
            "generate-data=db_faker.commands.generate_data:GenerateData"
        ]
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords='db_faker test databases data',
    name='db_faker',
    packages=find_packages(include=['db_faker', 'db_faker.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/PBarri/db-faker',
    version=VERSION,
    zip_safe=False,
    cmd_class={
        'verify': VerifyVersionCommand
    }
)
