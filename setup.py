# -*- coding: utf-8 -*-
'''
meta_iron -- flattening and smoothing sequence metadata creation and curation
'''

# Developers, install with
#    pip install --editable .
# and execute as a module.

from setuptools import setup

from meta_iron.version import version

setup(
    name='meta_iron',
    version=version,
    url='http://github.com/LegumeFederation/meta_iron',
    keywords=['science', 'biology', 'bioinformatics', 'data curation'],
    license='BSD',
    description='flattening and smoothing sequence metadata creation and curation',
    long_description=open('README.md').read(),
    author='Joel Berendzen',
    author_email='joelb@ncgr.org',
    packages=['meta_iron'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['click>=5.0',
                      'click_plugins'],
    entry_points={
                 'console_scripts':['meta_iron = meta_iron:cli']
                },
    classifiers=[
                        'Development Status :: 3 - Alpha',
                        'Environment :: Console',
                        'Environment :: MacOS X',
                        'Environment :: Win32 (MS Windows)',
                        'Intended Audience :: Science/Research',
                        'License :: Other/Proprietary License ',
                        'Operating System :: OS Independent',
                        'Programming Language :: Python',
                        'Topic :: Scientific/Engineering :: Bio-Informatics',
                        ]
)
