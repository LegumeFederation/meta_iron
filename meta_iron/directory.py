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
@click.argument('directorytype', type=str, default='')
def init_directory_metadata(dir):
    '''Initialize a metadata file.

    :param dir: Optional directory in which to initialize the file.
    If not present, the system-dependent default application directory
    will be used.  If this argument is '.', then the current working
    directory will be used.  This argument accepts tilde expansions.
    '''
    metadata_obj = get_user_context_obj()['metadata_obj']
    metadata_obj.write_metadata_dict(directorytype, metadata_dict={})



@cli.command()
def show_directory_metadata():
    '''Prints contents of directory metadata file.

        Example:
            meta_iron -v show_directory_metadata
    '''
    metadata_obj = get_user_context_obj()['metadata_obj']
    if not metadata_obj.metadata_found:
        logger.info('No metadata  was found, use init_directory_metadata first')
    else:
        logger.info('Metadata at this directory:')
        logger.info(metadata_obj.format_metadata(metadata_obj.directory_metadata))
        logger.info('\n')


@cli.command()
def show_flattened_directory_metadata():
    '''Prints contents of flattened metadata.

        Example:
            meta_iron -v show_flattened_directory_metadata
    '''
    metadata_obj = get_user_context_obj()['metadata_obj']
    if not metadata_obj.metadata_found:
        logger.info('No metadata  was found, use init_directory_metadata first')
    else:
        logger.info('Metadata at this directory:')
        logger.info(metadata_obj.format_metadata(metadata_obj.metadata, show_source=True))
        logger.info('\n')


@cli.command()
def write_flattened_directory_metadata():
    '''Writes metadata file.

        Example:
            meta_iron -v write_flattened_directory_metadata
    '''
    metadata_obj = get_user_context_obj()['metadata_obj']
    if not metadata_obj.metadata_found:
        logger.info('No metadata  was found, use init_directory_metadata first')
    else:
        logger.info('Metadata at this directory:')
        logger.info(metadata_obj.format_metadata(metadata_obj.metadata, show_source=True))
        logger.info('\n')