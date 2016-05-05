# -*- coding: utf-8 -*-
'''Defines directory types and implements commands on directories
'''

# module imports
from . import cli, get_user_context_obj, logger
from .common import *

#
# private context function
#
_ctx = click.get_current_context

@cli.command()
@click.argument('nodetype', type=str, default='')
def init_node_metadata(dir):
    '''Initialize a metadata file.

    :param dir: Optional directory in which to initialize the file.
    If not present, the system-dependent default application directory
    will be used.  If this argument is '.', then the current working
    directory will be used.  This argument accepts tilde expansions.
    '''
    global metadata_obj
    metadata_obj.write_metadata_dict(nodetype, metadata_dict={})

@cli.command()
def show_node_metadata():
    '''Prints location and contents of node metadata file.

        Example:
            meta_iron -v show_metadata
    '''
    global  metadata_obj

    if metadata_obj.metadata_dict == {}:
        logger.info('No metadata file was found.')
    else:
        logger.info('metadata file path is "%s".', metadata_obj.path)
        for key in metadata_obj.metadata_dict.keys():
            logger.info('  %s: %s', key, metadata_obj.metadata_dict[key])


