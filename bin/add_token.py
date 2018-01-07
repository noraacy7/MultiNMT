"""Add artificial token to the head of training data to
tell the system which language to translate.
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import codecs
import sys


def main():
    parser = argparse.ArgumentParser(description="Add artificial token.")
    parser.add_argument("--data", nargs="+", required=True,
                help="Source data file.")
    parser.add_argument("--lang", nargs="+", required=True,
                help="Languages token, i.e. fr: French; es: Spanish; en: English")
    args = parser.parse_args()
    if len(args.data)!=len(args.lang):
        print("Files and languages don't match!")
        sys.exit(0)
    # write token to data
    name = args.data
    token = ["<2"+item+">" for item in args.lang]
    streams = [codecs.open(item, "r", "utf-8") for item in name]
    new_streams = [codecs.open(item+".2"+lang, "w", "utf-8") for item, lang in zip(name, args.lang)]
    for f, tok, new_f in zip(streams, token, new_streams):
        lines = f.readlines()
        lines = [tok+" "+line for line in lines]
        for line in lines:
            new_f.write(line)
    for f, new_f in zip(streams, new_streams):
        f.close()
        new_f.close()


if __name__=="__main__":
    main()
