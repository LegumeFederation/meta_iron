# -*- coding: utf-8 -*-
'''
meta_iron --

This is a command-line tool designed to deal with common problems
in creating and maintaining a biological data repository, namely:

    * Metadata creation, inheritance and flattening.
    * Filename regularization.
    * Resource discovery.
    * Data curation.

'''
#
# standard library imports
#
import warnings
import functools
import datetime
from pkg_resources import iter_entry_points
import locale
import os
import logging
from pathlib import Path # python 3.4 or later
#
# third-party imports
#
from click_plugins import with_plugins
#
# global logger object
#
logger = logging.getLogger('meta_iron')
#
# local imports
#
from .common import *
#
# set locale so grouping works
#
locale.setlocale(locale.LC_ALL, 'en_US')
#
# private context function
#
_ctx = click.get_current_context
#
# Class definitions begin here
#
class CleanInfoFormatter(logging.Formatter):
    '''A logging formatter for stderr usage
    '''
    def __init__(self, fmt = '%(levelname)s: %(message)s'):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        if record.levelno == logging.INFO:
            return record.getMessage()
        return logging.Formatter.format(self, record)
#
# function definitions begin here
#
def init_user_context(initial_context_obj=None):
    '''Put info from global options into user context dictionary
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if initial_context_obj is None:
                _ctx().obj = {}
            else:
                _ctx().obj = initial_context_obj
            ctx_dict = _ctx().obj
            if _ctx().params['verbose']:
                ctx_dict['logLevel'] = 'verbose'
            elif _ctx().params['quiet']:
                ctx_dict['logLevel'] = 'quiet'
            else:
                ctx_dict['logLevel'] = 'default'
            # change working directory if requested
            dir = _ctx().params['dir']
            if dir != '.':
                path = Path(str(dir)).expanduser()
                if not path.exists():
                    print('Error: --dir option target "%s" does not exist.'
                          %path)
                    sys.exit(1)
                elif not path.is_dir():
                    print('Error: --dir option target "%s" is not a directory.'
                          %path)
                    sys.exit(1)
                else:
                    os.chdir(str(path))
                    ctx_dict['dir'] = dir
            #
            for key in ['progress']:
                ctx_dict[key] = _ctx().params[key]
            return f(*args, **kwargs)
        return wrapper
    return decorator

def init_logging_to_stderr_and_file(file_log_level=DEFAULT_FILE_LOGLEVEL,
                     stderr_log_level=DEFAULT_STDERR_LOGLEVEL):
    '''Log to stderr and to a log file at different levels
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # find out the verbose/quiet level
            if _ctx().params['verbose']:
                _log_level = logging.DEBUG
            elif _ctx().params['quiet']:
                _log_level = logging.ERROR
            else:
                _log_level = stderr_log_level
            logger.setLevel(file_log_level)
            stderrHandler = logging.StreamHandler(sys.stderr)
            stderrFormatter = CleanInfoFormatter()
            stderrHandler.setFormatter(stderrFormatter)
            stderrHandler.setLevel(_log_level)
            logger.addHandler(stderrHandler)

            if not _ctx().params['no_logfile']: # start a log file
                # If a subcommand was used, log to a file in the
                # logs/ subdirectory of the current working directory
                #  with the subcommand in the file name.
                subcommand = _ctx().invoked_subcommand
                if subcommand is not None:
                    logfile_name = PROGRAM_NAME + '-'+ subcommand + '.log'
                    logfile_path = Path('./logs/'+logfile_name)
                    if not logfile_path.parent.is_dir(): # create logs/ dir
                        try:
                            logfile_path.parent.mkdir(mode=0o755, parents=True)
                        except OSError:
                            logger.error('Unable to create logfile directory "%s"',
                                         logfile_path.parent)
                            raise OSError
                    else:
                        if logfile_path.exists():
                            try:
                                logfile_path.unlink()
                            except OSError:
                                logger.error('Unable to remove existing logfile "%s"',
                                             logfile_path)
                                raise OSError
                    logfileHandler = logging.FileHandler(str(logfile_path))
                    logfileFormatter = logging.Formatter('%(levelname)s: %(message)s')
                    logfileHandler.setFormatter(logfileFormatter)
                    logfileHandler.setLevel(file_log_level)
                    logger.addHandler(logfileHandler)
            logger.debug('Command line: "%s"', ' '.join(sys.argv))
            logger.debug('%s version %s', PROGRAM_NAME, VERSION)
            logger.debug('Run started at %s', str(STARTTIME)[:-7])

            return f(*args, **kwargs)
        return wrapper
    return decorator


def log_elapsed_time():
    '''Log the elapsed time for long-lived commands
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            returnobj = f(*args, **kwargs)
            logger.debug('Elapsed time is %s', str(datetime.now()-STARTTIME)[:-7])
            return returnobj
        return wrapper
    return decorator

def init_metadata_object():
    '''Log the elapsed time for long-lived commands
    '''
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            _ctx().obj['metadata_obj'] = HierarchicalMetadataObject()
            return f(*args, **kwargs)
        return wrapper
    return decorator

#
# CLI entry point
#
@with_plugins(iter_entry_points('meta_iron.cli_plugins'))
@click.group(epilog=AUTHOR+' <'+EMAIL+'>.  '+COPYRIGHT)
@click.option('--warnings_as_errors', is_flag=True, show_default=True,
              default=False, help='Warnings cause exceptions.')
@click.option('-v', '--verbose', is_flag=True, show_default=True,
              default=False, help='Log debugging info to stderr.')
@click.option('-q', '--quiet', is_flag=True, show_default=True,
              default=False, help='Suppress logging to stderr.')
@click.option('--no_logfile', is_flag=True, show_default=True,
              default=False, help='Suppress logging to file.')
@click.option('--progress', is_flag=True, show_default=True,
              default=False, help='Show a progress bar, if supported.')
@click.option('--dir', default='.',
               help='Execute command in this directory. [default: PWD]')
@click.version_option(version=VERSION, prog_name=PROGRAM_NAME)
@init_user_context()
@init_logging_to_stderr_and_file()
@init_metadata_object()
def cli(warnings_as_errors, verbose, quiet,
        progress, no_logfile, dir):
    """meta_iron -- metadata flattening and smoothing

    If COMMAND is present, and --no_logfile was not invoked,
    a log file named meta_iron-COMMAND.log
    will be written in the ./logs/ directory.
    """
    if warnings_as_errors:
        logger.debug('Runtime warnings (e.g., from pandas) will cause exceptions')
        warnings.filterwarnings('error')

#

@cli.command()
@log_elapsed_time()
def test_logging():
    '''Logs at different severity levels.

        Example:
            meta_iron test_logging
    '''
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')


@cli.command()
def show_context_object():
    '''Prints the global context object.
    '''
    user_ctx = get_user_context_obj()
    logger.info('User context object, not including metadata')
    for key in user_ctx.keys():
        if key != 'metadata_obj':
            logger.info('   %s: %s', key, user_ctx[key])

@cli.command()
def show_metadata():
    '''Prints metadata from the current context.
    '''
    metadata_obj = get_user_context_obj()['metadata_obj']
    logger.info(metadata_obj)


#import other cli functions
from .directory import *
from .file import *
from .attributes import *
