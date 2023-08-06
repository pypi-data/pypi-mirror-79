infile   = {{i.infile    | quote}}
outfile  = {{o.outfile  | quote}}
obsvfile = {{o.obsvfile | quote}}
exptfile = {{o.exptfile | quote}}

{% if args.intype == 'cont' %}

#
#         | Disease | Healthy |
# --------+---------+---------+
#   mut   |   40    |   12    |
# non-mut |   23    |   98    |
# --------+---------+---------+
#
cont.table = read.table(infile, sep = "\t", header = T, row.names = 1, check.names = F)

{% else %}

#
# Contingency table rows: Mut, Non
# Contingency table cols: Disease, Healthy
#
#         | S1 | S2 | ... | Sn |
# --------+----+----+-----+----+
# Disease | 1  | 0  | ... | 1  |
# Healthy | 0  | 1  | ... | 0  |
# --------+----+----+-----+----+
# Mut     | 1  | 0  | ... | 1  |
# Non     | 0  | 1  | ... | 0  |
#
ct.cnames = c()
ct.rnames = c()
{% if isinstance(args.ctcols, list) %}
ct.cnames = {{args.ctcols}}
{% elif args.ctcols %}
ct.cnames = {{args.ctcols | lambda x: [y.strip() for y in x.split(',') if y.strip()]}}
{% else %}
trim  = Vectorize(function (x) gsub("^\\s+|\\s+$", "", x))
lines = readLines(infile, n = 2)
for (line in lines) {
	if (!startsWith(line, '# Contingency table ')) next
	if (startsWith(line, '# Contingency table cols:')) {
		ct.cnames = trim(unlist(strsplit(substring(line, 26), ',', fixed = T)))
	}
	else if (startsWith(line, '# Contingency table rows:')) {
		ct.rnames = trim(unlist(strsplit(substring(line, 26), ',', fixed = T)))
	}
}
{% endif %}

raw.data   = read.table(infile, sep = "\t", header = T, row.names = 1, check.names = F)
# generate contingency table
if (length(ct.rnames) == 0 && length(ct.cnames) == 0) {
	stop('No row names and col names specified for contingency table.')
}
if (length(ct.rnames) == 0) {
	ct.rnames = setdiff(rownames(raw.data), ct.cnames)
}
if (length(ct.cnames) == 0) {
	ct.cnames = setdiff(rownames(raw.data), ct.rnames)
}

# transposed cont.table
cont.table = matrix(NA, ncol = length(ct.cnames), nrow = length(ct.rnames))
colnames(cont.table) = ct.cnames
rownames(cont.table) = ct.rnames
# get the number of each contingency cell
for (rname in ct.rnames) {
	for (cname in ct.cnames) {
		tmp1 = raw.data[rname, ] == 1
		tmp2 = raw.data[cname, ] == 1
		tmp  = tmp1 & tmp2
		cont.table[rname, cname] = length(tmp[tmp])
	}
}
{% endif %}

# further parameters may be introduced, but for now just use defaults
ret = chisq.test(cont.table)
out = data.frame(Xsquare = ret$statistic, df = ret$parameter, pval = ret$p.value, method = ret$method)

#
# Xsquare 1.706667
# df  1
# pval    0.1914184
# method  Pearson's Chi-squared test with Yates' continuity correction
#
write.table(t(out), outfile, col.names = F, sep = "\t", quote = F)
write.table(ret$observed, obsvfile, sep = "\t", quote = F)
write.table(ret$expected, exptfile, sep = "\t", quote = F)
