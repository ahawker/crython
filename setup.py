__author__ = 'Andrew Hawker <andrew.r.hawker@gmail.com>'

import crython

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name=crython.__name__,
    version=crython.__version__,
    description='Cron scheduling for python functions.',
    long_description=open('README.md').read(),
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/ahawker/crython',
    license=open('LICENSE.md').read(),
    package_dir={'crython': 'crython'},
    packages=['crython'],
    test_suite='tests',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6'
        'Programming Language :: Python :: 2.7'
    )
)
