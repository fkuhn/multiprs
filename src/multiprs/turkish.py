import treetaggerwrapper
import corpustools
import argparse


# note: TreeTagger must be installed on your system


def extract_tier(corpuspath):
    """
    extracts
    :param corpuspath:
    :return:
    """
    collection = corpustools.ExmaIterator(corpuspath)


def main():
    """
    main method for turkish pos tagging
    :return:
    """
