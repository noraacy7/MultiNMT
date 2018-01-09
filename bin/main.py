"""Train model."""

from nmt import nmt

import tensorflow as tf
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    nmt.add_arguments(parser)
    nmt.FLAGS, unparsed = parser.parse_known_args()
    tf.app.run(main=nmt.main, argv=[sys.argv[0]]+unparsed)

if __name__=="__main__":
    main()
