#!/usr/bin/env python
"""Plot genomic elements."""
import json
from pathlib import Path
from pyppl import PyPPL
from diot import Diot
from biopipely import params, opts

HERE = Path(__file__).parent.resolve()
ARGS_FILE = HERE / 'gplot.args.toml'

help_group = 'SCRIPTS'
params = params.copy()

params.desc = [__doc__]
params.from_file(ARGS_FILE, force=True)

params.get_param('genes').callback = lambda val: val or opts.refgene
params.get_param('genome').show = True


def main(opts): # pylint: disable=too-many-branches,too-many-locals,too-many-statements
    """Main function"""
    from bioprocs.genomeplot import (pInteractionTrack,
                                     pAnnoTrack,
                                     pDataTrack,
                                     pUcscTrack,
                                     pGenomePlot)

    chrom, startend = opts.region.split(':')
    start, end = startend.split('-')
    start = int(start)
    end = int(end)
    track_procs = []
    #uuid       = utils.uid(str(sys.argv))
    for i, tracktype in enumerate(opts.tracks):
        if tracktype == 'data':
            datatrackproc = pDataTrack.copy(tag=opts.names[i])
            datatrackproc.input = (opts.names[i], opts.inputs[i], chrom)
            if opts.params:
                datatrackproc.args.opts.update(json.loads(opts.params[i]))
            track_procs.append(datatrackproc)
        elif tracktype == 'anno':
            annotrackproc = pAnnoTrack.copy(tag=opts.names[i])
            annotrackproc.input = (opts.names[i], opts.inputs[i], chrom)
            if opts.params:
                annotrackproc.args.opts.update(json.loads(opts.params[i]))
            track_procs.append(annotrackproc)
        elif tracktype == 'ucsc':
            ucsctrackproc = pUcscTrack.copy(tag=opts.names[i])
            ucsctrack, gviztrack = opts.inputs[i].split(':')
            ucsctrackproc.input = (opts.names[i], ucsctrack, gviztrack,
                                   opts.region)
            if opts.params:
                ucsctrackproc.args.opts.update(json.loads(opts.params[i]))
            track_procs.append(ucsctrackproc)
        else:
            intertrackproc = pInteractionTrack.copy(tag=opts.names[i])
            infile, intype = opts.inputs[i].split(':')
            intertrackproc.input = (opts.names[i], infile, opts.region)
            intertrackproc.args.intype = intype
            if opts.params:
                intertrackproc.args.opts.update(json.loads(opts.params[i]))
            track_procs.append(intertrackproc)

    if end - start > opts.splitlen:
        pGenomePlot.depends = track_procs
        #pGenomePlot.tag            = uuid
        pGenomePlot.forks = opts.forks
        pGenomePlot.exdir = opts.outdir
        pGenomePlot.args.ideoTrack = opts.ideo
        pGenomePlot.args.axisTrack = opts.axis
        pGenomePlot.args.geneTrack = opts.genes
        if opts.devpars:
            pGenomePlot.args.devpars.update(json.loads(opts.devpars))
        if opts.plotparams:
            pGenomePlot.args.opts.update(json.loads(opts.plotparams))
        if len(opts.highlights) == 2 and '-' not in opts.highlist[0]:
            hi1 = opts.highlights[0]
            hi2 = opts.highlights[1]
        else:
            hi1 = ';'.join(opts.highlights)
            hi2 = hi1
        pGenomePlot.input = lambda *chs: [
            ([ch.get() for ch in chs], "%s:%s-%s" %
             (chrom, start, start + 10000), hi1),
            ([ch.get() for ch in chs], "%s:%s-%s" %
             (chrom, end - 100000, end), hi2),
        ]

    else:
        pGenomePlot.depends = track_procs
        #pGenomePlot.tag            = uuid
        pGenomePlot.exdir = opts.outdir
        pGenomePlot.args.ideoTrack = opts.ideo
        pGenomePlot.args.axisTrack = opts.axis
        pGenomePlot.args.geneTrack = opts.genes
        if opts.devpars:
            pGenomePlot.args.devpars.update(json.loads(opts.devpars))
        if opts.plotparams:
            pGenomePlot.args.opts.update(json.loads(opts.plotparams))
        pGenomePlot.input = lambda *chs: [([ch.get() for ch in chs], opts.
                                           region, ';'.join(opts.highlights))]

    PyPPL().start(track_procs).run()


if __name__ == "__main__":
    main(params.parse())
