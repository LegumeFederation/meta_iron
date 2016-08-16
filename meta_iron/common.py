# -*- coding: utf-8 -*-
'''Global constants and common helper functions.
'''
#
# library imports
#
import logging
import sys
import os
import ast
import json
from datetime import datetime
from pathlib import Path # python 3.4 or later
from collections import OrderedDict, MutableMapping
from distutils.util import strtobool
from distutils.version import StrictVersion
#
# 3rd-party module imports
#
import pandas as pd
import click
from tabulate import tabulate
from pint import UnitRegistry
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

ROOT_METADATA_FILE_PATTERN = '*root_metadata.tsv'
NODE_METADATA_FILE_PATTERN = '*node_metadata.tsv'
#
# Every root or directory metadata file will have these attributes set at creation time.
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
# Dictionary of known directory types with mandatory attributes for that type.
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
# Helper functions
#

#
# global logger object
#
logger = logging.getLogger('meta_iron')
#
# Class definitions begin here.
#
class JSONOrderedDict(OrderedDict):
    '''An OrderedDict with JSON string output format
    '''
    def __str__(self):
        return json.dumps(d)

class OrderedDictionaryParser(ast.NodeVisitor):
    def visit_Dict(self,node):
        keys,values = node.keys,node.values
        keys = [n.s for n in node.keys]
        values = [n.s for n in node.values]
        self.ordered_dictionary = JSONOrderedDict(zip(keys,values))

class MetadataTypes(object):
    '''Defines types and type handling for metadata

    '''
    # The type dictionary contains mappings between
    # type names and class constructors.  The constructors must
    # return an object for which __str__ is defined and
    # which raises ValueError if an illegal value is
    # input to the constructor.
    #
    class StringType(object):
        def __init__(self, s):
            self.name = 'stringtalm78wa' \
                        ''
            return str(s)

    def __init__(self):
        self.string = 'string'
        self.integer = 'integer'
        METADATA_TYPE_DICT = {self.string: str,
                              self.integer: int,
                              'float': float,
                              'boolean': strtobool,
                              'list': self.list_init,
                              'dictionary': self.dictionary_init,
                              'version': self.version_init,
                              'identifier': self.identifier_init,
                              'units': self.units_init,
                              'OID': self.OID_init,
                              'file': self.file_init,
                              'directory': self.directory_init,
                              'URL': self.URL_init
                              }
        self.dict_parser = OrderedDictionaryParser()
        self.unit_registry = UnitRegistry()
        #self.unit_registry.load_definitions(unitsfile)

    def version_init(self, s):
        '''Chcek if valid version string, using distutils.StrictVersion

        :param s:
        :return:
        '''
        VersionChecker = StrictVersion()
        VersionChecker.parse(s) # raises ValueError if no agreement
        return s

    def units_init(self, s):
        try:
            self.unit_registry(s)
        except UndefinedUnitError:
            raise ValueError
        return s

    def OID_init(self, s):
        pass

    def URL_init(self, s):
        pass

    def file_init(self, s):
        pass

    def directory_init(self, s):
        pass

    def list_init(self, s):
        return list(ast.literal_eval(s))


    def dictionary_init(self, s):
        return self.dict_parser.visit(ast.parse(s)).ordered_dictionary


    def identifier_init(self, s):

        '''Check if valid identifier.
        :param s:
        :return: s if valid
        '''
        if not s.isidentifier():
            raise ValueError
        else:
            return s.lower()


    def from_string(self, s, data_type):
        if data_type not in self.METADATA_TYPE_DICT:
            raise ValueError
        return self.METADATA_TYPE_DICT[data_type](s)


metadata_types = MetadataTypes()

ATTRIBUTE_TYPE_DICT = {'name': 'identifier',
                       'value': 'value',
                       'label': metadata_types.string,
                       'units': 'units',
                       'min': 'basetype',
                       'max': 'basetype',
                       'precision': metadata_types.integer,
                       'width': metadata_types.integer,
                       'allowed_values': 'basetype_list',
                       'description': metadata_types.string,
                       'notes': metadata_types.string,
                       'evaluate': 'boolean',
                       'append': 'boolean'
                       }


