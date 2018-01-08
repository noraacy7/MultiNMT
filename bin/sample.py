"""Oversample script."""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import codecs


def repeat_corpus(corpus, repeat):
    """Copy line for repeat times.
    Args:
        corpus: parallel corpus to copy.
        repeat: repeat time.
    Return:
        New corpus repeat copy for times.
    """
    new_corpus = []
    for rep in range(repeat):
        new_corpus.extend(corpus)
    return new_corpus

def main():
    parser = argparse.ArgumentParser(description="Oversample corpus")
    parser.add_argument("--data", nargs="+", required=True,
                help="corpus to oversample")
    parser.add_argument("--repeat", default=10, type=int,
                help="number of repeat times")
    args = parser.parse_args()
    # read data
    streams = [codecs.open(data, "r", "utf-8") for data in args.data]
    corpus = [f.readlines() for f in streams]
    new_corpus = [repeat_corpus(lines, args.repeat) for lines in corpus]
    # write data into sample file
    new_streams = [codecs.open(data+".sample", "w", "utf-8") for data in args.data]
    for lines, f in zip(new_corpus, new_streams):
        for line in lines:
            f.write(line)
    for f, new_f in zip(streams, new_streams):
        f.close()
        new_f.close()


if __name__=="__main__":
    main()
