"""
    crython
    ~~~~~~~

    Lightweight task scheduler using cron expressions.

    :copyright: (c) 2013 Andrew Hawker.
    :license: MIT, see LICENSE for more details.
"""
import ast
import io
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version_regex = re.compile(r'__version__\s+=\s+(.*)')


def get_version():
    with io.open('crython/__init__.py', 'r', encoding='utf-8') as f:
        return str(ast.literal_eval(version_regex.search(f.read()).group(1)))


def get_long_description():
    with io.open('README.rst', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='crython',
    version=get_version(),
    author='Andrew Hawker',
    author_email='andrew.r.hawker@gmail.com',
    url='https://github.com/ahawker/crython',
    license='MIT',
    description='Lightweight task scheduler using cron expressions.',
    long_description=get_long_description(),
    packages=['crython'],
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
