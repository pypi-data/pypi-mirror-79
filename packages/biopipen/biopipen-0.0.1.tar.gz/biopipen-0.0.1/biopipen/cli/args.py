"""Arguments of bioprocs"""
import logging
from pathlib import Path
from pyparam import Params, defaults
from .modules import Module
from .commands import Command
from .utils import file_newer, logger

defaults.CONSOLE_WIDTH = 100
defaults.HELP_OPTION_WIDTH = 28

CACHED_ARGS = Path('~/.biopipely.args.toml').expanduser()

def help_modifier(help_param, help_cmd):
    """Modify the help argument or command"""
    help_cmd.group = 'Other commands'

def help_callback(helps):
    """Modify help page"""
    # don't show all processes
    del helps['PROCESSES'][:]
    helps['PROCESSES'].append((['{modname.procname}'], ['Run a process.']))

    del helps['MODULES'][:]
    helps['MODULES'].append((['{modname}'], ['List process of the module.']))

params = Params(prog='biopipely',
                desc='A set of procs for bioinformatics.',
                help_callback=help_callback,
                help_modifier=help_modifier)
# see if anything changed, otherwise load from the CACHED_ARGS
if (not CACHED_ARGS.is_file() or
        not Command.use_cache(CACHED_ARGS) or
        not Module.use_cache(CACHED_ARGS) or
        file_newer(__file__, CACHED_ARGS)):
    logger.setLevel(logging.DEBUG)
    Command.to_params(params)
    Module.to_params(params)
    logger.setLevel(logging.INFO)
    params.to_file(CACHED_ARGS)
else:
    params.from_file(CACHED_ARGS)


# def helpx(helps):
#     """help assembler."""
#     from bioprocs.console.utils import Pipeline
#     helps.add('Assembled pipelines', sectype='option', prefix='')
#     helps.add('Processes', sectype='option', prefix='')
#     helps.add('Other commands', sectype='option', prefix='')
#     help_avail = helps.select('Available')
#     help_pipeline = helps.select('Assembled')
#     help_process = helps.select('Processes')
#     help_other = helps.select('Other')

#     for ppl in Pipeline.pipelines():
#         help_pipeline.add((ppl, '', Pipeline(ppl).desc))

#     help_process.add(help_avail.select('list'))
#     help_process.add(help_avail.select('proc'))
#     help_process.add(
#         ('<module>', '',
#          ['List the process of module.', 'Same as "bioprocs list <module>"']))
#     help_process.add(('<module.proc>', '', 'Run a process in command line.'))
#     help_other.add(help_avail.select('completion'))
#     help_other.add(help_avail.select('params'))
#     help_other.add(help_avail.select('profile'))
#     help_other.add(help_avail.select('help'))

#     helps.remove('Available')


# # modify help page
# commands._helpx = helpx
