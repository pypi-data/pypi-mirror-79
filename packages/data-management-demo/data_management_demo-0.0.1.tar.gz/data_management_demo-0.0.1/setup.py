#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

python_requires = '>=3.6'

install_requires = [
    'opencv-python==3.2.0.8',
    'tifffile==2020.9.3',
    'console-menu==0.6.0',
    'pathlib==1.0.1',
    'toml==0.10.1'
]

tests_require = [ ]

setup(
    author="Julian Pitney",
    author_email='julianpitney@gmail.com',
    python_requires=python_requires,
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
    description="Data management solution demo",
    install_requires=install_requires,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='data_management_demo',
    name='data_management_demo',
    packages=find_packages(include=['data_management_demo', 'data_management_demo.*']),
    test_suite='tests',
    tests_require=tests_require,
    url='https://github.com/julianpitney/data_management_demo',
    version='0.0.1',
    zip_safe=False,
)
