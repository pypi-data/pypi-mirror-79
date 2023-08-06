"""Script for plink.pPlinkSimulate"""
# pylint: disable=undefined-variable,unused-import,invalid-name
# pylint: disable=unsupported-assignment-operation,not-a-mapping

from os import path
from diot import Diot
from bioprocs.utils import shell2 as shell

seed = {{i.seed | repr}}
outdir = {{o.outdir | quote}}
out = path.join(outdir, "simsnps." +
                str(seed if isinstance(seed, int) else 'noseed'))
plink = {{args.plink | repr}}
ncases = {{args.ncases | repr}}
nctrls = {{args.nctrls | repr}}
nsnps = {{args.nsnps | repr}}
label = {{args.label | repr}}
dprev = {{args.dprev | repr}}
minfreq = {{args.minfreq | repr}}
maxfreq = {{args.maxfreq | repr}}
hetodds = {{args.hetodds | repr}}
homodds = {{args.homodds | repr}}
params = {{args.params | repr}}

shell.load_config(plink=plink)

# write the parameter file
parfile = path.join(outdir, 'simsnps.par.txt')
with open(parfile, 'w') as f:
    f.write(
        "{nsnps}\t{label}\t{minfreq}\t{maxfreq}\t{hetodds}\t{homodds}\n".format(
            nsnps=nsnps, label=label, minfreq=minfreq,
            maxfreq=maxfreq, hetodds=hetodds, homodds=homodds
        )
    )
if isinstance(seed, int):
    params.seed = seed
params.simulate = parfile
params.out = out

params['simulate-ncases'] = ncases
params['simulate-ncontrols'] = nctrls
params['simulate-prevalence'] = dprev

shell.plink(**params).fg
