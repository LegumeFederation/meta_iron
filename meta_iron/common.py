# -*- coding: utf-8 -*-
'''Global constants and common helper functions.
'''
#
# library imports
#
import logging
from datetime import datetime
from pathlib import Path # python 3.4 or later
from itertools import chain
import sys
#
# 3rd-party modules
#
import yaml
import click

try:
    from .version import version as __version__ # noqa
except ImportError:
    __version__ = 'devel'
#
# global constants
#
PROGRAM_NAME = 'meta_iron'
AUTHOR = 'Joel Berendzen'
EMAIL = 'joelb@ncgr.org'
COPYRIGHT = """Copyright (C) 2016, The National Center for Genome Resources.  All rights reserved.
"""
PROJECT_HOME = 'https://github.com/LegumeFederation/meta_iron'
DOCS_HOME = 'https://meta_iron.readthedocs.org/en/stable'

DEFAULT_FILE_LOGLEVEL = logging.DEBUG
DEFAULT_STDERR_LOGLEVEL = logging.INFO
VERSION = __version__
STARTTIME = datetime.now()
ROOT_METADATA_FILE_ENVVAR = 'META_IRON_ROOT_METADATA_FILE_PATH'
#
# global logger object
#
logger = logging.getLogger(PROGRAM_NAME)
#
# Class definitions begin here.
#
class PersistentMetadataObject(object):
    '''Defines a persistent metadata object

    Attributes:
        :metadata_dict: Dictionary of metadata parameters.
        :name: metadata filename.
        :path: metadata filepath (absolute).
    '''
    def __init__(self, metadata_dir=None, name='node_metadata.yaml'):
        '''Inits the metadata dictionary

        Reads a metadata file from a subdirectory of the
        current working directory.  If that file isn't found,
        then searches in the system-specific metadata directory.
        If that file isn't found either, creates a new file in the
        directory specified by the location parameter.
        '''
        self.name = name
        self._default_dict = {'meta_iron_version': VERSION,
                              'children': [],
                              }

        self._default_path = Path((click.get_app_dir(PROGRAM_NAME)+'/' + self.name))
        self._cwd_path = Path ('.' + '/.' + PROGRAM_NAME + '/' + self.name)
        if metadata_dir is not None:
            self.path = self._get_path_from_dir(metadata_dir)
        elif self._cwd_path.is_file():
            self.path = self._cwd_path
        else:
            self.path = self._default_path
        if not self.path.exists():
            self.metadata_dict = {}
            self.path = None
        else:
            with self.path.open('rt') as f:
                self.metadata_dict = yaml.safe_load(f)

    def _get_path_from_dir(self, dir):
        return Path(str(dir) + '/.' + PROGRAM_NAME +'/' + self.name).expanduser()

    def _update_metadata_dict(self):
        '''Update metadata dictionary if necessary
        :param metadata_dict: metadata dictionary.
        :return: Updated metadata dictionary.
        '''
        try:
            if self.metadata_dict['version'] != VERSION:
                # Do whatever updates necessary, depending on version.
                # For now, nothing needs to be done.
                self.metadata_dict['version'] = VERSION
        except KeyError:
            logger.warning('Initializing metadata file "%s"',
                           self.path)
            self.metadata_dict = self._default_dict


    def write_metadata_dict(self, metadata_dict=None, dir=None):
        '''Writes a YAML metadata dictionary
        :param metadata_dict: metadata dictionary
        :return: None
        '''
        if dir is None or dir is '':
            if self.path is None:
                self.path = self._default_path
        elif dir is '.':
            self.path = self._cwd_path
        else:
            self.path = self._get_path_from_dir(dir)

        if metadata_dict == {}:
            self.metadata_dict = self._default_dict
        elif metadata_dict is not None and metadata_dict != self.metadata_dict:
                self.metadata_dict = metadata_dict
                self._update_metadata_dict()

        if not self.path.parent.exists():
            # create parent directory
            logger.debug('Creating metadata file directory "%s"',
                          self.path.parent)
            try:
                self.path.parent.mkdir(parents=True)
            except OSError:
                logger.error('Unable to create parent directory "%s".',
                             self.path.parent)
                sys.exit(1)
        if not self.path.parent.is_dir():
            logger.error('Path "%s" exists, but is not a directory.',
                         self.path.parent)
            sys.exit(1)
        if not self.path.exists():
            logger.debug('Creating metadata file "%s"', self.path)
            try:
                self.path.touch()
            except OSError:
                logger.error('Path "%s" is not writable.', self.path)
                sys.exit(1)
        with self.path.open(mode='wt') as f:
            yaml.dump(self.metadata_dict, f)
metadata_obj = PersistentmetadataObject()

#
# helper functions called by multiple cli functions
#
def get_user_context_obj():
    '''Returns the user context, containing logging and metadata data.

    :return: User context object (dict)
    '''
    return click.get_current_context().obj

def to_str(seq):
    '''Decode bytestring if necessary.

    :param seq: Input bytestring, string, or other sequence.
    :return: String.
    '''
    if isinstance(seq, bytes):
        value = seq.decode('utf-8')
    elif isinstance(seq, str):
        value = seq
    else:
        value = str(seq)
    return value


def to_bytes(seq):
    '''Encode or convert string if necessary.

    :param seq: Input string, bytestring, or other sequence.
    :return: Bytestring.
    '''
    if isinstance(seq, str):
        value = seq.encode('utf-8')
    elif isinstance(seq, bytes):
        value = seq
    else:
        value = bytes(seq)
    return value
