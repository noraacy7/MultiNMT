"""Shuffle dataset."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np
import argparse
import codecs


def main():
    parser = argparse.ArgumentParser(description="Shuffle corpus.")
    parser.add_argument("--data", nargs="+",
                required=True,
                help="List of corpus to shuffle.")
        args = parser.parse_args()
    # read files in the arg list
    name = args.data
    suffix = "." + args.suffix
    f = [codecs.open(item, "r", "utf-8") for item in name]
    data = [fd.readlines() for fd in f]
    size = min(len(lines) for lines in data)
    # shuffle order
    order = np.arange(size)
    np.random.shuffle(order)
    # generate shuffle file
    new_f = [codecs.open(item+".shuf", "w", "utf-8") for item in name]
    for idx in order.tolist():
        lines = [item[idx] for item in data]
        for line, fd in zip(lines, new_f):
            fd.write(line)
    for fdr, fdw in zip(f, new_f):
        fdr.close()
        fdw.close()


if __name__=="__main__":
    main()
