# -*- coding: utf-8 -*-
'''Global constants and common helper functions.
'''
#
# library imports
#
import logging
from datetime import datetime
from pathlib import Path # python 3.4 or later
import sys
#
# 3rd-party modules
#
import yaml
import click

#
# module version--kept in its own file for setup.py
#
from .version import version as __version__ # noqa
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
# Every root or node metadata file will have these attributes set at creation time.
#
REQUIRED_DIRECTORY_ATTRIBUTES = {
                                'meta_iron_version': VERSION,
                                'version': '',
                                'children': [],
                                'files': [],
                                'type': '',
                                'alias': '',
                                'depth': 0
                                }
#
# Dictionary of known node types with mandatory attributes for that type.
# These inherit hierarchically, and may be overridden at any lower point.
#
DIRECTORY_TYPES = {'root': {'root_version': '',
                            'root_url': '',
                            'root_name': '',
                            'root_code': '',
                            'curator': '',
                            'curator_url': '',
                            'temp': False,
                            'upload': True,
                            'alias_start_level': 1
                            },
                   'log': {'temp': True,
                           'upload': False
                           },
                   'temp': {'temp': True,
                            'upload': False
                            },
                   'bin': {'executable': True
                           },
                   'common': {'name': 'Legumes'
                              },
                   'species':{'name': '',
                              'common_name': '',
                              'code': '',
                              'genome_size_Mbp': 0.0,
                              'taxon_id': 0
                              },
                   'organism':{'reference_url': '',
                               'organism_name': '',
                               'organism_code': '',
                               'organism_desc': ''
                               },
                   'genome':{'assemblies': []
                             },
                   'genomic_reads':{'read_files': []
                                    },
                   'assembly':{'total_assembly_size_bp': 0,
                               'assembly_files': [],
                               'annotation_dirs': []
                               },
                   'annotation':{'feature_files':[]
                                 },
                   'transcriptome':{'transcriptome_files':[],
                                    'columnar_metadata_file': ''
                                    }
}
#
# Every file is required to have these attributes set
#
REQUIRED_FILE_ATTRIBUTES = {'file_size': 0,
                            'file_mod_timestamp': '',
                            'file_compression': '',
                            'file_type': ''
                            }
#
# Dictionary of known file types.
#
FILE_TYPES = {'assembly': {'assembly_size', 0
                           },
              'reads': {'n_reads':0,
                        'basepairs':0
                        },
              'feature': {'n_features':0
                           }
              }
#
# global logger object
#
logger = logging.getLogger('meta_iron')
#
# Class definitions begin here.
#
class HierarchicalMetadataObject(object):
    '''Defines a hierarchical persistent metadata object

    Attributes:
        :metadata_dict: Dictionary of metadata parameters.
        :name: metadata filename.
        :path: metadata filepath (absolute).
    '''
    def __init__(self, metadata_dir=None, name='node_metadata.yaml'):
        '''Initialize a node metadata dictionary

        Reads a metadata file from a subdirectory of the
        current working directory.  If that file isn't found,
        then searches in the system-specific metadata directory.
        If that file isn't found either, creates a new file in the
        directory specified by the location parameter.
        '''
        self.type = type
        if self.type == 'root':
            self.name = 'root_metadata.yaml'
        else:
            self.name = 'node_metadata.yaml'

        self.path = Path (self.name)
        if not self.path.exists():
            self.metadata_dict = {}
            self.path = None
        else:
            with self.path.open('rt') as f:
                self.metadata_dict = yaml.safe_load(f)

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


    def write_metadata_dict(self, metadata_dict=None):
        '''Writes a YAML metadata dictionary
        :param metadata_dict: metadata dictionary
        :return: None
        '''
        if metadata_dict == {}:
            self.metadata_dict = self._default_dict
        elif metadata_dict is not None and metadata_dict != self.metadata_dict:
                self.metadata_dict = metadata_dict
                self._update_metadata_dict()

        if not self.path.exists():
            logger.debug('Creating metadata file "%s"', self.path)
            try:
                self.path.touch()
            except OSError:
                logger.error('Path "%s" is not writable.', self.path)
                sys.exit(1)
        with self.path.open(mode='wt') as f:
            yaml.dump(self.metadata_dict, f)

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
