"""Simple tokenizer."""

import argparse
import codecs
import re
import os


def main():
    parser = argparse.ArgumentParser(description="Simple tokenizer")
    parser.add_argument("--data", default=None,
            required=True,
            help="Source text file")
    parser.add_argument("--save_token_data", default=None,
            required=True,
            help="Save token data file")
    args = parser.parse_args()
    # split token
    _WORD_SPLIT = re.compile("([.,!?\":;)(])")
    # tokenize
    with codecs.open(args.data, "r", "utf-8") as in_f:
        with codecs.open(args.save_token_data, "w", "utf-8") as out_f:
            for sentence in in_f:
                words = []
                segment = [w for w in sentence.strip().split()]
                for seg in segment:
                    words.extend(_WORD_SPLIT.split(seg))
                words = [w for w in words if w]
                out_f.write(" ".join(words) + "\n")


if __name__=="__main__":
    main()
