"""Utilities for read/write TSV files"""

import types
import tempfile
from collections import OrderedDict

class TsvRecord:
    """Tsv record"""

    __slots__ = ('__keys', '__vals')

    def __init__(self, vals=None, keys=None):
        """
        r = TsvRecord([1,2,3,4,5])
        r.__vals == [1,2,3,4,5]
        r.__keys == None
        """
        self.__vals = vals or []
        if keys:
            self.__keys = dict(zip(keys, range(len(keys))))
            if len(self.__keys) != len(self.__vals):
                raise ValueError("Unequal length of keys and values. "
                                 "Make sure you don't have duplicated keys.")
        else:
            self.__keys = None

    def attachKeys(self, keys): # pylint: disable=invalid-name
        """Attach keys to the record"""
        if len(keys) != len(self.__vals):
            raise KeyError("Line doesn't have {} columns: {}".format(
                len(keys), self.__vals))
        self.__keys = dict(zip(keys, range(len(keys))))
    attach_keys = attachKeys

    def keys(self):
        """Get the keys of the record"""
        if not self.__keys:
            return range(len(self.__vals))
        return sorted(self.__keys, key=self.__keys.get)

    def values(self):
        """Get the values of the record"""
        return self.__vals

    def items(self):
        """Get the items of the record"""
        if not self.__keys:
            return enumerate(self.__vals)
        return zip(list(self.keys()), list(self.__vals))

    def __repr__(self):
        return '<TsvRecord: {!r}>'.format(dict(self.items()))

    def __getitem__(self, key):
        if isinstance(key, (slice, int)):
            return self.__vals[key]

        if self.__keys and key in self.__keys:
            return self.__vals[self.__keys[key]]

        raise KeyError("Record contains no '{}' field.".format(key))

    def __getattr__(self, key):
        if str(key).startswith('__') or str(key).startswith('_TsvRecord'):
            return super(TsvRecord, self).__getattr__(key)
        return self[key]

    def __setitem__(self, key, value):
        if isinstance(key, int):
            if key > len(self) or key < 0:
                raise IndexError('Index out of range: {}'.format(key))
            self.__vals[key] = value
        elif self.__keys and key in self.__keys:
            self.__vals[self.__keys[key]] = value
        else:
            self.__keys = self.__keys or {}
            self.__keys[key] = len(self)
            self.__vals.append(value)

    def __len__(self):
        return len(self.__vals)

    def __setattr__(self, key, value):
        if str(key).startswith('__') or str(key).startswith('_TsvRecord'):
            super(TsvRecord, self).__setattr__(key, value)
        else:
            self[key] = value

    def get(self, key, default=None):
        """Returns the value for a given key, or default."""
        try:
            return self[key]
        except KeyError:
            return default

    def __eq__(self, other):
        return self.keys() == other.keys() and self.values() == other.values()

    def __ne__(self, other):
        return not self.__eq__(other)

    def asDict(self, ordered=False): # pylint: disable=invalid-name
        """Returns the row as a dictionary, as ordered."""
        return OrderedDict(self.items()) if ordered else dict(ordered.items())
    as_dict = asDict

    def __contains__(self, key):
        return self.__keys and key in self.__keys

    def __delitem__(self, key):
        if not self.__keys:
            del self.__vals[key]
        elif key in self.__keys:
            del self.__vals[self.__keys[key]]
            del self.__keys[key]
        else:
            del self.__keys[list(self.keys())[key]]
            del self.__vals[key]

    def pop(self, key, *default):
        """Pop up a key of the recrod"""
        if not default and key not in self:
            raise KeyError("No such key: %s" % key)
        if len(default) > 2:
            raise ValueError("More than 1 default value.")
        if key not in self:
            return default[0]
        ret = self[key]
        del self[key]
        return ret


class TsvReader: # pylint: disable=too-many-instance-attributes
    """Tsv reader"""
    def __init__(self, # pylint: disable=too-many-arguments
                 infile,
                 delimit='\t',
                 comment='#',
                 skip=0,
                 # "False": no head;
                 # "None"/"True": split first line with delimit,
                 # "Callback": get head for first line in your way
                 cnames=True,
                 attach=True,
                 row=None,  # row factory
                 cname0="ROWNAME"):
        # in case infile is a Pathlib.Path object
        infile = str(infile)
        if infile.endswith('.gz'):
            import gzip
            self.file = gzip.open(infile, 'rt')
        else:
            self.file = open(infile, errors='replace')

        self.delimit = delimit
        self.comment = comment
        self.attach = attach
        self.row = row
        self.tell = 0

        if skip > 0:
            for _ in range(skip):
                self.file.readline()

        while True:
            self.tell = self.file.tell()
            line = self.file.readline()
            if comment and line.startswith(comment):
                continue
            self.file.seek(self.tell)
            break

        headline = self.file.readline() if cnames is not False else ''
        if callable(cnames):
            self.cnames = cnames(headline)
        elif headline:
            if comment and headline.startswith(comment):
                headline = headline[1:].lstrip()
            self.cnames = headline.rstrip('\n').split(delimit)
        else:
            self.cnames = []
        # try to add "cname0" as column name
        self.tell = self.file.tell()
        firstline = self.file.readline().rstrip('\n')
        ncols = len(firstline.split(delimit))

        if firstline and self.cnames and len(self.cnames) == ncols - 1:
            self.cnames.insert(0, cname0)
        if firstline and self.cnames and len(self.cnames) != ncols:
            raise ValueError('Not a valid tsv file. Head has '
                             '%s columns, while first line has %s.' %
                             (len(self.cnames), ncols))

        self.file.seek(self.tell)
        self.meta = self.cnames

    def next(self):
        """Get the next line"""
        line = self.file.readline()
        line = line.rstrip('\n')
        # empty lines not allowed
        if not line:
            raise StopIteration()
        record = TsvRecord(line.split(self.delimit))
        if self.attach and self.cnames:
            record.attachKeys(self.cnames)
        if callable(self.row):
            return self.row(record)
        return record

    def dump(self, col=None):
        """Dump all records"""
        if col is None:
            return list(self)
        if not isinstance(col, list):
            return [r[col] for r in self]
        return [tuple(r[c] for c in col) for r in self]

    def __next__(self):
        return self.next()

    def rewind(self):
        """Reset the file cursor"""
        self.file.seek(self.tell)

    def __iter__(self):
        return self

    def __del__(self):
        self.close()

    def close(self):
        """Close the file handle"""
        if hasattr(self, 'file') and self.file:
            self.file.close()


