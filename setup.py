"""Script for setuptools."""
import sys
from setuptools import setup, find_packages


with open('README.md') as readme:
    long_description = readme.read()

version = '1.0.0'

deps = [gooey, sys, streamtologger, json]


setup(
    name='DARx Driver',
    version=1.01,
    url='https://github.com/k0n1ev/darx/',
    author='Syndivia',
    author_email='enquiry@syndivia.com',
    description=('GUI and script modules for DARx Bioconjugation Automation Machine'),
    license='MIT',
    packages=find_packages(),
    install_requires=deps,
    include_package_data=True,
    classifiers = [
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Bioconjugation :: Open Research',
        'Topic :: Chemistry :: Biology',
        'Programming Language :: Python :: 3.0',
    ],
    long_description='''
DARx Machine (Beta)
############
GUI and script modules for DARx Bioconjugation Automation Machine
-----------------------------------------------------------------------------
'''
)
