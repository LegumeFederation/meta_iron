# -*- coding: utf-8 -*-
'''
meta_iron -- metadata flattening and smoothing
'''

# Developers:
# Install with
# pip install --editable .
# and execute as a module.


from setuptools import setup

setup(
    name='aakbar',
    version='0.1'
    url='http://github.com/GenerisBio/aakbar',
    keywords=['science', 'biology', 'bioinformatics', 'data' ],
    license='BSD',
    description='metadata maintainance tools',
    long_description=open('README.rst').read(),
    author='Joel Berendzen',
    author_email='joelb@ncgr.org',
    packages=['meta_iron'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['bcbio-gff',
                      'click>=5.0',
                      'click_plugins',
                      'numpy',
                      'pandas'],
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
