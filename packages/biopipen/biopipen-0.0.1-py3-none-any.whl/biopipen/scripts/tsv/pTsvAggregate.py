import math
from functools import partial
from diot import Diot
from pyppl.utils import always_list
from bioprocs.utils.tsvio2 import TsvReader, TsvWriter

infile   = {{ i.infile | quote}}
outfile  = {{ o.outfile | quote}}
inopts   = {{ args.inopts | repr}}
on       = {{ args.on | ?:isinstance(_, int) or _.startswith('lambda ')
					  | =:_ | !quote}}
origin   = {{args.origin | repr}}
helper   = {{args.helper | repr}}
issorted = {{args.sorted | repr}}
if not isinstance(helper, list):
	helper = [helper]

# built-in aggregators
def aggr_sum(rs, idx):
	ret = [0] * len(idx)
	for r in rs:
		for i, ix in enumerate(idx):
			ret[i] += float(r[ix])
	return ret[0] if len(idx) == 1 else ret

def aggr_mean(rs, idx):
	lenrs = float(len(rs))
	sums  = aggr_sum(rs, idx)
	if len(idx) == 1:
		return sums/lenrs
	return [s/lenrs for s in sums]

def get_median(ls):
	ls = list(sorted(float(l) for l in ls))
	lenls = len(ls)
	if lenls % 2 == 1:
		return ls[int((lenls-1)/2.0)]
	return (ls[int((lenls-2)/2.0)] + ls[int(lenls/2.0)])/2.0

def aggr_median(rs, idx):
	if len(idx) == 1:
		return get_median(r[idx[0]] for r in rs)
	lss = [[] for _ in idx]
	for r in rs:
		for i, ix in enumerate(idx):
			lss[i].append(r[ix])
	return [get_median(ls) for ls in lss]

def aggr_min(rs, idx):
	if len(idx) == 1:
		return min(float(r[idx[0]]) for r in rs)
	ret = [None] * len(idx)
	for r in rs:
		for i, ix in enumerate(idx):
			ret[i] = r[ix] if ret[i] is None else min(ret[i], float(r[ix]))
	return ret

def aggr_max(rs, idx):
	if len(idx) == 1:
		return max(float(r[idx[0]]) for r in rs)
	ret = [None] * len(idx)
	for r in rs:
		for i, ix in enumerate(idx):
			ret[i] = r[ix] if ret[i] is None else max(ret[i], float(r[ix]))
	return ret

def aggr_fisher(rs, idx):
	from scipy.stats import combine_pvalues
	if (len(idx) == 1):
		return combine_pvalues([float(r[idx[0]]) for r in rs])[1]
	ret = [None] * len(idx)
	for i, ix in enumerate(idx):
		ret[i] = combine_pvalues([float(r[ix]) for r in rs])[1]
	return ret

def aggr_first(rs, idx):
	return rs[0][idx[0]]

def aggr_last(rs, idx):
	return rs[-1][idx[0]]

builtin = {
	"first" : aggr_first,
	"last"  : aggr_last,
	"sum"   : aggr_sum,
	"mean"  : aggr_mean,
	"median": aggr_median,
	"min"   : aggr_min,
	"max"   : aggr_max,
	"fisher": aggr_fisher,
}

helper = [line for line in helper if line]
exec('\n'.join(helper), globals())
aggrs   = Diot()
naggrs  = {}

{% for col, func in args.aggrs.items() %}
col  = {{col | quote}}
aggrs[col] = {{func | ?.startswith('$') | !:_ | =quote}}
if not callable(aggrs[col]) and not aggrs[col].startswith('$'):
	raise ValueError("I don't know how for {!r}.".format(col))
if not callable(aggrs[col]):
	fn, args = aggrs[col].split(':', 1)
	fn = fn.strip()[1:]
	if fn not in builtin:
		raise ValueError('Unknown builtin aggregation function, expect first, last, sum, mean, median, min or max.')
	args = [int(arg) if arg.isdigit() else arg for arg in args.strip().split(',')]
	aggrs[col] = partial(builtin[fn], idx = args)
naggrs[col] = len(always_list(col))
{% endfor %}

reader = TsvReader(infile, **inopts)
writer = TsvWriter(outfile, delimit = inopts.get('delimit', "\t"))
if not reader.cnames:
	row = next(reader)
	reader.rewind()
	reader.cnames = ['COL' + str(i+1) for i in range(len(row))]

if not isinstance(on, int) and not callable(on) and on not in reader.cnames:
	raise ValueError('{!r} is not a valid column name!'.format(on))

if 'keep' in origin:
	writer.cnames = reader.cnames[:]
writer.cnames += ['AggrOn'] + always_list(','.join(aggrs.keys()))
if on in reader.cnames:
	on = reader.cnames.index(on)

writer.writeHead()

group = None
rows  = {}
for row in reader:
	aggron = on(row) if callable(on) else row[on]
	if not issorted:
		rows.setdefault(aggron, []).append(row)
		continue

	if group is None:
		group = aggron

	if aggron == group:
		rows.setdefault(group, []).append(row)

	else:
		rows.setdefault(aggron, []).append(row)
		group = aggron

for grup, data in rows.items():
	aggrout = [grup]
	for newcol, aggr in aggrs.items():
		if naggrs[newcol] > 1:
			aggrout.extend(aggr(data))
		else:
			aggrout.append(aggr(data))
	if origin == 'keep':
		for row in data:
			writer.write(list(row.values()) + aggrout)
	elif origin in ('keep1', 'keep0'):
		writer.write(list(data[0].values()) + aggrout)
	elif origin == 'keep-1':
		writer.write(list(data[-1].values()) + aggrout)
	else:
		writer.write(aggrout)
writer.close()
