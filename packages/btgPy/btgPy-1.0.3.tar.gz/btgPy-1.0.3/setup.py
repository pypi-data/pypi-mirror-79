import re
from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def get_version():
    """
    Read version from __init__.py
    """
    version_regex = re.compile(
        '__version__\\s*=\\s*(?P<q>[\'"])(?P<version>\\d+(\\.\\d+)*(-(alpha|beta|rc)(\\.\\d+)?)?)(?P=q)'
    )
    here = path.abspath(path.dirname(__file__))
    init_location = path.join(here, "btgPy/__init__.py")

    with open(init_location) as init_file:
        for line in init_file:
            match = version_regex.search(line)

    if not match:
        raise Exception(
            "Couldn't read version information from '{0}'".format(init_location)
        )

    return match.group('version')

setup(
    name='btgPy',
    version=get_version(),
    description='Data science tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/bgonzalezd/btgPy',
    author='Briter Gonzalez',
    author_email='btg.developers@gmail.com',
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='CHAID pandas numpy scipy statistics statistical analysis',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'cython',
        'numpy',
        'pandas',
        'treelib',
        'pytest',
        'scipy',
        'savReaderWriter',
        'graphviz',
        'plotly',
        'colorlover',
        'enum34; python_version == "2.7"'
    ],
    extras_require={
        'test': ['codecov', 'tox', 'tox-pyenv', 'detox', 'pytest', 'pytest-cov'],
    }
)