class TsvWriter:
    """Tsv writer"""
    def __init__(self, outfile=None, delimit='\t', append=False):
        openfunc = open
        outfile = str(outfile)  # support pathlib
        if outfile and outfile.endswith('.gz'):
            import gzip
            openfunc = gzip.open

        self.delimit = delimit
        self.cnames = []
        if outfile:
            self.file = openfunc(outfile, 'wt' if not append else 'at')
            self.filename = outfile
        else:
            self.file = tempfile.NamedTemporaryFile(delete=False)
            self.filename = self.file.name
        self.meta = self.cnames  # alias

    def writeHead(self, callback=True): # pylint: disable=invalid-name
        """Write the header to file"""
        if not self.cnames:
            return
        if callback and callable(callback):
            head = callback(self.cnames)
            if isinstance(head, list):
                head = self.delimit.join(head)
            self.file.write(head + "\n")
        elif callback:
            head = self.delimit.join(self.cnames)
            self.file.write(head + "\n")

    write_head = writeHead

    def write(self, record):
        """Write the recrod to file"""
        if isinstance(record, (list, types.GeneratorType)):
            self.file.write(self.delimit.join(str(v) for v in record) + '\n')
        elif isinstance(record, TsvRecord):
            if not self.cnames:
                self.write(record.values())
            else:
                self.write(record[n] for n in self.cnames)
        else:
            self.file.write(str(record))

    def __del__(self):
        self.close()

    def close(self):
        """Close the file handle."""
        if hasattr(self, 'file') and self.file:
            self.file.close()


class TsvJoin:
    """Join tsv files"""
    @staticmethod
    def compare(obja, objb, reverse=False):
        """Compare object a and b
        Return the index whose value is smaller if reverse is false
        """
        if not reverse:
            return 0 if obja < objb else 1 if obja > objb else -1
        return 0 if obja > objb else 1 if obja < objb else -1

    @staticmethod
    def _debug(rows, mat):
        from sys import stderr
        row_index = None
        for i, row in enumerate(rows):
            stderr.write("- File {}: {}\n".format(i+1, row))
            row_index = i
        if mat < 0:
            stderr.write("- Matched\n")
        else:
            stderr.write("- File {} is behand\n".format(row_index+1))
        stderr.write('-' * 80 + "\n")

    def __init__(self, *files, **inopts):
        inopts_default = dict(
            delimit='\t',
            comment='#',
            skip=0,
            cnames=True,
            attach=False,
            row=None,
            cname0="ROWNAME"
        )
        inopts_multi = {}
        self.length = len(files)
        for key, val in inopts.items():
            if not isinstance(val, list):
                inopts_multi[key] = [val] * self.length
            elif len(val) < self.length:
                inopts_multi[key] = val + \
                    [inopts_default[key]] * (self.length - len(val))
            else:
                inopts_multi[key] = val
        inopts = []
        for i in range(self.length):
            inopts.append({k: v[i] for k, v in inopts_multi.items()})
        self.readers = [TsvReader(f, **inopts[i]) for i, f in enumerate(files)]
        self.debug = False

    def _default_match(self, *rows):
        data = [row[0] for row in rows]
        mind = min(data)
        return -1 if data.count(mind) == self.length else data.index(mind)

    def join(self, do, outfile, match=None, outopts=None):
        """Start joining"""
        outopts = outopts or {}
        outopts['delimit'] = outopts.get('delimit', "\t")
        outopts['append'] = outopts.get('append', False)

        cnames = outopts.pop('cnames', False)

        head_callback = outopts.pop('headCallback')

        out = TsvWriter(outfile, **outopts)
        out.cnames = (cnames
                      if isinstance(cnames, list)
                      else self.readers[cnames].cnames
                      if isinstance(cnames, int) and not isinstance(cnames,
                                                                    bool)
                      else sum((reader.cnames
                                for reader in self.readers
                                if reader.cnames), [])
                      if cnames
                      else [])
        if out.cnames:
            out.writeHead(head_callback)

        match = match or self._default_match
        rows = [None] * self.length
        while True:
            try:
                for i, row in enumerate(rows):
                    rows[i] = row or next(self.readers[i])
                mat = match(*rows)
                if self.debug:
                    self._debug(rows, mat)
                if mat < 0:  # matched
                    do(out, *rows)
                    mat = 0
                rows[mat] = None
            except StopIteration:
                break
            except Exception:
                from sys import stderr
                from traceback import format_exc
                info = format_exc().splitlines()
                info.append("With rows:")
                info.extend(["- {}".format(r) for r in rows])
                stderr.write("\n".join(info) + "\n\n")
                rows = [None] * self.length
                continue
        out.close()
