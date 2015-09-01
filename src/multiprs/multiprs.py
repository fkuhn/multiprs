__author__ = 'kuhn'

import argparse

def main():

    # top level parser
    parser = argparse.ArgumentParser(prog='multiprs', usage='%(prog)s [options]')
    subparsers = parser.add_subparsers(help='sub-command help')

    # sub parsers for 'turkish', 'english, 'german'  command
    parser_turkish = subparsers.add_parser('turkish', help='compare help')
    parser_german = subparsers.add_parser('german', help='compare help')
    parser_english = subparsers.add_parser('english', help='compare help')

    # parser
    subsubparsers = parser_turkish.add_subparsers(help='sub-command help')
    tag_turkish = subsubparsers.add_parser('tag', help='sub-command help')
    tag_turkish.add_argument('exmapath', action='append',  nargs=2, type=file, help='exmapath help')

