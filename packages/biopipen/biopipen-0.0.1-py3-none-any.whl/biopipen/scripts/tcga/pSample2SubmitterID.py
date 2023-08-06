"""Script for tcga.pSample2SubmitterID"""
# pylint: disable=invalid-name,undefined-variable
import json
import glob
import os
from shutil import copyfile
from threading import Lock
from bioprocs.utils.parallel import Parallel

# load varialbes
indir = {{i.indir | quote}}
mdfile = {{i.mdfile | quote}}
outdir = {{o.outdir | quote}}
nthread = {{args.nthread | repr}}
method = {{args.method | quote}}
length = {{args.len | repr}}

sam_meta = None
sample_ids = {}
with open(mdfile) as f:
    sam_meta = json.load(f)

exts = dict()
for sam in sam_meta:
    parts = sam['file_name'].split('.')
    ext = '.' + parts[-1]
    if ext == '.gz':
        ext = '.' + parts[-2] + ext
    exts[sam['file_name']] = ext
    sample_ids[sam['file_name']
               ] = sam['associated_entities'][0]['entity_submitter_id'][:length]

samfiles = []
for ext in set(exts.values()):
    samfiles += glob.glob(os.path.join(os.path.abspath(indir), "*" + ext))
    # or direct dir from TCGA download
    samfiles += glob.glob(os.path.join(os.path.abspath(indir), "*", "*" + ext))

lock = Lock()


def single(samfile):
    """Do a single file"""
    bn = os.path.basename(samfile)
    if not bn in sample_ids:
        return
    newfile = os.path.join(outdir, sample_ids[bn] + exts[bn])
    with lock:
        if os.path.exists(newfile):
            os.remove(newfile)
        if 'link' in method:
            os.symlink(samfile, newfile)
        elif method == 'copy':
            copyfile(samfile, newfile)


p = Parallel(nthread=nthread, backend='threading', raiseExc=True)
p.run(single, [(samfile,) for samfile in samfiles])
