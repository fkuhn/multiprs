import argparse
import sys
import os
import yaml

# top level parser
parser = argparse.ArgumentParser(prog='multiprs', usage='%(prog)s [options]')
subparsers = parser.add_subparsers(prog='train', help='sub-command help')
parser.add_argument('language', choices=['tr', 'de', 'en'], help='language to tag exb files from: tr, de, en')
parser.add_argument('filepath', help='filepath to exmaralda file')
parser.add_argument('outputfile', help='filepath to outputfile')

# create option for a config.yml


def main():

    args = parser.parse_args()

    if args.language == 'tr':
        parse_turkish(args)
    elif args.language == 'de':
        parse_german()
    elif args.language == 'en':
        parse_english()


def parse_turkish(args):
    print args.filepath


def parse_german():
    pass


def parse_english():
    pass


def train_paramterfile():
    pass


if __name__ == '__main__':
    main()
