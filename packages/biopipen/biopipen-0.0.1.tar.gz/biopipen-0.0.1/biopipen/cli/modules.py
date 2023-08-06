"""Load modules"""
import importlib.util
from typing import Union
from functools import lru_cache
from pathlib import Path
from itertools import zip_longest
from modkit import Module as ModkitModule
from rich import print as rich_print, box
from rich.table import Table
from pyppl import Proc
from .utils import (
    file_newer, ROOT_MODULE, CommandABC, logger, import_from_path
)

MODULE_DIR = Path(__file__).parent.parent
MODULE_FILES = [path for path in MODULE_DIR.glob('*.py')
                if not path.name.startswith('_')]

class Module(CommandABC):
    """A module of biopipely"""

    @classmethod
    @lru_cache()
    def collections(cls):
        """Load all modules"""
        ret = {}
        logger.debug('- Loading sub-modules ...')
        for modfile in MODULE_FILES:
            logger.debug('  Loading %s', modfile.stem)
            ret[modfile.stem] = cls(modfile)
        return ret

    @classmethod
    def use_cache(cls, cache_file: Path) -> bool:
        """Tell should we use the cache file"""
        return file_newer(cache_file, MODULE_FILES)

    @classmethod
    def is_a(cls, name: str) -> bool:
        """Tell if a given name is a module"""
        if "." in name:
            name = name.split(".")[0]
        return MODULE_DIR.joinpath(name + '.py').is_file()

    @classmethod
    def get(cls, name: str) -> Union["Module", "Process"]:
        """Get the module or process instance by name"""
        if "." in name:
            modname, procname = name.split(".", 1)
            return cls(MODULE_DIR.joinpath(modname + '.py')).procs[procname]
        return cls(MODULE_DIR.joinpath(name + '.py'))

    @classmethod
    def to_params(cls, params: "Params"):
        """Load the modules to params"""
        for modname, module in cls.collections().items():
            command = params.add_command(modname, desc=module.doc,
                                         group='MODULES')
            command.help_on_void = False
            for procname, proc in module.procs.items():
                proccmd = params.add_command(f"{modname}.{procname}",
                                             desc=proc.doc,
                                             group='PROCESSES')
                proc.to_params(proccmd)

    def __init__(self, path: Path):
        self.name = path.stem
        # load the module from path
        module = import_from_path(path)
        self.doc = (module.__doc__.strip()
                    if module.__doc__
                    else '[ Not documented ]')
        self.procs = Process.collections(module)

    def run(self, opts):
        """Nothing to do but just list all processes"""
        table = Table(box=box.SIMPLE)
        table.add_column('Process', style="green")
        table.add_column('Description')

        for name, proc in self.procs.items():
            table.add_row(name, proc.doc.rstrip())

        rich_print(table)

class Process:

    @classmethod
    @lru_cache()
    def collections(cls, module):
        processes = {}
        if isinstance(module, ModkitModule):
            for proc_id in module._PROC_FACTORY:
                proc = getattr(module, proc_id)
                processes[proc_id] = cls(
                    proc,
                    module._PROC_FACTORY[proc_id].aliasof
                )

            return processes

        for attr in dir(module):
            proc = getattr(module, attr)
            if not isinstance(proc, Proc):
                continue
            processes[attr] = cls(proc)

        return processes

    def __init__(self, proc, aliasof=None):
        self.proc = proc
        if aliasof:
            self.doc = 'Alias of [italic magenta]%s[/italic magenta]' % aliasof
        else:
            self.doc = proc.config.annotate.description or proc.desc

    def to_params(self, params):
        """Load to params"""
