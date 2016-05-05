# -*- coding: utf-8 -*-
'''
meta_iron -- flattening and smoothing sequence metadata creation and curation
'''

# This file makes it easier for developers to test in-place via the command
# python3 -m meta_iron
# from the directory above this one.

from .__init__ import cli
if __name__ == '__main__':
    cli(auto_envvar_prefix='META_IRON')