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
import os
import collections
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

ROOT_METADATA_FILE_PATTERN = 'root_metadata*.yaml'
NODE_METADATA_FILE_PATTERN = 'node_metadata*.yaml'
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
        self.path_list, self.rooted = self._check_for_metadata('.')
        metadata_dict_list = []
        self.metadata = {}
        self.node_metadata = {}
        self.node_dir = os.getcwd()
        for path in self.path_list:
            with path.open('rt') as f:
                try:
                    metadata_dict_list.append(yaml.safe_load(f))
                except:
                    logger.error('Corrupt metadata file at "%s".',
                                 path)
                    sys.exit(1)
        if len(metadata_dict_list) == 0:
            self.metadata_found = False
            logger.debug('No metadata file found in "%s".',
                         str(Path('.').resolve()))
            self.metadata = {}
            self.source = {}
            self.node_depth = None
        else:
            self.metadata_found = True
            self.node_depth = len(self.path_list)-1
            self.metadata = {}
            self.source = {}
            for i in range(len(metadata_dict_list)):
                (self.metadata,
                self.source) = self._recursive_overlay(self.metadata,
                                                        metadata_dict_list[i],
                                                        self.source,
                                                        str(self.path_list[i]))
            if 'meta' in self.source: # don't track meta-metadata source
                del self.source['meta']
        if self.rooted:
            logger.debug('Root metadata found at "%s".',
                         self.path_list[0])
        else:
            if self.metadata_found:
                logger.debug('No root metadata file found.')
        for key in self.metadata.keys():


    def __str__(self):
        desc = 'Hierarchical Metadata object, version %s\n' %VERSION
        #desc += '%s\n'%self.metadata
        #desc += 'meta%s\n'%self.metadata['meta']
        #desc += '%s\n'%self.source
        if self.rooted:
            top_desc = 'root'
        else:
            top_desc = 'unrooted top'
        if self.node_depth == 1:
            level_plural = ''
        else:
            level_plural = 's'
        desc += 'Node "%s" is %d level%s deep from %s ' %(self.node_dir,
                                                          self.node_depth,
                                                          level_plural,
                                                          top_desc)
        desc += 'at "%s".\n' %self.path_list[0]
        desc += '    Name        Value [Units]   Source\n'
        for k,v in sorted(self.metadata.items()):
            if k != 'meta':
                try:
                    units = ' '+ self.metadata['meta'][k]['units']
                except KeyError:
                    units = ''
                try:
                    key_desc = self.metadata['meta'][k]['desc']
                except KeyError:
                    key_desc = k
                desc += ' %s  %s%s  %s\n'%(key_desc,
                                           v,
                                           units,
                                           self.source[k])
        return desc


    def _recursive_overlay(self,
                           dict_element,
                           possible_map,
                           source_dict,
                           source):
        if isinstance(possible_map, collections.MutableMapping):
            for k, v in possible_map.items():
                if k not in dict_element:
                    dict_element[k] = {}
                if k not in source_dict:
                    source_dict[k] = {}
                (dict_element[k],
                     source_dict[k]) = self._recursive_overlay(dict_element[k],
                                                               v,
                                                               source_dict[k],
                                                               source)
        else: # not a map
            dict_element = possible_map
            source_dict = source
        return dict_element, source_dict


    def _check_for_metadata(self,
                            search_path='.',
                            path_list=[]):
        '''Recursively check upwards for metadata files
        '''
        root_found = False
        root_list = list(Path(search_path).glob(ROOT_METADATA_FILE_PATTERN))
        if len(root_list) > 1:
            logger.error('More than one root metadata file was found in "%s".',
                         Path(search_path))
            sys.exit(1)
        elif len(root_list) == 1:
            path_list += root_list
            root_found = True
        else: # not at the root, iterate upwards
            node_list = list(Path(search_path).glob(NODE_METADATA_FILE_PATTERN))
            if len(node_list)>1:
                logger.error('More than one node metadata file was found in "%s".',
                             Path(search_path))
                sys.exit(1)
            elif len(node_list) == 1:
                if search_path == '.':
                    recurse_path = '..'
                else:
                    recurse_path = search_path+'/..'
                path_list, root_found = self._check_for_metadata(search_path=recurse_path,
                                         path_list=path_list)
                path_list += node_list
        return (path_list, root_found)

    def _update_node_metadata_dict(self):
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


    def write_node_metadata_dict(self, metadata_dict=None):
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
