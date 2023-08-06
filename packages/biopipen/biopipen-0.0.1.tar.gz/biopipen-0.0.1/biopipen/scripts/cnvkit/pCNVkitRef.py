from os import path
from diot import Diot
from bioprocs.utils import shell2 as shell

cnvkit   = {{args.cnvkit | quote}}
infiles  = {{i.infiles | repr}}
ref      = {{args.ref | quote}}
outfile  = {{o.outfile | quote}}
params   = {{args.params | repr}}
nthread  = {{args.nthread | repr}}

shell.load_config(cnvkit = dict(
	_exe = cnvkit,
	_env = dict(
		OPENBLAS_NUM_THREADS = str(nthread),
		OMP_NUM_THREADS      = str(nthread),
		NUMEXPR_NUM_THREADS  = str(nthread),
		MKL_NUM_THREADS      = str(nthread)
	),
	_cwd = path.dirname(outfile)
))

params.o = outfile
params.f = ref
shell.cnvkit.reference(*infiles, **params).fg