class HierarchicalMetadataObject(object):
    '''Defines a hierarchical persistent metadata object

    Attributes:
        :metadata_dict: Dictionary of metadata parameters.
        :name: metadata filename.
        :path: metadata filepath (absolute).
    '''
    def __init__(self, metadata_dir=None, name='node_metadata.tsv'):
        '''Initialize a directory metadata dictionary

        Reads a metadata file from a subdirectory of the
        current working directory.  If that file isn't found,
        then searches in the system-specific metadata directory.
        If that file isn't found either, creates a new file in the
        directory specified by the location parameter.
        '''
        self.path_list, rooted = self._check_for_metadata('.')
        self.directory_dir = os.getcwd()
        self.metadata_found = False
        self.metadata = None
        self.source = None
        self.directory_depth = None
        self.directory_metadata = None
        if len(self.path_list) == 0:
            logger.debug('No directory metadata file found in "%s".',
                         str(Path('.').resolve()))
            return
        elif not rooted:
            logger.debug('No root metadata file found, skipping metadata parsing.')
            return
        self.directory_depth = len(self.path_list)-1
        for path in self.path_list:
            with path.open('rt') as f:
                try:
                    self.directory_metadata = self._read_metadata_file(f,
                                                     sep='\t',
                                                     index_col=0)
                except:
                    logger.error('Corrupt metadata file at "%s".',
                                 path)
            if not self.metadata_found: # must be root directory
                self.metadata = self.directory_metadata
                self.metadata_found = True
            else:
                for col in self.directory_metadata.columns:
                    self.metadata[col] = self.directory_metadata[col].notnull()


    def __str__(self):
        desc = 'Hierarchical Metadata object, version %s.\n' %VERSION
        if self.directory_depth == 1:
            level_plural = ''
        else:
            level_plural = 's'
        # Files in path
        desc += 'Directory "%s" is %d level%s deep from root:\n' %(self.directory_dir,
                                                          self.directory_depth,
                                                          level_plural)
        table_data = []
        for i, path in enumerate(self.path_list):
            table_data.append([i, path])
        desc += tabulate(table_data, headers=['Depth', 'Path'])
        # Node metadata values
        desc += '\n\nMetadata at This Node:\n'
        desc += self.format_metadata(self.directory_metadata)
        # Metadata Values
        desc += '\n\nMetadata After Overloading:\n'
        desc += self.format_metadata(self.metadata, show_source=True)
        desc += '\n'
        return desc

    def format_metadata(self, data_dict, show_source=False):
        table_data = []
        headers = ['Name', 'Value','Units']
        if show_source:
            headers.append('Source')
        for k,v in sorted(data_dict.items()):
            if k != 'meta':
                try:
                    units = self.metadata['meta'][k]['units']
                except KeyError:
                    units = ''
                try:
                    key_desc = self.metadata['meta'][k]['desc']
                except KeyError:
                    key_desc = k
                row_data = [key_desc, v, units]
                if show_source:
                    row_data.append(self.source[k])
                table_data.append(row_data)
        return tabulate(table_data, headers=headers)

    def _recursive_overlay(self,
                           dict_element,
                           possible_map,
                           source_dict,
                           source):
        if isinstance(possible_map, MutableMapping):
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

    def _read_metadata_file(self,fh, root=False):
        return pd.read_csv(fh,
                    sep='\t',
                    index_col=0)

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
            directory_list = list(Path(search_path).glob(NODE_METADATA_FILE_PATTERN))
            if len(directory_list)>1:
                logger.error('More than one directory metadata file was found in "%s".',
                             Path(search_path))
                sys.exit(1)
            elif len(directory_list) == 1:
                if search_path == '.':
                    recurse_path = '..'
                else:
                    recurse_path = search_path+'/..'
                path_list, root_found = self._check_for_metadata(search_path=recurse_path,
                                         path_list=path_list)
                path_list += directory_list
        return (path_list, root_found)

    def _update_directory_metadata_dict(self):
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


    def write_directory_metadata_dict(self, metadata_dict=None):
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

class MetadataAttribute(object):
    '''Operations on metadata about metadata
    '''
    def __init__(self,
                 desc=None,
                 units=None,
                 long_description=None,
                 max=None,
                 min=None,
                ):
        self.desc = desc
#
# helper functions called by multiple cli functions
#
def get_user_context_obj():
    '''Returns the user context, containing logging and metadata data.

    :return: User context object (dict)
    '''
    return click.get_current_context().obj

