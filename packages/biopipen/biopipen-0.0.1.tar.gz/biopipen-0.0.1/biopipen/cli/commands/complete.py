"""List all modules or processes of a given module"""
import sys
from pyparam import Params, POSITIONAL
from rich import print as rich_print, box
from rich.table import Table
from ..utils import logger

params = Params(desc=__doc__)
params.add_param('shell', type='choice', choices=['bash', 'fish', 'zsh'],
                 desc='The shell name')

def main(opts):
    from ..args import params
    print(params.shellcode(opts.shell))

if __name__ == '__main__':
    parsed = params.parse()
    main(parsed)
